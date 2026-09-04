import asyncio
import argparse
import logging
import json
from app.db.session import AsyncSessionLocal
from app.engine.pipeline import AIPipeline
from app.engine.aggregation import InsightAggregator
from app.models.conversations import Conversation
from sqlalchemy.future import select

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_analysis(limit: int, model: str, dry_run: bool, validation_sample: bool):
    if validation_sample:
        limit = 20
        logger.info(f"Running in VALIDATION SAMPLE mode. Processing {limit} records.")

    async with AsyncSessionLocal() as db:
        # Fetch conversations (unprocessed logic can be added later, for now we limit)
        result = await db.execute(select(Conversation).limit(limit))
        conversations = result.scalars().all()
        
        pipeline = AIPipeline(db_session=db, model_name=model, dry_run=dry_run)
        
        results = []
        for conv in conversations:
            analysis = await pipeline.process_conversation(conv)
            if analysis:
                results.append((conv, analysis))

        if validation_sample:
            logger.info("\n--- VALIDATION SAMPLE RESULTS ---")
            for conv, analysis in results:
                print(f"\nSource ID: {conv.source_id}")
                safe_content = conv.raw_content[:200].encode('ascii', 'replace').decode('ascii')
                print(f"Content: {safe_content}...")
                print(f"Relevant: {analysis.relevance} (Score: {analysis.ai_confidence})")
                print(f"Reason: {analysis.relevance_reason}")
                print(f"Primary Barrier: {analysis.primary_barrier_category} - {analysis.primary_barrier_detail}")
                print("-" * 50)
            
            print("\nPlease manually inspect the above sample before full execution.")

async def run_aggregation(dry_run: bool, model: str):
    async with AsyncSessionLocal() as db:
        from app.engine.gemini import GeminiClient
        client = GeminiClient(model_name=model)
        aggregator = InsightAggregator(db_session=db, client=client, dry_run=dry_run)
        await aggregator.run()

def run_cli():
    parser = argparse.ArgumentParser(description="Myntra Discovery Engine - AI Pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_analysis = subparsers.add_parser("run-analysis")
    parser_analysis.add_argument("--limit", type=int, default=1000)
    parser_analysis.add_argument("--model", type=str, default="gemini-2.5-flash")
    parser_analysis.add_argument("--stage", type=str, help="Not fully implemented, runs all stages")
    parser_analysis.add_argument("--dry-run", action="store_true")
    parser_analysis.add_argument("--validation-sample", action="store_true")

    parser_agg = subparsers.add_parser("run-aggregation")
    parser_agg.add_argument("--dry-run", action="store_true")
    parser_agg.add_argument("--model", type=str, default="gemini-2.5-flash")

    args = parser.parse_args()

    if args.command == "run-analysis":
        asyncio.run(run_analysis(args.limit, args.model, args.dry_run, args.validation_sample))
    elif args.command == "run-aggregation":
        asyncio.run(run_aggregation(args.dry_run, args.model))

if __name__ == "__main__":
    run_cli()
