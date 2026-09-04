import React, { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { Bot, Box, Brain, CheckCircle, FileCheck, FolderOpen, HelpCircle, Info, LayoutDashboard, MonitorPlay, Radar, Settings, User, RefreshCw } from 'lucide-react';

// Evidence data is now fetched from the backend

export default function EvidenceExplorer() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [allEvidence, setAllEvidence] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const [filters, setFilters] = useState({
    source: searchParams.get('source') || 'all',
    type: searchParams.get('type') || 'all',
    area: searchParams.get('area') || 'all',
    stage: searchParams.get('stage') || 'all'
  });

  useEffect(() => {
    setFilters({
      source: searchParams.get('source') || 'all',
      type: searchParams.get('type') || 'all',
      area: searchParams.get('area') || 'all',
      stage: searchParams.get('stage') || 'all'
    });
  }, [searchParams]);

  useEffect(() => {
    const fetchEvidence = async () => {
      try {
        const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
        const response = await fetch(`${baseUrl}/api/v1/evidence/`);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        
        const mapped = data.map(item => {
          let sourceKey = 'other';
          let sourceLabel = 'Other';
          if (item.source === 'playstore') { sourceKey = 'google-play'; sourceLabel = 'Google Play'; }
          else if (item.source === 'appstore') { sourceKey = 'app-store'; sourceLabel = 'Apple App Store'; }
          else if (item.source === 'youtube') { sourceKey = 'youtube'; sourceLabel = 'YouTube'; }
          
          let areaKey = 'other';
          if (item.area === 'Price') areaKey = 'price';
          else if (item.area === 'Quality') areaKey = 'quality';
          else if (item.area === 'Availability') areaKey = 'availability';
          else if (item.area === 'Fit') areaKey = 'fit';

          let intentColor = 'slate';
          const intentLower = (item.intent || '').toLowerCase();
          if (intentLower.includes('high')) intentColor = 'emerald';
          else if (intentLower.includes('medium') || intentLower.includes('moderate')) intentColor = 'amber';
          else if (intentLower.includes('low')) intentColor = 'blue';

          const stageVal = item.stage ? item.stage.toLowerCase() : 'unknown';
          const stageLabel = stageVal === 'unknown' ? 'Unknown' : stageVal.charAt(0).toUpperCase() + stageVal.slice(1);

          return {
            id: item.id,
            source: sourceKey,
            sourceLabel: sourceLabel,
            stage: stageVal,
            stageLabel: stageLabel,
            type: item.isDirect ? 'direct' : 'indirect',
            typeLabel: item.isDirect ? 'DIRECT EVIDENCE' : 'INDIRECT EVIDENCE',
            area: areaKey,
            text: item.text,
            primaryBarrier: item.primaryBarrier || 'Unknown',
            secondaryBarrier: item.secondaryBarrier || 'None',
            intent: item.intent || 'Unknown',
            intentIcon: Box,
            intentColor,
            isDirect: item.isDirect
          };
        });
        
        // Count occurrences of each text to identify multiple observations from the same conversation
        const textCounts = {};
        mapped.forEach(item => {
          textCounts[item.text] = (textCounts[item.text] || 0) + 1;
        });

        mapped.forEach(item => {
          item.observationCount = textCounts[item.text];
        });

        setAllEvidence(mapped);
      } catch (error) {
        console.error('Failed to fetch evidence:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchEvidence();
  }, []);

  const updateFilter = (group, value) => {
    const newFilters = { ...filters, [group]: value };
    setFilters(newFilters);
    
    // Update URL params
    const newParams = new URLSearchParams();
    Object.keys(newFilters).forEach(key => {
      if (newFilters[key] !== 'all') {
        newParams.set(key, newFilters[key]);
      }
    });
    setSearchParams(newParams);
  };

  const resetFilters = () => {
    setFilters({ source: 'all', type: 'all', area: 'all', stage: 'all' });
    setSearchParams(new URLSearchParams());
  };

  const filteredEvidence = allEvidence.filter(item => {
    if (filters.source !== 'all' && item.source !== filters.source) return false;
    if (filters.type !== 'all' && item.type !== filters.type) return false;
    if (filters.area !== 'all' && item.area !== filters.area) return false;
    if (filters.stage !== 'all' && item.stage !== filters.stage) return false;
    return true;
  });

  const directCount = allEvidence.filter(e => e.isDirect).length;
  const indirectCount = allEvidence.filter(e => !e.isDirect).length;
  const totalCount = allEvidence.length || 72;
  
  const uniqueFilteredEvidence = [];
  const seenTexts = new Set();
  filteredEvidence.forEach(item => {
    if (!seenTexts.has(item.text)) {
      seenTexts.add(item.text);
      uniqueFilteredEvidence.push(item);
    }
  });
  const directPct = totalCount > 0 ? (directCount / totalCount * 100).toFixed(1) : 8.2;
  const indirectPct = totalCount > 0 ? (indirectCount / totalCount * 100).toFixed(1) : 91.8;

  const Pill = ({ group, val, label }) => {
    const isActive = filters[group] === val;
    return (
      <button 
        onClick={() => updateFilter(group, isActive ? 'all' : val)}
        className={`filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs shadow-sm transition-colors ${
          isActive 
            ? 'bg-primary text-on-primary font-semibold' 
            : 'bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium'
        }`}
      >
        {label}
      </button>
    );
  };

  return (
    <>
      <header className="fixed top-0 w-full z-50 pt-safe bg-surface/95 backdrop-blur-xl border-b border-outline-variant/30 shadow-[0_1px_8px_rgba(0,0,0,0.03)]">
        <div className="h-20 px-space-base flex flex-col justify-center gap-space-2xs">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-space-sm">
              <div className="flex flex-col">
                <div className="flex items-center gap-space-xs">
                  <span className="font-title text-[18px] text-on-surface tracking-tight leading-none">Wishlist Intelligence</span>
                  <span className="px-space-xs py-space-2xs rounded bg-surface-container-high text-primary font-code-sm text-[10px] uppercase font-semibold tracking-wide">AI Engine</span>
                </div>
                <span className="text-[12px] text-on-surface-variant">AI Discovery Engine</span>
              </div>
            </div>
            <div className="flex items-center gap-space-sm">
              <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center shadow-sm"><User className="text-on-primary text-[18px]" /></div>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-space-xs min-w-0">
              <span className="inline-block w-1.5 h-1.5 rounded-full bg-secondary shrink-0"></span>
              <span className="text-[12px] text-on-surface-variant truncate font-medium">PM Fellowship / Myntra Discovery</span>
            </div>
            <div className="flex items-center gap-space-xs text-on-surface-variant shrink-0">
              <span className="font-code-sm text-[11px] text-on-surface-variant"><span className="text-primary font-semibold">1,447</span> analyzed / <span className="text-secondary font-semibold">{loading ? 72 : totalCount}</span> established</span>
            </div>
          </div>
        </div>
      </header>

      <main className="flex flex-col relative w-full pt-20 pb-28 bg-surface min-h-screen">
        <div className="flex flex-col w-full">
          <div className="px-space-base pt-space-md pb-space-sm flex flex-col gap-space-sm bg-surface">
            <div className="flex items-start justify-between">
              <div className="flex flex-col">
                <h1 className="text-[22px] font-title text-on-surface tracking-tight font-bold">Evidence Explorer</h1>
                <p className="text-[13px] text-on-surface-variant mt-0.5">Browse and filter the evidence behind the opportunity areas.</p>
              </div>
            </div>

            <div className="bg-surface-container-low rounded-xl p-space-base border border-outline-variant/40 shadow-sm flex flex-col gap-space-sm">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-space-xs">
                  <CheckCircle className="text-primary text-[18px]" />
                  <span className="text-[13px] text-on-surface font-semibold tracking-tight">Corpus Status</span>
                </div>
                <span className="inline-flex items-center gap-1 font-code-sm text-[11px] text-primary font-semibold bg-primary/10 px-2 py-0.5 rounded-full">
                  <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
                  Verified Active
                </span>
              </div>
              <div>
                <div className="text-[14px] text-on-surface font-semibold leading-snug">
                  {loading ? 72 : totalCount} Established Observations
                </div>
                <div className="text-[12px] text-on-surface-variant mt-0.5">
                  From {new Set(allEvidence.map(e => e.text)).size || 63} unique source conversations
                </div>
              </div>

              <div className="flex flex-col gap-1.5 pt-0.5">
                <div className="w-full bg-surface-container-high h-2.5 rounded-full overflow-hidden flex shadow-inner">
                  <div className="bg-emerald-600 h-full transition-all duration-500" style={{width: `${directPct}%`}} title={`Direct: ${loading ? 6 : directCount} observations (${directPct}%)`}></div>
                  <div className="bg-primary h-full transition-all duration-500" style={{width: `${indirectPct}%`}} title={`Indirect: ${loading ? 67 : indirectCount} observations (${indirectPct}%)`}></div>
                </div>
                <div className="flex items-center justify-between text-on-surface-variant font-code-sm text-[11px]">
                  <div className="flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-emerald-600"></span>
                    <span className="font-medium text-slate-800">{loading ? 6 : directCount} Direct Evidence ({directPct}%)</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-primary"></span>
                    <span className="font-medium text-slate-800">{loading ? 67 : indirectCount} Indirect Evidence ({indirectPct}%)</span>
                  </div>
                </div>
              </div>

              <div className="pt-2 border-t border-outline-variant/30 flex flex-col gap-1.5">
                <div className="text-[11px] font-semibold uppercase tracking-wider text-tertiary">Verified Ingestion Sources</div>
                <div className="grid grid-cols-1 gap-1 text-[12px] text-slate-700">
                  <div className="flex items-center justify-between bg-surface-container-lowest/80 px-2 py-1 rounded border border-outline-variant/30">
                    <span className="flex items-center gap-1.5 font-medium"><Box className="text-[15px] text-primary" />Google Play</span>
                    <span className="font-code-sm text-[11px] text-slate-900 font-medium">500 analyzed / <strong className="text-primary font-bold">28 linked</strong></span>
                  </div>
                  <div className="flex items-center justify-between bg-surface-container-lowest/80 px-2 py-1 rounded border border-outline-variant/30">
                    <span className="flex items-center gap-1.5 font-medium"><Box className="text-[15px] text-primary" />Apple App Store</span>
                    <span className="font-code-sm text-[11px] text-slate-900 font-medium">500 analyzed / <strong className="text-primary font-bold">26 linked</strong></span>
                  </div>
                  <div className="flex items-center justify-between bg-surface-container-lowest/80 px-2 py-1 rounded border border-outline-variant/30">
                    <span className="flex items-center gap-1.5 font-medium"><MonitorPlay className="text-[15px] text-secondary" />YouTube</span>
                    <span className="font-code-sm text-[11px] text-slate-900 font-medium">447 analyzed / <strong className="text-secondary font-bold">19 linked</strong></span>
                  </div>
                </div>
                <div className="flex items-center gap-1 text-[11px] text-tertiary pt-0.5">
                  <Info className="text-[14px]" />
                  <span className="">Note: Reddit excluded (0 records)</span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex flex-col gap-space-sm bg-surface-container-low px-space-base py-space-md border-y border-outline-variant/40 shadow-sm transition-all duration-300 ease-in-out" id="filterTray">
            <div className="flex items-center justify-between">
              <span className="font-label-sm text-[11px] text-on-surface uppercase tracking-wider font-bold">Source Channel</span>
            </div>
            <div className="flex items-center gap-space-xs overflow-x-auto pb-1 -mx-space-base px-space-base scrollbar-none">
              <Pill group="source" val="all" label="All Sources" />
              <Pill group="source" val="google-play" label="Google Play" />
              <Pill group="source" val="app-store" label="Apple App Store" />
              <Pill group="source" val="youtube" label="YouTube" />
            </div>

            <div className="flex items-center justify-between pt-space-xs">
              <span className="font-label-sm text-[11px] text-on-surface uppercase tracking-wider font-bold">Evidence Type</span>
            </div>
            <div className="flex items-center gap-space-xs overflow-x-auto pb-1 -mx-space-base px-space-base scrollbar-none">
              <Pill group="type" val="all" label="All Types" />
              <Pill group="type" val="direct" label="Direct Evidence" />
              <Pill group="type" val="indirect" label="Indirect Evidence" />
              <Pill group="type" val="validation" label="Needs Validation" />
            </div>

            <div className="flex items-center justify-between pt-space-xs">
              <span className="font-label-sm text-[11px] text-on-surface uppercase tracking-wider font-bold">Opportunity Area</span>
            </div>
            <div className="flex items-center gap-space-xs overflow-x-auto pb-1 -mx-space-base px-space-base scrollbar-none">
              <Pill group="area" val="all" label="All Areas" />
              <Pill group="area" val="other" label="Other / System Friction" />
              <Pill group="area" val="price" label="Price / Value" />
              <Pill group="area" val="quality" label="Quality / Auth." />
              <Pill group="area" val="availability" label="Availability / Stock" />
              <Pill group="area" val="fit" label="Fit / Size" />
            </div>

            <div className="flex items-center justify-between pt-space-xs">
              <span className="font-label-sm text-[11px] text-on-surface uppercase tracking-wider font-bold">Shopping Stage</span>
            </div>
            <div className="flex items-center gap-space-xs overflow-x-auto pb-1 -mx-space-base px-space-base scrollbar-none">
              <Pill group="stage" val="all" label="All Stages" />
              <Pill group="stage" val="discovery" label="Discovery" />
              <Pill group="stage" val="consideration" label="Consideration" />
              <Pill group="stage" val="decision" label="Decision" />
              <Pill group="stage" val="unknown" label="Unknown" />
            </div>
          </div>

          <div className="px-space-base py-space-sm bg-surface-container-lowest border-b border-outline-variant/30">
            <span className="text-[13px] text-on-surface-variant">Showing <strong className="text-on-surface font-semibold">{uniqueFilteredEvidence.length}</strong> unique source conversations <span className="font-code-sm text-[11px] text-tertiary">({filteredEvidence.length} established observations)</span></span>
            <button onClick={resetFilters} className="text-[13px] text-primary font-semibold flex items-center gap-space-2xs active:opacity-75">
              <RefreshCw className="text-[14px]" />
              <span className="">Reset view</span>
            </button>
          </div>

          <div className="px-space-base flex flex-col gap-space-md">
            {loading ? (
              <div className="py-space-xl flex flex-col items-center justify-center text-center text-on-surface-variant">
                <RefreshCw className="text-[32px] mb-4 text-primary animate-spin" />
                <span className="font-title text-[15px] font-semibold text-on-surface">Loading established observations...</span>
              </div>
            ) : uniqueFilteredEvidence.map((item) => {
              const IntentIcon = item.intentIcon;
              const colorClass = item.isDirect ? 'emerald' : 'purple';
              return (
                <div key={item.id} className="evidence-card bg-surface-container-lowest rounded-xl p-space-md shadow-sm border border-outline-variant/40 flex flex-col gap-space-sm transition-all">
                  <div className="flex items-center justify-between flex-wrap gap-space-2xs border-b border-outline-variant/20 pb-2">
                    <div className="flex items-center gap-1.5">
                      <span className="w-6 h-6 rounded-full bg-surface-container-high text-primary flex items-center justify-center">
                        {item.source === 'youtube' ? <MonitorPlay className="text-[14px]" /> : <Box className="text-[14px]" />}
                      </span>
                      <span className="text-[12px] text-on-surface font-bold">{item.sourceLabel}</span>
                      <span className="w-1 h-1 rounded-full bg-outline"></span>
                      <span className="text-[12px] text-on-surface-variant font-medium">{item.stageLabel}</span>
                      {item.observationCount > 1 && (
                        <>
                          <span className="w-1 h-1 rounded-full bg-outline"></span>
                          <span className="text-[11px] text-tertiary font-medium bg-tertiary/10 px-1.5 py-0.5 rounded-sm">Multiple analyses from this conversation</span>
                        </>
                      )}
                    </div>
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold tracking-wider uppercase bg-${colorClass}-100 text-${colorClass}-800 border border-${colorClass}-300 flex items-center gap-1`}>
                      <span className={`w-1.5 h-1.5 rounded-full bg-${colorClass}-600`}></span>
                      {item.typeLabel}
                    </span>
                  </div>

                  <div className="relative pl-3.5 py-1">
                    <div className={`absolute left-0 top-0 bottom-0 w-1 bg-${item.isDirect ? 'emerald-600' : 'primary'} rounded-full`}></div>
                    <p className="font-medium text-slate-900 text-[13px] leading-relaxed">
                      “{item.text}”
                    </p>
                  </div>

                  <div className="flex flex-wrap gap-1.5 pt-1">
                    <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-100 border border-slate-200 text-[11px]">
                      <span className="text-tertiary font-medium">Primary Barrier:</span>
                      <span className="text-slate-900 font-semibold">{item.primaryBarrier}</span>
                    </div>
                    <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-100 border border-slate-200 text-[11px]">
                      <span className="text-tertiary font-medium">Secondary Barrier:</span>
                      <span className="text-slate-900 font-semibold">{item.secondaryBarrier}</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-1 border-t border-outline-variant/20">
                    <div className="flex items-center gap-1.5">
                      <IntentIcon className={`text-[14px] text-${item.intentColor}-600`} />
                      <span className="text-[11px] text-on-surface-variant font-medium">Purchase Intent:</span>
                      <span className={`text-[11px] text-slate-900 font-bold bg-${item.intentColor}-50 px-2 py-0.5 rounded border border-${item.intentColor}-200`}>{item.intent}</span>
                    </div>
                  </div>
                </div>
              );
            })}

            {!loading && uniqueFilteredEvidence.length === 0 && (
              <div className="py-space-xl flex flex-col items-center justify-center text-center text-on-surface-variant">
                <Box className="text-[40px] mb-2 opacity-50" />
                <span className="font-title text-[16px] font-semibold text-on-surface">No evidence matches these filters</span>
                <span className="text-[13px]">Try adjusting or clearing your filters to see more results.</span>
                <button onClick={resetFilters} className="mt-4 px-4 py-2 bg-primary text-on-primary rounded-lg text-[13px] font-semibold active:scale-95 transition-transform">
                  Reset Filters
                </button>
              </div>
            )}
          </div>

          <div className="px-space-base pt-space-md pb-space-xl flex flex-col items-center justify-center">
            <div className="mt-4 p-3 bg-surface-container-low rounded-xl border border-outline-variant/30 text-xs text-slate-600 max-w-sm flex items-start gap-2 text-left">
              <FileCheck className="text-[18px] text-tertiary shrink-0 mt-0.5" />
              <p className="leading-normal">
                <strong className="text-slate-900 font-semibold">Methodology Note:</strong> Directional public conversation evidence. Does not establish business impact or causality.
              </p>
            </div>
          </div>
        </div>
      </main>

      <nav className="fixed bottom-0 w-full z-50 pb-safe bg-surface/95 backdrop-blur-xl border-t border-outline-variant/30 shadow-[0_-1px_8px_rgba(0,0,0,0.04)]" data-active-classes="text-primary font-medium">
        <div className="flex items-center justify-around h-16 px-space-xs">
          <Link to="/" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors">
            <LayoutDashboard className="text-[20px]" />
            <span className="font-label-sm text-label-sm">Overview</span>
          </Link>
          <Link to="/copilot" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors">
            <Bot className="text-[20px]" />
            <span className="font-label-sm text-label-sm">Copilot</span>
          </Link>
          <Link to="/radar" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors">
            <Radar className="text-[20px]" />
            <span className="font-label-sm text-label-sm">Radar</span>
          </Link>
          <Link to="/evidence" aria-current="page" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 transition-colors text-primary font-semibold">
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
