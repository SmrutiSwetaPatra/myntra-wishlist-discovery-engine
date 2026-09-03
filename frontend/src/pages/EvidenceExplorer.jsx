import React from 'react';

export default function EvidenceExplorer() {
  return (
    <>
<header className="fixed top-0 w-full z-50 pt-safe bg-surface/95 backdrop-blur-xl border-b border-outline-variant/30 shadow-[0_1px_8px_rgba(0,0,0,0.03)]"><div className="h-20 px-space-base flex flex-col justify-center gap-space-2xs"><div className="flex items-center justify-between"><div className="flex items-center gap-space-sm"><div className="flex flex-col"><div className="flex items-center gap-space-xs"><span className="font-title text-title text-on-surface tracking-tight leading-none">Wishlist Intelligence</span><span className="px-space-xs py-space-2xs rounded bg-surface-container-high text-primary font-code-sm text-[10px] uppercase font-semibold tracking-wide">AI Engine</span></div><span className="font-body-sm text-body-sm text-on-surface-variant">AI Discovery Engine</span></div></div><div className="flex items-center gap-space-sm"><div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center shadow-sm"><span className="material-symbols-outlined text-on-primary text-[18px]">person</span></div></div></div><div className="flex items-center justify-between"><div className="flex items-center gap-space-xs min-w-0"><span className="inline-block w-1.5 h-1.5 rounded-full bg-secondary shrink-0"></span><span className="font-label-sm text-label-sm text-on-surface-variant truncate font-medium">PM Fellowship / Myntra Discovery</span></div><div className="flex items-center gap-space-xs text-on-surface-variant shrink-0"><span className="font-code-sm text-[11px] text-on-surface-variant"><span className="text-primary font-semibold">1,447</span> analyzed / <span className="text-secondary font-semibold">73</span> established</span></div></div></div></header><main className="flex flex-col relative w-full pt-20 pb-28 bg-surface min-h-screen"><div className="flex flex-col w-full">
<div className="px-space-base pt-space-md pb-space-sm flex flex-col gap-space-sm bg-surface">
<div className="flex items-start justify-between">
<div className="flex flex-col">
<h1 className="font-headline-md text-headline-md text-on-surface tracking-tight font-bold">Evidence Explorer</h1>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">Browse and filter the evidence behind the opportunity areas.</p>
</div>
<button aria-label="Toggle filter tray" className="h-9 px-space-sm rounded-xl bg-surface-container-high text-primary flex items-center gap-space-xs font-label-sm text-label-sm shadow-sm active:scale-95 transition-transform border border-primary/10" id="filterToggleBtn">
<span className="material-symbols-outlined text-[18px]">tune</span>
<span className="font-semibold">Filter (3)</span>
</button>
</div>

<div className="bg-surface-container-low rounded-xl p-space-base border border-outline-variant/40 shadow-sm flex flex-col gap-space-sm">
<div className="flex items-center justify-between">
<div className="flex items-center gap-space-xs">
<span className="material-symbols-outlined text-primary text-[18px]">verified</span>
<span className="font-label-sm text-label-sm text-on-surface font-semibold tracking-tight">Corpus Status</span>
</div>
<span className="inline-flex items-center gap-1 font-code-sm text-xs text-primary font-semibold bg-primary/10 px-2 py-0.5 rounded-full">
<span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
Verified Active
</span>
</div>
<div>
<div className="font-label-md text-sm text-on-surface font-semibold leading-snug">
73 Established Pre-Purchase Records
</div>
<div className="font-body-sm text-xs text-on-surface-variant mt-0.5">
(6 Direct Evidence, 67 Indirect Evidence)
</div>
</div>

<div className="flex flex-col gap-1.5 pt-0.5">
<div className="w-full bg-surface-container-high h-2.5 rounded-full overflow-hidden flex shadow-inner">
<div className="bg-emerald-600 h-full transition-all duration-500" style={{width: "8.2%"}} title="Direct: 6 records (8.2%)"></div>
<div className="bg-primary h-full transition-all duration-500" style={{width: "91.8%"}} title="Indirect: 67 records (91.8%)"></div>
</div>
<div className="flex items-center justify-between text-on-surface-variant font-code-sm text-[11px]">
<div className="flex items-center gap-1.5">
<span className="w-2 h-2 rounded-full bg-emerald-600"></span>
<span className="font-medium text-slate-800">6 Direct Evidence (8.2%)</span>
</div>
<div className="flex items-center gap-1.5">
<span className="w-2 h-2 rounded-full bg-primary"></span>
<span className="font-medium text-slate-800">67 Indirect Evidence (91.8%)</span>
</div>
</div>
</div>

<div className="pt-2 border-t border-outline-variant/30 flex flex-col gap-1.5">
<div className="text-[11px] font-semibold uppercase tracking-wider text-tertiary">Verified Ingestion Sources</div>
<div className="grid grid-cols-1 gap-1 text-[12px] font-body-sm text-slate-700">
<div className="flex items-center justify-between bg-surface-container-lowest/80 px-2 py-1 rounded border border-outline-variant/30">
<span className="flex items-center gap-1.5 font-medium"><span className="material-symbols-outlined text-[15px] text-primary">shop</span>Google Play</span>
<span className="font-code-sm text-[11px] text-slate-900 font-medium">500 analyzed / <strong className="text-primary font-bold">28 linked</strong></span>
</div>
<div className="flex items-center justify-between bg-surface-container-lowest/80 px-2 py-1 rounded border border-outline-variant/30">
<span className="flex items-center gap-1.5 font-medium"><span className="material-symbols-outlined text-[15px] text-primary">file_download</span>Apple App Store</span>
<span className="font-code-sm text-[11px] text-slate-900 font-medium">500 analyzed / <strong className="text-primary font-bold">26 linked</strong></span>
</div>
<div className="flex items-center justify-between bg-surface-container-lowest/80 px-2 py-1 rounded border border-outline-variant/30">
<span className="flex items-center gap-1.5 font-medium"><span className="material-symbols-outlined text-[15px] text-secondary">smart_display</span>YouTube</span>
<span className="font-code-sm text-[11px] text-slate-900 font-medium">447 analyzed / <strong className="text-secondary font-bold">19 linked</strong></span>
</div>
</div>
<div className="flex items-center gap-1 text-[11px] text-tertiary pt-0.5">
<span className="material-symbols-outlined text-[14px]">info</span>
<span className="">Note: Reddit excluded (0 records)</span>
</div>
</div>
</div>
</div>

<div className="flex flex-col gap-space-sm bg-surface-container-low px-space-base py-space-md border-y border-outline-variant/40 shadow-sm transition-all duration-300 ease-in-out" id="filterTray">

<div className="flex items-center justify-between">
<span className="font-label-sm text-[11px] text-on-surface uppercase tracking-wider font-bold">Source Channel</span>
<span className="font-code-sm text-[11px] text-tertiary">Single Select</span>
</div>
<div className="flex items-center gap-space-xs overflow-x-auto pb-1 -mx-space-base px-space-base scrollbar-none">
<button className="filter-pill active shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-primary text-on-primary font-semibold shadow-sm transition-colors" data-group="source" data-val="all">All Sources (73)</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="source" data-val="google-play">Google Play (28)</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="source" data-val="app-store">Apple App Store (26)</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="source" data-val="youtube">YouTube (19)</button>
</div>

<div className="flex items-center justify-between pt-space-xs">
<span className="font-label-sm text-[11px] text-on-surface uppercase tracking-wider font-bold">Evidence Type</span>
</div>
<div className="flex items-center gap-space-xs overflow-x-auto pb-1 -mx-space-base px-space-base scrollbar-none">
<button className="filter-pill active shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-primary text-on-primary font-semibold shadow-sm transition-colors" data-group="type" data-val="all">All Types</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="type" data-val="direct">Direct Evidence (6)</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="type" data-val="indirect">Indirect Evidence (67)</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="type" data-val="validation">Needs Validation (24)</button>
</div>

<div className="flex items-center justify-between pt-space-xs">
<span className="font-label-sm text-[11px] text-on-surface uppercase tracking-wider font-bold">Opportunity Area</span>
</div>
<div className="flex items-center gap-space-xs overflow-x-auto pb-1 -mx-space-base px-space-base scrollbar-none">
<button className="filter-pill active shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-primary text-on-primary font-semibold shadow-sm transition-colors" data-group="area" data-val="all">All Areas</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="area" data-val="other">Other / System Friction (24) · Needs Validation</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="area" data-val="price">Price / Value (19)</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="area" data-val="quality">Quality / Authenticity (15)</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="area" data-val="availability">Availability / Stock (10)</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="area" data-val="fit">Fit / Size (5)</button>
</div>

<div className="flex items-center justify-between pt-space-xs">
<span className="font-label-sm text-[11px] text-on-surface uppercase tracking-wider font-bold">Shopping Stage</span>
</div>
<div className="flex items-center gap-space-xs overflow-x-auto pb-1 -mx-space-base px-space-base scrollbar-none">
<button className="filter-pill active shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-primary text-on-primary font-semibold shadow-sm transition-colors" data-group="stage" data-val="all">All Stages</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="stage" data-val="save">Save</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="stage" data-val="revisit">Revisit</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="stage" data-val="evaluate">Evaluate</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="stage" data-val="uncertainty">Resolve Uncertainty</button>
<button className="filter-pill shrink-0 px-3 py-1.5 rounded-full font-label-sm text-xs bg-surface-container-high text-on-surface hover:bg-primary/15 font-medium transition-colors" data-group="stage" data-val="decide">Decide</button>
</div>
</div>

<div className="px-space-base py-space-sm flex items-center justify-between bg-surface">
<span className="font-label-sm text-label-sm text-on-surface-variant">Showing <strong className="text-on-surface font-label-md">6</strong> of <span className="font-code-sm text-code-sm font-semibold">73</span> verified entries</span>
<button className="font-label-sm text-label-sm text-primary font-semibold flex items-center gap-space-2xs active:opacity-75" id="resetFilters">
<span className="material-symbols-outlined text-[16px]">restart_alt</span>
<span className="">Reset view</span>
</button>
</div>

<div className="px-space-base flex flex-col gap-space-md">

<div className="evidence-card bg-surface-container-lowest rounded-xl p-space-md shadow-sm border border-outline-variant/40 flex flex-col gap-space-sm transition-all" data-area="price" data-source="google-play" data-stage="uncertainty" data-type="direct">

<div className="flex items-center justify-between flex-wrap gap-space-2xs border-b border-outline-variant/20 pb-2">
<div className="flex items-center gap-1.5">
<span className="w-6 h-6 rounded-full bg-surface-container-high text-primary flex items-center justify-center">
<span className="material-symbols-outlined text-[14px]">shop</span>
</span>
<span className="font-label-md text-xs text-on-surface font-bold">Google Play</span>
<span className="w-1 h-1 rounded-full bg-outline"></span>
<span className="font-body-sm text-xs text-on-surface-variant font-medium">Resolve Uncertainty</span>
</div>
<span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold tracking-wider uppercase bg-emerald-100 text-emerald-800 border border-emerald-300 flex items-center gap-1">
<span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
DIRECT EVIDENCE
</span>
</div>

<div className="relative pl-3.5 py-1">
<div className="absolute left-0 top-0 bottom-0 w-1 bg-emerald-600 rounded-full"></div>
<p className="font-medium text-slate-900 text-sm leading-relaxed">
“I have had 5 items saved in my wishlist for weeks. Every time a sale alert pops up, the actual discount doesn’t apply to the saved brands at checkout. Why notify if the deal is restricted?”
</p>
</div>

<div className="flex flex-wrap gap-1.5 pt-1">
<div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-100 border border-slate-200 text-xs">
<span className="text-tertiary font-medium">Primary Barrier:</span>
<span className="text-slate-900 font-semibold">Price / Value</span>
</div>
<div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-100 border border-slate-200 text-xs">
<span className="text-tertiary font-medium">Secondary Barrier:</span>
<span className="text-slate-900 font-semibold">Promotion Ambiguity</span>
</div>
</div>

<div className="flex items-center justify-between pt-1 border-t border-outline-variant/20">
<div className="flex items-center gap-1.5">
<span className="material-symbols-outlined text-[16px] text-emerald-700">trending_up</span>
<span className="font-label-sm text-xs text-on-surface-variant font-medium">Purchase Intent:</span>
<span className="font-code-sm text-xs text-slate-900 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">High</span>
</div>
<button aria-label="Bookmark record" className="text-tertiary hover:text-primary flex items-center p-1 rounded hover:bg-surface-container">
<span className="material-symbols-outlined text-[18px]">bookmark_border</span>
</button>
</div>
</div>

<div className="evidence-card bg-surface-container-lowest rounded-xl p-space-md shadow-sm border border-outline-variant/40 flex flex-col gap-space-sm transition-all" data-area="price" data-source="app-store" data-stage="revisit" data-type="direct">

<div className="flex items-center justify-between flex-wrap gap-space-2xs border-b border-outline-variant/20 pb-2">
<div className="flex items-center gap-1.5">
<span className="w-6 h-6 rounded-full bg-surface-container-high text-primary flex items-center justify-center">
<span className="material-symbols-outlined text-[14px]">file_download</span>
</span>
<span className="font-label-md text-xs text-on-surface font-bold">Apple App Store</span>
<span className="w-1 h-1 rounded-full bg-outline"></span>
<span className="font-body-sm text-xs text-on-surface-variant font-medium">Revisit</span>
</div>
<span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold tracking-wider uppercase bg-emerald-100 text-emerald-800 border border-emerald-300 flex items-center gap-1">
<span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
DIRECT EVIDENCE
</span>
</div>

<div className="relative pl-3.5 py-1">
<div className="absolute left-0 top-0 bottom-0 w-1 bg-emerald-600 rounded-full"></div>
<p className="font-medium text-slate-900 text-sm leading-relaxed">
“The price in the wishlist showed ₹1,299 but when clicking through to the product page it jumped to ₹1,899 without explanation. Kept it in wishlist hoping it reverts.”
</p>
</div>

<div className="flex flex-wrap gap-1.5 pt-1">
<div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-100 border border-slate-200 text-xs">
<span className="text-tertiary font-medium">Primary Barrier:</span>
<span className="text-slate-900 font-semibold">Price / Value</span>
</div>
<div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-100 border border-slate-200 text-xs">
<span className="text-tertiary font-medium">Secondary Barrier:</span>
<span className="text-slate-900 font-semibold">Price Fluctuations</span>
</div>
</div>

<div className="flex items-center justify-between pt-1 border-t border-outline-variant/20">
<div className="flex items-center gap-1.5">
<span className="material-symbols-outlined text-[16px] text-amber-600">swap_horiz</span>
<span className="font-label-sm text-xs text-on-surface-variant font-medium">Purchase Intent:</span>
<span className="font-code-sm text-xs text-slate-900 font-bold bg-amber-50 px-2 py-0.5 rounded border border-amber-200">Medium</span>
</div>
<button aria-label="Bookmark record" className="text-tertiary hover:text-primary flex items-center p-1 rounded hover:bg-surface-container">
<span className="material-symbols-outlined text-[18px]">bookmark_border</span>
</button>
</div>
</div>

<div className="evidence-card bg-surface-container-lowest rounded-xl p-space-md shadow-sm border border-outline-variant/40 flex flex-col gap-space-sm transition-all" data-area="other" data-source="youtube" data-stage="decide" data-type="direct">

<div className="flex items-center justify-between flex-wrap gap-space-2xs border-b border-outline-variant/20 pb-2">
<div className="flex items-center gap-1.5">
<span className="w-6 h-6 rounded-full bg-surface-container-high text-secondary flex items-center justify-center">
<span className="material-symbols-outlined text-[14px]">smart_display</span>
</span>
<span className="font-label-md text-xs text-on-surface font-bold">YouTube</span>
<span className="w-1 h-1 rounded-full bg-outline"></span>
<span className="font-body-sm text-xs text-on-surface-variant font-medium">Decide</span>
</div>
<span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold tracking-wider uppercase bg-emerald-100 text-emerald-800 border border-emerald-300 flex items-center gap-1">
<span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
DIRECT EVIDENCE
</span>
</div>

<div className="relative pl-3.5 py-1">
<div className="absolute left-0 top-0 bottom-0 w-1 bg-emerald-600 rounded-full"></div>
<p className="font-medium text-slate-900 text-sm leading-relaxed">
“Showed my wishlist haul in this vlog, but half the items were marked out of stock after being saved for just 2 days without any back-in-stock alert option.”
</p>
</div>

<div className="flex flex-wrap gap-1.5 pt-1">
<div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-100 border border-slate-200 text-xs">
<span className="text-tertiary font-medium">Primary Barrier:</span>
<span className="text-slate-900 font-semibold">Other / System Friction</span>
</div>
<div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-100 border border-slate-200 text-xs">
<span className="text-tertiary font-medium">Secondary Barrier:</span>
<span className="text-slate-900 font-semibold">Wishlist Management UX</span>
</div>
</div>

<div className="flex items-center justify-between pt-1 border-t border-outline-variant/20">
<div className="flex items-center gap-1.5">
<span className="material-symbols-outlined text-[16px] text-emerald-700">check_circle</span>
<span className="font-label-sm text-xs text-on-surface-variant font-medium">Purchase Intent:</span>
<span className="font-code-sm text-xs text-slate-900 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">High</span>
</div>
<button aria-label="Bookmark record" className="text-tertiary hover:text-primary flex items-center p-1 rounded hover:bg-surface-container">
<span className="material-symbols-outlined text-[18px]">bookmark_border</span>
</button>
</div>
</div>

<div className="evidence-card bg-surface-container-lowest rounded-xl p-space-md shadow-sm border border-outline-variant/40 flex flex-col gap-space-sm transition-all" data-area="quality" data-source="google-play" data-stage="evaluate" data-type="indirect">

<div className="flex items-center justify-between flex-wrap gap-space-2xs border-b border-outline-variant/20 pb-2">
<div className="flex items-center gap-1.5">
<span className="w-6 h-6 rounded-full bg-surface-container-high text-primary flex items-center justify-center">
<span className="material-symbols-outlined text-[14px]">shop</span>
</span>
<span className="font-label-md text-xs text-on-surface font-bold">Google Play</span>
<span className="w-1 h-1 rounded-full bg-outline"></span>
<span className="font-body-sm text-xs text-on-surface-variant font-medium">Evaluate</span>
</div>
<span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold tracking-wider uppercase bg-purple-100 text-purple-800 border border-purple-300 flex items-center gap-1">
<span className="w-1.5 h-1.5 rounded-full bg-purple-600"></span>
INDIRECT EVIDENCE
</span>
</div>

<div className="relative pl-3.5 py-1">
<div className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-full"></div>
<p className="font-medium text-slate-900 text-sm leading-relaxed">
“Comments on review videos frequently note hesitation to buy saved ethnic wear because fabric details and real lighting photos are missing on the app.”
</p>
</div>

<div className="flex flex-wrap gap-1.5 pt-1">
<div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-100 border border-slate-200 text-xs">
<span className="text-tertiary font-medium">Primary Barrier:</span>
<span className="text-slate-900 font-semibold">Quality / Authenticity</span>
</div>
<div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-100 border border-slate-200 text-xs">
<span className="text-tertiary font-medium">Secondary Barrier:</span>
<span className="text-slate-900 font-semibold">Catalog Representation</span>
</div>
</div>

<div className="flex items-center justify-between pt-1 border-t border-outline-variant/20">
<div className="flex items-center gap-1.5">
<span className="material-symbols-outlined text-[16px] text-blue-600">help_outline</span>
<span className="font-label-sm text-xs text-on-surface-variant font-medium">Purchase Intent:</span>
<span className="font-code-sm text-xs text-slate-900 font-bold bg-blue-50 px-2 py-0.5 rounded border border-blue-200">Moderate</span>
</div>
<button aria-label="Bookmark record" className="text-tertiary hover:text-primary flex items-center p-1 rounded hover:bg-surface-container">
<span className="material-symbols-outlined text-[18px]">bookmark_border</span>
</button>
</div>
</div>

<div className="evidence-card bg-surface-container-lowest rounded-xl p-space-md shadow-sm border border-outline-variant/40 flex flex-col gap-space-sm transition-all" data-area="fit" data-source="app-store" data-stage="uncertainty" data-type="indirect">

<div className="flex items-center justify-between flex-wrap gap-space-2xs border-b border-outline-variant/20 pb-2">
<div className="flex items-center gap-1.5">
<span className="w-6 h-6 rounded-full bg-surface-container-high text-primary flex items-center justify-center">
<span className="material-symbols-outlined text-[14px]">file_download</span>
</span>
<span className="font-label-md text-xs text-on-surface font-bold">Apple App Store</span>
<span className="w-1 h-1 rounded-full bg-outline"></span>
<span className="font-body-sm text-xs text-on-surface-variant font-medium">Resolve Uncertainty</span>
</div>
<span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold tracking-wider uppercase bg-purple-100 text-purple-800 border border-purple-300 flex items-center gap-1">
<span className="w-1.5 h-1.5 rounded-full bg-purple-600"></span>
INDIRECT EVIDENCE
</span>
</div>

<div className="relative pl-3.5 py-1">
<div className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-full"></div>
<p className="font-medium text-slate-900 text-sm leading-relaxed">
“Users discuss keeping footwear wishlisted while searching external forums to figure out if brand sizing runs small or true to UK size.”
</p>
</div>

<div className="flex flex-wrap gap-1.5 pt-1">
<div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-100 border border-slate-200 text-xs">
<span className="text-tertiary font-medium">Primary Barrier:</span>
<span className="text-slate-900 font-semibold">Fit / Size</span>
</div>
<div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-100 border border-slate-200 text-xs">
<span className="text-tertiary font-medium">Secondary Barrier:</span>
<span className="text-slate-900 font-semibold">Sizing Discrepancies</span>
</div>
</div>

<div className="flex items-center justify-between pt-1 border-t border-outline-variant/20">
<div className="flex items-center gap-1.5">
<span className="material-symbols-outlined text-[16px] text-blue-600">straighten</span>
<span className="font-label-sm text-xs text-on-surface-variant font-medium">Purchase Intent:</span>
<span className="font-code-sm text-xs text-slate-900 font-bold bg-blue-50 px-2 py-0.5 rounded border border-blue-200">Moderate</span>
</div>
<button aria-label="Bookmark record" className="text-tertiary hover:text-primary flex items-center p-1 rounded hover:bg-surface-container">
<span className="material-symbols-outlined text-[18px]">bookmark_border</span>
</button>
</div>
</div>

<div className="evidence-card bg-surface-container-lowest rounded-xl p-space-md shadow-sm border border-outline-variant/40 flex flex-col gap-space-sm transition-all" data-area="availability" data-source="google-play" data-stage="evaluate" data-type="indirect">

<div className="flex items-center justify-between flex-wrap gap-space-2xs border-b border-outline-variant/20 pb-2">
<div className="flex items-center gap-1.5">
<span className="w-6 h-6 rounded-full bg-surface-container-high text-primary flex items-center justify-center">
<span className="material-symbols-outlined text-[14px]">shop</span>
</span>
<span className="font-label-md text-xs text-on-surface font-bold">Google Play</span>
<span className="w-1 h-1 rounded-full bg-outline"></span>
<span className="font-body-sm text-xs text-on-surface-variant font-medium">Evaluate</span>
</div>
<span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold tracking-wider uppercase bg-purple-100 text-purple-800 border border-purple-300 flex items-center gap-1">
<span className="w-1.5 h-1.5 rounded-full bg-purple-600"></span>
INDIRECT EVIDENCE
</span>
</div>

<div className="relative pl-3.5 py-1">
<div className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-full"></div>
<p className="font-medium text-slate-900 text-sm leading-relaxed">
“Customers mention leaving products in wishlist because estimated delivery date to tier-2 pincodes fluctuates between 4 to 11 days.”
</p>
</div>

<div className="flex flex-wrap gap-1.5 pt-1">
<div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-100 border border-slate-200 text-xs">
<span className="text-tertiary font-medium">Primary Barrier:</span>
<span className="text-slate-900 font-semibold">Availability / Stock</span>
</div>
<div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-100 border border-slate-200 text-xs">
<span className="text-tertiary font-medium">Secondary Barrier:</span>
<span className="text-slate-900 font-semibold">Delivery Fulfilment</span>
</div>
</div>

<div className="flex items-center justify-between pt-1 border-t border-outline-variant/20">
<div className="flex items-center gap-1.5">
<span className="material-symbols-outlined text-[16px] text-emerald-700">local_shipping</span>
<span className="font-label-sm text-xs text-on-surface-variant font-medium">Purchase Intent:</span>
<span className="font-code-sm text-xs text-slate-900 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">High</span>
</div>
<button aria-label="Bookmark record" className="text-tertiary hover:text-primary flex items-center p-1 rounded hover:bg-surface-container">
<span className="material-symbols-outlined text-[18px]">bookmark_border</span>
</button>
</div>
</div>
</div>

<div className="px-space-base pt-space-lg pb-space-lg flex flex-col items-center gap-space-xs text-center">
<div className="w-10 h-10 rounded-full bg-surface-container-high flex items-center justify-center text-primary mb-1">
<span className="material-symbols-outlined text-[20px]">psychology</span>
</div>
<span className="font-label-md text-label-md text-on-surface font-semibold">Synthesizing 67 further observations</span>
<p className="font-body-sm text-body-sm text-on-surface-variant max-w-xs leading-relaxed">Cross-referencing behavioral patterns from Myntra app store feedback corpus.</p>
<div className="mt-4 p-3 bg-surface-container-low rounded-xl border border-outline-variant/30 text-xs text-slate-600 max-w-sm flex items-start gap-2 text-left">
<span className="material-symbols-outlined text-[18px] text-tertiary shrink-0 mt-0.5">policy</span>
<p className="leading-normal">
<strong className="text-slate-900 font-semibold">Methodology Note:</strong> Directional public conversation evidence. Does not establish business impact or causality.
</p>
</div>
</div>
</div>
</main><nav className="fixed bottom-0 w-full z-50 pb-safe bg-surface/95 backdrop-blur-xl border-t border-outline-variant/30 shadow-[0_-1px_8px_rgba(0,0,0,0.04)]" data-active-classes="text-primary font-medium"><div className="flex items-center justify-around h-16 px-space-xs"><a className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors" data-path="overview" href="#"><span className="material-symbols-outlined text-[20px]">dashboard</span><span className="font-label-sm text-label-sm">Overview</span></a><a className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors" data-path="discovery-copilot" href="#"><span className="material-symbols-outlined text-[20px]">smart_toy</span><span className="font-label-sm text-label-sm">Copilot</span></a><a className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors" data-path="opportunity-radar" href="#"><span className="material-symbols-outlined text-[20px]">radar</span><span className="font-label-sm text-label-sm">Radar</span></a><a aria-current="page" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 transition-colors text-primary font-semibold" data-path="evidence-explorer" href="#"><span className="material-symbols-outlined text-[20px]">folder_data</span><span className="font-label-sm text-label-sm">Evidence</span></a><a className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors" data-path="settings" href="#"><span className="material-symbols-outlined text-[20px]">settings</span><span className="font-label-sm text-label-sm">Settings</span></a></div></nav>
    </>
  );
}
