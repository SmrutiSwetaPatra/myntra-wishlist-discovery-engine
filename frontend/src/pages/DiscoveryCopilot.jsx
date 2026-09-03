import React, { useState } from 'react';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'https://myntra-wishlist-discovery-engine-production-5a76.up.railway.app';

export default function DiscoveryCopilot() {
  const [query, setQuery] = useState("What prevents wishlisted products from being purchased?");
  const [loading, setLoading] = useState(false);
  const [synthesis, setSynthesis] = useState(null);
  const [evidenceList, setEvidenceList] = useState([]);
  const [error, setError] = useState(null);
  
  // Basic session id generator
  const [sessionId] = useState(() => Math.random().toString(36).substring(2, 15));

  const suggestedPrompts = [
    { text: "What prevents wishlisted products from being purchased?", icon: "psychology" },
    { text: "Why do users save products but not buy them later?", icon: "help_outline" },
    { text: "What do users need to know before buying a saved fashion product?", icon: "apparel" },
    { text: "How do users compare shortlisted products?", icon: "compare" },
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
      const filteredEvidence = (data.evidence || []).filter(e => e.source?.toLowerCase() !== 'reddit').map(e => ({
        source: e.source,
        text: e.text || e.original_evidence_text || e.raw_content,
        type: e.type || (e.validation_status?.includes('direct') ? 'DIRECT EVIDENCE' : 'INDIRECT EVIDENCE'),
        confidence: e.confidence || 'Medium',
        stage: e.shopping_stage || 'Unknown',
        barrier: e.primary_barrier_category || 'Unknown'
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

      <main className="flex flex-col relative w-full pt-28 pb-28 bg-surface min-h-screen">
        <div className="flex flex-col w-full px-space-base gap-space-lg pb-space-xl">
          
          <div className="flex flex-col gap-space-2xs">
            <div className="flex items-center gap-space-xs">
              <span className="material-symbols-outlined text-primary text-[20px]" style={{fontVariationSettings: "'FILL' 1"}}>auto_awesome</span>
              <h1 className="font-headline-sm text-headline-sm text-on-surface tracking-tight">Discovery Copilot</h1>
            </div>
            <p className="font-body-sm text-body-sm text-on-surface-variant">Ask questions about what users say before they purchase.</p>
          </div>

          <div className="flex flex-col gap-space-sm bg-surface-container-lowest p-space-base rounded-xl shadow-sm border border-outline-variant/30">
            <div className="relative flex items-center">
              <span className="material-symbols-outlined absolute left-space-md text-on-surface-variant text-[20px] pointer-events-none">search</span>
              <input 
                className="w-full bg-surface-container-low text-on-surface font-body-md text-body-md pl-10 pr-space-base py-space-sm rounded-lg placeholder:text-outline focus:outline-none focus:bg-surface-container-lowest transition-all" 
                id="copilot-input" 
                placeholder="Ask what users need before buying a saved item..." 
                type="text" 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
              />
            </div>
            <div className="flex items-center justify-between gap-space-sm">
              <div className="flex items-center gap-space-xs text-on-surface-variant">
                <span className="material-symbols-outlined text-[16px] text-secondary">verified_user</span>
                <span className="font-label-sm text-label-sm">Grounded Synthesis</span>
              </div>
              <button 
                onClick={handleAsk}
                disabled={loading}
                className="bg-primary disabled:opacity-50 hover:bg-primary-container active:scale-95 transition-all text-on-primary font-label-md text-label-md px-space-base py-space-xs rounded-lg flex items-center gap-space-xs shadow-sm shadow-primary/20"
              >
                {loading ? (
                  <>
                    <span className="material-symbols-outlined text-[18px] animate-spin">refresh</span>
                    <span>Synthesizing...</span>
                  </>
                ) : (
                  <>
                    <span>Ask Copilot</span>
                    <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
                  </>
                )}
              </button>
            </div>

            <div className="flex flex-col gap-space-xs pt-space-xs border-t border-outline-variant/20">
              <span className="font-code-sm text-code-sm text-on-surface-variant uppercase tracking-wider font-medium">Suggested Exploration Prompts</span>
              <div className="flex flex-col gap-1.5" id="prompt-chips">
                {suggestedPrompts.map((prompt, idx) => (
                  <button 
                    key={idx}
                    onClick={() => setQuery(prompt.text)}
                    className={`prompt-pill text-left transition-colors font-label-sm text-label-sm px-space-sm py-2 rounded-lg flex items-center gap-2 ${query === prompt.text ? 'bg-surface-container-high text-primary' : 'bg-surface-container text-on-surface-variant hover:bg-surface-container-high hover:text-primary'}`} 
                    type="button"
                  >
                    <span className="material-symbols-outlined text-[16px] shrink-0 text-primary">{prompt.icon}</span>
                    <span className="leading-snug">{prompt.text}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="flex items-start gap-space-xs bg-surface-container p-space-sm rounded-lg border border-outline-variant/30">
            <span className="material-symbols-outlined text-secondary text-[18px] shrink-0 mt-0.5">policy</span>
            <p className="font-body-sm text-body-sm text-on-surface-variant leading-relaxed">
              <strong className="font-semibold text-on-surface">Strict Guardrail:</strong> Answers synthesized exclusively from retrieved public evidence (Google Play, Apple App Store, YouTube). Public conversation evidence is directional and should not be generalized to the wider user population without primary validation.
            </p>
          </div>

          {error && (
            <div className="bg-red-50 text-red-800 p-4 rounded-lg font-body-sm">
              {error}
            </div>
          )}

          {synthesis && (
            <div className="flex flex-col bg-surface-container-lowest rounded-xl shadow-md overflow-hidden border border-outline-variant/30">
              <div className="bg-primary p-space-base text-on-primary flex flex-col gap-space-2xs">
                <div className="flex items-center justify-between">
                  <span className="font-code-sm text-code-sm text-on-primary-container uppercase tracking-wider font-semibold flex items-center gap-1.5">
                    <span className="material-symbols-outlined text-[15px]">psychology</span>
                    AI-GENERATED SYNTHESIS
                  </span>
                  <span className="flex items-center gap-1.5 bg-surface-container-lowest/20 backdrop-blur-sm px-space-xs py-space-2xs rounded text-on-primary font-code-sm text-code-sm font-medium">
                    <span className="inline-block w-1.5 h-1.5 rounded-full bg-secondary-container animate-pulse"></span>
                    Grounded Output
                  </span>
                </div>
                <h2 className="font-headline-sm text-headline-sm text-on-primary font-semibold leading-snug">
                  “{query}”
                </h2>
              </div>
              
              <div className="p-space-base flex flex-col gap-space-md">
                <div className="flex flex-col gap-space-sm text-on-surface font-body-md text-body-md leading-relaxed whitespace-pre-wrap">
                  {synthesis}
                </div>
              </div>
            </div>
          )}

          {evidenceList.length > 0 && (
            <div className="flex flex-col gap-space-sm">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-space-xs">
                  <span className="material-symbols-outlined text-primary text-[20px]">fact_check</span>
                  <h2 className="font-title text-title text-on-surface">Supporting Ground Truth</h2>
                </div>
                <span className="font-code-sm text-code-sm text-on-surface-variant font-medium">{evidenceList.length} representative records shown</span>
              </div>

              <div className="flex flex-col gap-space-sm">
                {evidenceList.map((evidence, idx) => {
                  const isDirect = evidence.type === 'DIRECT EVIDENCE';
                  const colorClass = isDirect ? 'emerald' : 'purple';
                  
                  return (
                    <div key={idx} className="flex flex-col bg-surface-container-lowest p-space-base rounded-xl shadow-sm gap-space-sm border border-outline-variant/20">
                      <div className="flex items-start justify-between gap-space-xs">
                        <div className="flex items-center gap-space-xs">
                          <span className="material-symbols-outlined text-primary text-[20px] capitalize">{evidence.source?.includes('youtube') ? 'smart_display' : evidence.source?.includes('apple') ? 'phone_iphone' : 'play_circle'}</span>
                          <span className="font-title text-title text-on-surface font-semibold capitalize">{evidence.source}</span>
                        </div>
                        <span className={`px-space-xs py-space-2xs rounded bg-${colorClass}-100 text-${colorClass}-800 font-code-sm text-code-sm uppercase font-semibold border border-${colorClass}-300`}>
                          {evidence.type}
                        </span>
                      </div>
                      
                      <div className="flex flex-wrap gap-space-xs items-center">
                        <span className="bg-surface-container text-on-surface font-label-sm text-label-sm px-space-xs py-space-2xs rounded">
                          Stage: {evidence.stage}
                        </span>
                        <span className="bg-surface-container-high text-primary font-label-sm text-label-sm px-space-xs py-space-2xs rounded">
                          Primary Barrier: {evidence.barrier}
                        </span>
                        <span className="bg-surface-container-high text-secondary font-label-sm text-label-sm px-space-xs py-space-2xs rounded">
                          Confidence: {evidence.confidence}
                        </span>
                      </div>
                      
                      <blockquote className={`font-body-md text-body-md text-on-surface-variant bg-surface-container-low p-space-sm rounded-lg italic leading-relaxed border-l-2 border-${colorClass}-500`}>
                        “{evidence.text}”
                      </blockquote>
                      <div className="flex items-center justify-between pt-space-2xs">
                        <span className="font-code-sm text-code-sm text-on-surface-variant font-medium">Public Feedback</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

        </div>
      </main>
    </>
  );
}
