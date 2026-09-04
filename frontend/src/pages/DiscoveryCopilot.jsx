import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Box, Brain, ClipboardCheck, FileCheck, RefreshCw, Search, ShieldCheck, Sparkles, LayoutDashboard, Bot, Radar, FolderOpen, Settings } from 'lucide-react';
import ReactMarkdown from 'react-markdown';


const API_BASE = import.meta.env.VITE_API_BASE_URL || 'https://myntra-wishlist-discovery-engine-production-5a76.up.railway.app';

export default function DiscoveryCopilot() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [synthesis, setSynthesis] = useState(null);
  const [evidenceList, setEvidenceList] = useState([]);
  const [error, setError] = useState(null);
  
  // Basic session id generator
  const [sessionId] = useState(() => Math.random().toString(36).substring(2, 15));

  const suggestedPrompts = [
    { text: "What prevents wishlisted products from being purchased?" },
    { text: "Why do users save products but not buy them later?" },
    { text: "What do users need to know before buying a saved fashion product?" },
    { text: "How do users compare shortlisted products?" },
  ];

  const handleAsk = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    setSynthesis(null);
    setEvidenceList([]);

    try {
      const response = await fetch(`${API_BASE}/api/v1/copilot/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          session_id: sessionId,
          require_validated_only: false
        })
      });

      if (!response.ok) {
        throw new Error('Failed to fetch from Copilot API');
      }

      const data = await response.json();
      setSynthesis(data.answer);
      
      // Filter out Reddit and format evidence securely
      const filteredEvidence = (data.evidence_cards || data.evidence || []).filter(e => e.source?.toLowerCase() !== 'reddit').map(e => ({
        source: e.source,
        text: e.raw_text || e.text || e.original_evidence_text || e.raw_content,
        type: (e.direct_indirect_classification === 'direct' || e.validation_status?.includes('direct')) ? 'DIRECT EVIDENCE' : 'INDIRECT EVIDENCE',
        confidence: e.ai_confidence ? (e.ai_confidence > 0.8 ? 'High' : 'Medium') : (e.confidence || 'Medium'),
        stage: e.shopping_stage || 'Unknown',
        barrier: e.primary_barrier_category || 'Unknown',
        area: e.primary_barrier_category ? String(e.primary_barrier_category).toLowerCase().split('/')[0].trim() : 'other'
      }));
      setEvidenceList(filteredEvidence);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch response. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <header className="fixed top-0 w-full z-50 pt-safe bg-surface/90 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.04)]">
        <div className="h-20 px-space-base flex flex-col justify-center gap-space-2xs">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-space-sm">
              <div className="flex flex-col">
                <div className="flex items-center gap-space-xs">
                  <span className="font-title text-title text-on-surface tracking-tight leading-none">Wishlist Intelligence</span>
                  <span className="px-space-xs py-space-2xs rounded bg-surface-container-high text-primary font-code-sm text-code-sm uppercase font-medium">AI Engine</span>
                </div>
                <span className="font-body-sm text-body-sm text-on-surface-variant">AI Discovery Engine</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="flex flex-col relative w-full pt-24 pb-28 bg-surface min-h-screen">
        <div className="flex flex-col w-full px-space-base gap-space-md pb-space-md">
          
          <div className="flex flex-col gap-1">
            <div className="flex items-center gap-space-xs">
              <Sparkles className="text-primary text-[20px]" style={{fontVariationSettings: "'FILL' 1"}} />
              <h1 className="text-[22px] font-title text-on-surface tracking-tight font-bold">Discovery Copilot</h1>
            </div>
            <p className="text-[13px] text-on-surface-variant">Ask questions about what users say before they purchase.</p>
          </div>

          <div className="flex flex-col gap-space-sm bg-surface-container-lowest p-space-sm rounded-xl shadow-sm border border-outline-variant/30">
            <div className="relative flex items-center">
              <Search className="absolute left-space-md text-on-surface-variant text-[18px] pointer-events-none" />
              <input 
                className="w-full bg-surface-container-low text-on-surface text-[14px] pl-10 pr-space-base py-2 rounded-lg placeholder:text-outline focus:outline-none focus:bg-surface-container-lowest transition-all" 
                id="copilot-input" 
                placeholder="Ask a question about pre-purchase behavior..." 
                type="text" 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
              />
            </div>
            <div className="flex items-center justify-between gap-space-sm">
              <div className="flex items-center gap-space-xs text-on-surface-variant">
                <ShieldCheck className="text-[14px] text-secondary" />
                <span className="text-[12px] font-medium">Grounded Synthesis</span>
              </div>
              <button 
                onClick={handleAsk}
                disabled={loading}
                className="bg-primary disabled:opacity-50 hover:bg-primary-container active:scale-95 transition-all text-on-primary text-[13px] font-semibold px-4 py-1.5 rounded-lg flex items-center gap-space-xs shadow-sm shadow-primary/20"
              >
                {loading ? (
                  <>
                    <RefreshCw className="text-[18px] animate-spin" />
                    <span>Synthesizing...</span>
                  </>
                ) : (
                  <>
                    <span>Ask Copilot</span>
                    <ArrowRight className="text-[18px]" />
                  </>
                )}
              </button>
            </div>

            <div className="flex flex-col gap-space-xs pt-space-xs border-t border-outline-variant/20">
              <span className="text-[11px] text-on-surface-variant uppercase tracking-wider font-semibold">Suggested Exploration Prompts</span>
              <div className="flex flex-col gap-1" id="prompt-chips">
                {suggestedPrompts.map((prompt, idx) => (
                  <button 
                    key={idx}
                    onClick={() => setQuery(prompt.text)}
                    className={`prompt-pill text-left transition-colors text-[13px] px-2.5 py-1.5 rounded-lg flex items-center gap-2 ${query === prompt.text ? 'bg-surface-container-high text-primary font-medium' : 'bg-surface-container text-on-surface-variant hover:bg-surface-container-high hover:text-primary'}`} 
                    type="button"
                  >
                    <Box className="text-[14px] shrink-0 text-primary" />
                    <span className="leading-snug">{prompt.text}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="flex items-start gap-space-xs bg-surface-container p-space-sm rounded-lg border border-outline-variant/30">
            <FileCheck className="text-secondary text-[18px] shrink-0 mt-0.5" />
            <p className="font-body-sm text-body-sm text-on-surface-variant leading-relaxed">
              <strong className="font-semibold text-on-surface">Strict Guardrail:</strong> Answers synthesized exclusively from retrieved public evidence (Google Play, Apple App Store, YouTube). Public conversation evidence is directional and should not be generalized to the wider user population without primary validation.
            </p>
          </div>

          {error && (
            <div className="bg-error-container text-on-error-container p-space-md rounded-xl shadow-sm border border-error/20 flex flex-col gap-space-2xs">
              <span className="font-label-md text-label-md font-semibold">Synthesis Failed</span>
              <p className="font-body-sm text-body-sm">{error}</p>
            </div>
          )}

          {synthesis && (
            <div className="flex flex-col bg-surface-container-lowest rounded-xl shadow-md overflow-hidden border border-outline-variant/30">
              <div className="bg-primary p-space-sm text-on-primary flex flex-col gap-1">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] text-on-primary-container uppercase tracking-wider font-semibold flex items-center gap-1.5">
                    <Brain className="text-[14px]" />
                    AI-GENERATED SYNTHESIS
                  </span>
                  <span className="flex items-center gap-1.5 bg-surface-container-lowest/20 backdrop-blur-sm px-2 py-0.5 rounded text-on-primary text-[11px] font-medium">
                    <span className="inline-block w-1.5 h-1.5 rounded-full bg-secondary-container animate-pulse"></span>
                    Grounded Output
                  </span>
                </div>
                <h2 className="text-[16px] text-on-primary font-semibold leading-snug">
                  “{query}”
                </h2>
              </div>
              
              <div className="p-space-sm flex flex-col gap-space-md">
                <div className="flex flex-col gap-space-sm text-on-surface text-[14px] leading-relaxed">
                  <ReactMarkdown
                    components={{
                      p: ({node, ...props}) => <p className="mb-2 last:mb-0" {...props} />,
                      ul: ({node, ...props}) => <ul className="list-disc pl-5 mb-2 flex flex-col gap-1" {...props} />,
                      ol: ({node, ...props}) => <ol className="list-decimal pl-5 mb-2 flex flex-col gap-1" {...props} />,
                      li: ({node, ...props}) => <li className="pl-1" {...props} />,
                      strong: ({node, ...props}) => <strong className="font-semibold text-slate-900" {...props} />,
                      h1: ({node, ...props}) => <h1 className="text-lg font-bold mt-3 mb-2 text-slate-900" {...props} />,
                      h2: ({node, ...props}) => <h2 className="text-[15px] font-bold mt-3 mb-2 text-slate-900" {...props} />,
                      h3: ({node, ...props}) => <h3 className="text-[14px] font-bold mt-2 mb-1 text-slate-900" {...props} />
                    }}
                  >
                    {synthesis}
                  </ReactMarkdown>
                </div>
              </div>
            </div>
          )}

          {synthesis && evidenceList.length === 0 && (
            <div className="flex items-center gap-space-xs text-on-surface-variant p-space-sm bg-surface-container-lowest border border-outline-variant/30 rounded-lg">
              <ClipboardCheck className="text-[18px]" />
              <span className="text-[13px]">No retrieved evidence</span>
            </div>
          )}

          {evidenceList.length > 0 && (
            <div className="flex flex-col gap-space-sm">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-space-xs">
                  <ClipboardCheck className="text-primary text-[18px]" />
                  <h2 className="font-title text-[16px] text-on-surface">Retrieved Evidence</h2>
                </div>
                <span className="text-[11px] text-on-surface-variant font-medium">{evidenceList.length} representative records shown</span>
              </div>

              <div className="flex flex-col gap-space-sm">
                {evidenceList.map((evidence, idx) => {
                  const isDirect = evidence.type === 'DIRECT EVIDENCE';
                  const colorClass = isDirect ? 'emerald' : 'purple';
                  
                  return (
                    <div key={idx} className="flex flex-col bg-surface-container-lowest p-space-sm rounded-xl shadow-sm gap-space-sm border border-outline-variant/20">
                      <div className="flex items-start justify-between gap-space-xs">
                        <div className="flex items-center gap-space-xs">
                          <span className="text-primary text-[14px] font-bold">[Evidence {idx + 1}]</span>
                          <span className="font-title text-[14px] text-on-surface font-semibold capitalize ml-1">{evidence.source}</span>
                        </div>
                        <span className={`px-2 py-0.5 rounded bg-${colorClass}-100 text-${colorClass}-800 text-[10px] uppercase font-semibold border border-${colorClass}-300`}>
                          {evidence.type}
                        </span>
                      </div>
                      
                      <div className="flex flex-wrap gap-1.5 items-center">
                        <span className="bg-surface-container text-on-surface text-[11px] px-2 py-0.5 rounded">
                          Stage: {evidence.stage}
                        </span>
                        <span className="bg-surface-container-high text-primary text-[11px] px-2 py-0.5 rounded">
                          Primary Barrier: {evidence.barrier}
                        </span>
                        <span className="bg-surface-container-high text-secondary text-[11px] px-2 py-0.5 rounded">
                          Confidence: {evidence.confidence}
                        </span>
                      </div>
                      
                      <blockquote className={`text-[13px] text-on-surface-variant bg-surface-container-low p-space-sm rounded-lg italic leading-relaxed border-l-2 border-${colorClass}-500`}>
                        “{evidence.text}”
                      </blockquote>
                      <div className="flex items-center justify-between pt-space-2xs">
                        <Link to={`/evidence?area=${evidence.area}`} className="font-code-sm text-code-sm text-primary font-medium hover:underline flex items-center gap-1">
                          View in Evidence Explorer <ArrowRight className="text-[14px]" />
                        </Link>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

        </div>
      </main>

      <nav className="fixed bottom-0 w-full z-50 pb-safe bg-surface/95 backdrop-blur-xl border-t border-surface-container shadow-[0_-1px_8px_rgba(0,0,0,0.04)]">
        <div className="flex items-center justify-around h-16 px-space-xs">
          <Link to="/" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors">
            <LayoutDashboard className="text-[20px]" />
            <span className="font-label-sm text-label-sm">Overview</span>
          </Link>
          <Link to="/copilot" aria-current="page" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 transition-colors text-primary font-semibold">
            <Bot className="text-[20px]" />
            <span className="font-label-sm text-label-sm">Copilot</span>
          </Link>
          <Link to="/radar" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors">
            <Radar className="text-[20px]" />
            <span className="font-label-sm text-label-sm">Radar</span>
          </Link>
          <Link to="/evidence" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors">
            <FolderOpen className="text-[20px]" />
            <span className="font-label-sm text-label-sm">Evidence</span>
          </Link>
          <Link to="/settings" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors">
            <Settings className="text-[20px]" />
            <span className="font-label-sm text-label-sm">Settings</span>
          </Link>
        </div>
      </nav>
    </>
  );
}
