import json
import asyncio
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from app.engine.copilot import DiscoveryCopilot
from app.engine.gemini import GeminiClient
from app.db.session import AsyncSessionLocal

class JudgeResult(BaseModel):
    answer_relevance: float = Field(description="Score 0.0 to 1.0. Does the answer address the question?")
    factual_correctness: float = Field(description="Score 0.0 to 1.0. Are the claims factually consistent with the evidence?")
    evidence_grounding: float = Field(description="Score 0.0 to 1.0. 0.0 if any facts/statistics/demographics are invented without evidence.")
    direct_indirect_distinction: float = Field(description="Score 0.0 to 1.0. Does it properly distinguish direct wishlist evidence from broader indirect evidence? Score 1.0 if not applicable.")
    quantitative_correctness: float = Field(description="Score 0.0 to 1.0. If numbers are used, do they accurately reflect the provided metrics/evidence?")
    citation_accuracy: float = Field(description="Score 0.0 to 1.0. Are conversation IDs properly cited where substantive claims are made?")
    unsupported_causal_inference: bool = Field(description="True if it falsely claims causality without explicit evidence.")
    refusal_correctness: float = Field(description="Score 0.0 to 1.0. If refusal is expected or given, is it justified?")
    product_reasoning_quality: float = Field(description="Score 0.0 to 1.0. Does it evaluate opportunity based on evidence strength, not just volume?")
    critical_failure: bool = Field(description="True if there are hallucinated statistics, fabricated IDs, or unsupported causal claims.")
    feedback: str = Field(description="Brief explanation of the scores and any failures.")

JUDGE_PROMPT = """
You are an expert AI Evaluator judging a Product Discovery Copilot's response based STRICTLY on the provided retrieved evidence.

QUESTION: {question}
EXPECTED MODE: {expected_mode} (answerable, partially_answerable, or insufficient_evidence)

COPILOT'S RESPONSE:
{response}

DETERMINISTIC METRICS GIVEN TO COPILOT:
{metrics}

RETRIEVED EVIDENCE CARDS GIVEN TO COPILOT:
{evidence}

EVALUATION RULES:
1. Grounding: The Copilot MUST NOT invent any facts, demographics, or statistics not explicitly present in the provided evidence or metrics.
2. Direct vs Indirect: It must distinguish 'validated_relevant' (direct wishlist evidence) from 'indirect_pre_purchase' (indirect friction).
3. Causality: It must not claim A causes B unless explicitly stated in the text.
4. Volume vs Strength: It should not just assume the highest volume problem is the most important if direct evidence is lacking.

Evaluate the response according to the schema provided.
"""

async def run_eval():
    print("Initializing Copilot...")
    copilot = DiscoveryCopilot()
    judge_client = GeminiClient()
    
    async with AsyncSessionLocal() as session:
        await copilot.initialize(session)
        
    with open('app/engine/benchmark_questions.json', 'r') as f:
        questions = json.load(f)
        
    results = []
    
    print(f"Running eval on {len(questions)} questions...")
    for i, q in enumerate(questions):
        print(f"[{i+1}/{len(questions)}] Evaluating Q{q['id']}: {q['category']}")
        
        # 1. Run Copilot
        copilot_resp = await copilot.query(q['question'], session_id=f"eval_{q['id']}")
        
        # 2. Deterministic Validation
        det_score = 1.0
        det_failures = []
        
        expected_refusal = (q['expected_mode'] == 'insufficient_evidence')
        if expected_refusal and not copilot_resp.insufficient_evidence:
            det_score = 0.0
            det_failures.append("Expected insufficient_evidence refusal, but copilot answered.")
        elif not expected_refusal and copilot_resp.insufficient_evidence:
            det_score = 0.0
            det_failures.append("Unexpected refusal. Copilot should have attempted an answer.")
            
        # Verify IDs cited exist in retrieved cards
        retrieved_ids = [c.conversation_id for c in copilot_resp.evidence_cards]
        cited_ids = re.findall(r'\[ID:\s*([a-f0-9\-]+)\]', copilot_resp.answer)
        for cid in cited_ids:
            if cid not in retrieved_ids:
                det_score = 0.0
                det_failures.append(f"Hallucinated citation: {cid}")
                
        # Check excluded records
        for c in copilot_resp.evidence_cards:
            if "excluded" in c.validation_status:
                det_score = 0.0
                det_failures.append(f"Used excluded record: {c.conversation_id}")
                
        # 3. LLM-as-Judge
        evidence_str = json.dumps([c.model_dump() for c in copilot_resp.evidence_cards])
        prompt = JUDGE_PROMPT.format(
            question=q['question'],
            expected_mode=q['expected_mode'],
            response=copilot_resp.model_dump_json(),
            metrics=json.dumps(copilot_resp.metrics),
            evidence=evidence_str
        )
        
        try:
            judge_res = await judge_client.extract_structured(prompt, "", JudgeResult)
        except Exception as e:
            print(f"Judge extraction failed for Q{q['id']}: {e}")
            judge_res = JudgeResult(
                answer_relevance=0, factual_correctness=0, evidence_grounding=0,
                direct_indirect_distinction=0, quantitative_correctness=0, citation_accuracy=0,
                unsupported_causal_inference=True, refusal_correctness=0, product_reasoning_quality=0,
                critical_failure=True, feedback=f"Judge failed: {e}"
            )
            
        # 4. Compute final score
        # Base LLM score average
        llm_score = (
            judge_res.answer_relevance +
            judge_res.factual_correctness +
            judge_res.evidence_grounding +
            judge_res.direct_indirect_distinction +
            judge_res.quantitative_correctness +
            judge_res.citation_accuracy +
            judge_res.refusal_correctness +
            judge_res.product_reasoning_quality
        ) / 8.0
        
        if judge_res.critical_failure or judge_res.unsupported_causal_inference or not det_score:
            final_score = 0.0
        else:
            final_score = (llm_score + det_score) / 2.0
            
        if final_score >= 0.80:
            status = "PASS"
        elif final_score >= 0.60:
            status = "REVIEW"
        else:
            status = "FAIL"
            
        result = {
            "id": q["id"],
            "category": q["category"],
            "expected_mode": q["expected_mode"],
            "question": q["question"],
            "status": status,
            "final_score": final_score,
            "deterministic_score": det_score,
            "deterministic_failures": det_failures,
            "llm_score": llm_score,
            "judge_result": judge_res.model_dump(),
            "copilot_response": copilot_resp.model_dump(),
        }
        results.append(result)
        
    # Generate JSON
    with open('benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=2)
        
    # Generate Report
    report_lines = ["# Discovery Benchmark Report\n"]
    
    total = len(results)
    passes = sum(1 for r in results if r['status'] == 'PASS')
    reviews = sum(1 for r in results if r['status'] == 'REVIEW')
    fails = sum(1 for r in results if r['status'] == 'FAIL')
    avg_score = sum(r['final_score'] for r in results) / total
    
    report_lines.append(f"**Overall Score:** {avg_score*100:.1f}%\n")
    report_lines.append(f"**Pass:** {passes} | **Review:** {reviews} | **Fail:** {fails}\n")
    
    # Category stats
    cat_scores = {}
    for r in results:
        cat = r['category']
        if cat not in cat_scores:
            cat_scores[cat] = []
        cat_scores[cat].append(r['final_score'])
        
    report_lines.append("## Category Scores")
    for cat, scores in cat_scores.items():
        report_lines.append(f"- **{cat}:** {sum(scores)/len(scores)*100:.1f}%")
        
    # Expected Mode stats
    mode_scores = {}
    for r in results:
        mode = r['expected_mode']
        if mode not in mode_scores:
            mode_scores[mode] = []
        mode_scores[mode].append(r['final_score'])
        
    report_lines.append("\n## Expected Mode Scores")
    for mode, scores in mode_scores.items():
        report_lines.append(f"- **{mode}:** {sum(scores)/len(scores)*100:.1f}%")
        
    # Failures
    report_lines.append("\n## Failures")
    for r in results:
        if r['status'] == 'FAIL':
            report_lines.append(f"\n### {r['id']} ({r['expected_mode']})")
            report_lines.append(f"**Q:** {r['question']}")
            report_lines.append(f"**Det Failures:** {r['deterministic_failures']}")
            report_lines.append(f"**Judge Feedback:** {r['judge_result']['feedback']}")
            if r['judge_result']['critical_failure']:
                report_lines.append(f"**CRITICAL FAILURE FLAGGED**")
                
    with open('benchmark_report.md', 'w') as f:
        f.write("\n".join(report_lines))
        
    print("Benchmark complete! Results saved.")

if __name__ == "__main__":
    asyncio.run(run_eval())
