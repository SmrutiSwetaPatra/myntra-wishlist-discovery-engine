import React from 'react';
import { Link } from 'react-router-dom';
import { AlertTriangle, ArrowRight, Bot, Brain, ChevronRight, Eye, FolderOpen, Info, LayoutDashboard, Lightbulb, LineChart, Radar, Settings, User } from 'lucide-react';


export default function OpportunityRadar() {
  return (
    <>
<header className="fixed top-0 w-full z-50 pt-safe bg-surface/90 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.04)]"><div className="h-20 px-space-base flex flex-col justify-center gap-space-2xs"><div className="flex items-center justify-between"><div className="flex items-center gap-space-sm"><div className="flex flex-col"><div className="flex items-center gap-space-xs"><span className="font-title text-title text-on-surface tracking-tight leading-none">Wishlist Intelligence</span><span className="px-space-xs py-space-2xs rounded bg-surface-container-high text-primary font-code-sm text-code-sm uppercase font-medium">AI Engine</span></div><span className="font-body-sm text-body-sm text-on-surface-variant">AI Discovery Engine</span></div></div><div className="flex items-center gap-space-sm"><div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center"><User className="text-on-primary text-[18px]" /></div></div></div><div className="flex items-center justify-between"><div className="flex items-center gap-space-xs min-w-0"><span className="inline-block w-1.5 h-1.5 rounded-full bg-secondary shrink-0"></span><span className="font-label-sm text-label-sm text-on-surface-variant truncate">PM Fellowship / Myntra Discovery</span></div><div className="flex items-center gap-space-xs text-on-surface-variant shrink-0"><span className="font-code-sm text-code-sm text-on-surface-variant"><span className="text-primary font-medium">1,447</span> analyzed / <span className="text-secondary font-medium">73</span> established</span></div></div></div></header><main className="flex flex-col relative w-full pt-20 pb-28 bg-surface min-h-screen"><div className="flex flex-col w-full">

<div className="px-space-base pt-space-base pb-space-sm flex flex-col gap-space-sm">
<div className="flex flex-col gap-space-xs">
<div className="flex items-center justify-between">
<div className="flex items-center gap-space-xs">
<Radar className="text-primary text-[22px]" />
<h1 className="font-headline-sm text-headline-sm text-on-surface">Opportunity Radar</h1>
</div>
</div>
<div>
<span className="inline-flex items-center px-space-sm py-space-2xs rounded-full bg-surface-container-high text-primary font-code-sm text-code-sm font-medium tracking-tight">73 Established Records (6 Direct, 67 Indirect)</span>
</div>
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant">Compare recurring opportunity areas across the established evidence base.</p>
</div>

<div className="px-space-base pb-space-md">
<div className="p-space-md rounded-xl bg-surface-container-low flex items-start gap-space-sm shadow-sm border border-outline-variant/30">
<div className="p-space-2xs rounded bg-surface-container-highest text-secondary shrink-0 mt-0.5">
<Info className="text-[16px]" />
</div>
<div className="flex flex-col gap-space-2xs">
<span className="font-label-sm text-label-sm text-on-surface uppercase tracking-wide font-semibold">Methodology Guardrail</span>
<p className="font-body-sm text-body-sm text-on-surface-variant leading-relaxed">
          Evidence volume is a directional signal, not proof of business impact or causality. Opportunity areas are hypotheses requiring primary research and experimentation. Recurring opportunity areas identified in the analyzed pre-purchase evidence.
        </p>
</div>
</div>
</div>

<div className="px-space-base pb-space-lg">
<div className="p-space-base rounded-xl bg-surface-container-lowest shadow-sm flex flex-col gap-space-md border border-outline-variant/20">
<div className="flex items-center justify-between">
<div>
<span className="font-title text-title text-on-surface block">Quadrant Map</span>
<span className="font-body-sm text-body-sm text-on-surface-variant">Evidence Landscape — Not Causal Impact</span>
</div>
<div className="flex items-center gap-space-xs">
<button className="hidden px-space-xs py-space-2xs rounded bg-surface-container text-primary font-code-sm text-code-sm hover:bg-surface-container-high transition-colors" id="resetChartFilterBtn">Reset</button>
<LineChart className="text-on-surface-variant text-[18px]" />
</div>
</div>

<div className="relative w-full max-w-3xl mx-auto aspect-[16/10] sm:aspect-[16/9] max-h-[400px] bg-surface-container-low/60 rounded-lg p-space-sm overflow-hidden select-none flex items-center justify-center">
<svg aria-label="Evidence Landscape Scatter Plot" className="w-full h-full overflow-visible" preserveAspectRatio="xMidYMid meet" role="img" viewBox="0 0 360 230">

<rect className="text-primary/5" fill="currentColor" height="90" rx="4" width="150" x="190" y="20" />
<text className="fill-primary" style={{fontSize: "7px", fontWeight: "600"}} textAnchor="end" x="335" y="32">HIGH VOLUME / DIRECT</text>
<rect className="text-on-surface-variant/5" fill="currentColor" height="85" rx="4" width="150" x="40" y="110" />
<text className="fill-tertiary" style={{fontSize: "7px"}} textAnchor="start" x="45" y="190">LOWER VOLUME / INDIRECT</text>


<line className="text-outline-variant/40" stroke="currentColor" strokeDasharray="3,3" strokeWidth="1" x1="40" x2="340" y1="20" y2="20" />
<line className="text-outline-variant/40" stroke="currentColor" strokeDasharray="3,3" strokeWidth="1" x1="40" x2="340" y1="65" y2="65" />
<line className="text-outline-variant/60" stroke="currentColor" strokeDasharray="3,3" strokeWidth="1.5" x1="40" x2="340" y1="110" y2="110" />
<line className="text-outline-variant/40" stroke="currentColor" strokeDasharray="3,3" strokeWidth="1" x1="40" x2="340" y1="155" y2="155" />
<line className="text-outline-variant" stroke="currentColor" strokeWidth="1.5" x1="40" x2="340" y1="195" y2="195" />

<line className="text-outline-variant" stroke="currentColor" strokeWidth="1.5" x1="40" x2="40" y1="20" y2="195" />
<line className="text-outline-variant/60" stroke="currentColor" strokeDasharray="3,3" strokeWidth="1.5" x1="190" x2="190" y1="20" y2="195" />
<line className="text-outline-variant/40" stroke="currentColor" strokeWidth="1" x1="340" x2="340" y1="20" y2="195" />

<text className="fill-on-surface-variant" style={{fontSize: "7px"}} textAnchor="end" x="35" y="23">4</text>
<text className="fill-on-surface-variant" style={{fontSize: "7px"}} textAnchor="end" x="35" y="68">3</text>
<text className="fill-on-surface-variant" style={{fontSize: "7px"}} textAnchor="end" x="35" y="113">2</text>
<text className="fill-on-surface-variant" style={{fontSize: "7px"}} textAnchor="end" x="35" y="158">1</text>
<text className="fill-on-surface-variant" style={{fontSize: "7px"}} textAnchor="end" x="35" y="198">0</text>
<text className="fill-on-surface-variant" style={{fontSize: "7px"}} textAnchor="middle" x="40" y="210">0</text>
<text className="fill-on-surface-variant" style={{fontSize: "7px"}} textAnchor="middle" x="190" y="210">12.5</text>
<text className="fill-on-surface-variant" style={{fontSize: "7px"}} textAnchor="middle" x="340" y="210">25</text>

<text className="fill-tertiary" style={{fontSize: "7px", letterSpacing: "0.04em"}} textAnchor="middle" x="190" y="224">TOTAL EVIDENCE VOLUME →</text>
<text className="fill-tertiary" style={{fontSize: "7px", letterSpacing: "0.04em"}} textAnchor="middle" transform="rotate(-90)" x="-105" y="14">DIRECT EVIDENCE COUNT →</text>


<g className="cursor-pointer transition-transform duration-200 hover:scale-110 active:scale-95">
<circle className="text-primary/20" cx="320" cy="85" fill="currentColor" r="15" />
<circle className="text-primary" cx="320" cy="85" fill="currentColor" r="10" />
<text fill="#ffffff" style={{fontSize: "8px", fontWeight: "600"}} textAnchor="middle" x="320" y="88.5">24</text>
<text className="fill-on-surface" style={{fontSize: "7px", fontWeight: "600"}} textAnchor="middle" x="320" y="65">Other / Friction</text>
</g>


<g className="cursor-pointer transition-transform duration-200 hover:scale-110 active:scale-95">
<circle className="text-secondary/20" cx="260" cy="85" fill="currentColor" r="14" />
<circle className="text-secondary" cx="260" cy="85" fill="currentColor" r="9.5" />
<text fill="#ffffff" style={{fontSize: "8px", fontWeight: "600"}} textAnchor="middle" x="260" y="88.5">19</text>
<text className="fill-secondary" style={{fontSize: "7px", fontWeight: "600"}} textAnchor="middle" x="260" y="66">Price / Value</text>
</g>


<g className="cursor-pointer transition-transform duration-200 hover:scale-110 active:scale-95">
<circle className="text-tertiary-container/40" cx="220" cy="180" fill="currentColor" r="12" />
<circle className="text-tertiary-container" cx="220" cy="180" fill="currentColor" r="8" />
<text fill="#ffffff" style={{fontSize: "7px", fontWeight: "600"}} textAnchor="middle" x="220" y="182.5">15</text>
<text className="fill-on-surface" style={{fontSize: "7px", fontWeight: "600"}} textAnchor="middle" x="220" y="164">Quality / Auth.</text>
</g>


<g className="cursor-pointer transition-transform duration-200 hover:scale-110 active:scale-95">
<circle className="text-tertiary/30" cx="160" cy="182" fill="currentColor" r="11" />
<circle className="text-tertiary" cx="160" cy="182" fill="currentColor" r="7.5" />
<text fill="#ffffff" style={{fontSize: "7px", fontWeight: "600"}} textAnchor="middle" x="160" y="184.5">10</text>
<text className="fill-on-surface-variant" style={{fontSize: "7px", fontWeight: "600"}} textAnchor="middle" x="160" y="167">Availability</text>
</g>


<g className="cursor-pointer transition-transform duration-200 hover:scale-110 active:scale-95">
<circle className="text-outline-variant/50" cx="100" cy="184" fill="currentColor" r="10" />
<circle className="text-outline" cx="100" cy="184" fill="currentColor" r="7" />
<text fill="#ffffff" style={{fontSize: "7px", fontWeight: "600"}} textAnchor="middle" x="100" y="186.5">5</text>
<text className="fill-on-surface-variant" style={{fontSize: "7px", fontWeight: "600"}} textAnchor="middle" x="100" y="170">Fit / Size</text>
</g>
</svg>
</div>

<div className="flex flex-col gap-space-xs pt-space-xs">
<div className="text-label-sm font-label-sm text-on-surface-variant pb-space-2xs uppercase tracking-wider">Exact Category Breakdown</div>
<div className="grid grid-cols-1 sm:grid-cols-2 gap-space-xs">
<Link to="/evidence?area=other" className="flex items-center justify-between p-space-xs rounded-lg bg-surface-container-low hover:bg-surface-container transition-colors text-left group">
<div className="flex items-center gap-space-xs min-w-0">
<span className="w-2.5 h-2.5 rounded-full bg-primary shrink-0 group-hover:scale-110 transition-transform"></span>
<span className="font-label-sm text-label-sm text-on-surface truncate group-hover:text-primary transition-colors">Other / System Friction</span>
</div>
<span className="font-code-sm text-code-sm text-on-surface-variant shrink-0 ml-space-xs">24 total (3 Direct, 21 Indirect)</span>
</Link>
<Link to="/evidence?area=price" className="flex items-center justify-between p-space-xs rounded-lg bg-surface-container-low hover:bg-surface-container transition-colors text-left group">
<div className="flex items-center gap-space-xs min-w-0">
<span className="w-2.5 h-2.5 rounded-full bg-secondary shrink-0 group-hover:scale-110 transition-transform"></span>
<span className="font-label-sm text-label-sm text-on-surface truncate group-hover:text-secondary transition-colors">Price / Value</span>
</div>
<span className="font-code-sm text-code-sm text-on-surface-variant shrink-0 ml-space-xs">19 total (3 Direct, 16 Indirect)</span>
</Link>
<Link to="/evidence?area=quality" className="flex items-center justify-between p-space-xs rounded-lg bg-surface-container-low hover:bg-surface-container transition-colors text-left group">
<div className="flex items-center gap-space-xs min-w-0">
<span className="w-2.5 h-2.5 rounded-full bg-tertiary-container shrink-0 group-hover:scale-110 transition-transform"></span>
<span className="font-label-sm text-label-sm text-on-surface truncate group-hover:text-tertiary-container transition-colors">Quality / Authenticity</span>
</div>
<span className="font-code-sm text-code-sm text-on-surface-variant shrink-0 ml-space-xs">15 total (0 Direct, 15 Indirect)</span>
</Link>
<Link to="/evidence?area=availability" className="flex items-center justify-between p-space-xs rounded-lg bg-surface-container-low hover:bg-surface-container transition-colors text-left group">
<div className="flex items-center gap-space-xs min-w-0">
<span className="w-2.5 h-2.5 rounded-full bg-tertiary shrink-0 group-hover:scale-110 transition-transform"></span>
<span className="font-label-sm text-label-sm text-on-surface truncate group-hover:text-tertiary transition-colors">Availability / Stock</span>
</div>
<span className="font-code-sm text-code-sm text-on-surface-variant shrink-0 ml-space-xs">10 total (0 Direct, 10 Indirect)</span>
</Link>
<Link to="/evidence?area=fit" className="flex items-center justify-between p-space-xs rounded-lg bg-surface-container-low hover:bg-surface-container transition-colors text-left sm:col-span-2 group">
<div className="flex items-center gap-space-xs min-w-0">
<span className="w-2.5 h-2.5 rounded-full bg-outline shrink-0 group-hover:scale-110 transition-transform"></span>
<span className="font-label-sm text-label-sm text-on-surface truncate group-hover:text-outline transition-colors">Fit / Size</span>
</div>
<span className="font-code-sm text-code-sm text-on-surface-variant shrink-0 ml-space-xs">5 total (0 Direct, 5 Indirect)</span>
</Link>
</div>
</div>
</div>
</div>

<div className="px-space-base pb-space-lg flex flex-col gap-space-md">
<div className="flex items-center justify-between flex-wrap">
<h2 className="font-title text-title text-on-surface">Opportunity Clusters</h2>
<span className="font-code-sm text-code-sm text-on-surface-variant">5 recurring opportunity areas identified in the analyzed pre-purchase evidence</span>
</div>

<div className="p-space-base rounded-xl bg-surface-container-lowest shadow-sm flex flex-col gap-space-sm transition-all duration-300 border border-outline-variant/20" id="card-other">
<div className="flex items-start justify-between gap-space-sm">
<div className="flex flex-col min-w-0">
<div className="flex items-center gap-space-xs">
<span className="w-2 h-2 rounded-full bg-primary shrink-0"></span>
<span className="font-headline-sm text-headline-sm text-on-surface truncate">Other / System Friction</span>
</div>
<span className="font-code-sm text-code-sm text-on-surface-variant mt-space-2xs">24 Established Records (3 Direct, 21 Indirect)</span>
</div>
<span className="px-space-xs py-space-2xs rounded bg-surface-container-high text-primary font-label-sm text-label-sm uppercase tracking-wider shrink-0 font-medium">Heterogeneous</span>
</div>

<div className="w-full h-1.5 rounded-full bg-surface-container overflow-hidden flex">
<div className="h-full bg-primary" style={{width: "12.5%"}}></div>
<div className="h-full bg-primary-fixed-dim" style={{width: "87.5%"}}></div>
</div>
<div className="flex flex-col gap-space-xs mt-space-xs">
<div className="p-space-sm rounded-lg bg-surface-container-low">
<span className="font-label-sm text-label-sm text-primary uppercase block font-semibold">Unmet Need</span>
<p className="font-body-md text-body-md text-on-surface mt-space-2xs">Mixed platform, service, returns, support, and wishlist-related friction requiring further validation and sub-theme analysis.</p>
</div>
<div className="p-space-sm rounded-lg bg-surface-container-high/60">
<span className="font-label-sm text-label-sm text-secondary uppercase block font-semibold flex items-center gap-1">
<AlertTriangle className="text-[14px]" /> Evidence Limitation
          </span>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">Mixed themes — requires sub-theme validation. Cannot be treated as a single root cause.</p>
</div>
</div>
<div className="pt-space-xs flex items-center justify-between">
<span className="font-code-sm text-code-sm text-tertiary">3 Direct Evidence, 21 Indirect</span>
<Link to="/evidence" className="px-space-md py-space-xs rounded bg-primary text-on-primary font-label-sm text-label-sm flex items-center gap-space-xs hover:bg-primary-container active:scale-95 transition-all shadow-sm">
<span className="">Explore 24 Records</span>
<ArrowRight className="text-[16px]" />
</Link>
</div>
</div>

<div className="p-space-base rounded-xl bg-surface-container-lowest shadow-sm flex flex-col gap-space-sm transition-all duration-300 border border-outline-variant/20" id="card-price">
<div className="flex items-start justify-between gap-space-sm">
<div className="flex flex-col min-w-0">
<div className="flex items-center gap-space-xs">
<span className="w-2 h-2 rounded-full bg-secondary shrink-0"></span>
<span className="font-headline-sm text-headline-sm text-on-surface truncate">Price / Value</span>
</div>
<span className="font-code-sm text-code-sm text-on-surface-variant mt-space-2xs">19 Established Records (3 Direct, 16 Indirect)</span>
</div>
<span className="px-space-xs py-space-2xs rounded bg-secondary-fixed text-on-secondary-fixed font-label-sm text-label-sm uppercase tracking-wider shrink-0 font-medium">Direct + Indirect Evidence</span>
</div>

<div className="w-full h-1.5 rounded-full bg-surface-container overflow-hidden flex">
<div className="h-full bg-secondary" style={{width: "15.8%"}}></div>
<div className="h-full bg-secondary-fixed-dim" style={{width: "84.2%"}}></div>
</div>
<div className="flex flex-col gap-space-xs mt-space-xs">
<div className="p-space-sm rounded-lg bg-surface-container-low">
<span className="font-label-sm text-label-sm text-secondary uppercase block font-semibold">Evidence Signal</span>
<p className="font-body-md text-body-md text-on-surface mt-space-2xs">Recurring price and promotion uncertainty appears across the established evidence base.</p>
</div>
<div className="p-space-sm rounded-lg bg-surface-container-low">
<span className="font-label-sm text-label-sm text-on-surface uppercase block font-semibold">Unmet Need</span>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">Transparent deal timing, coupon clarity, and protection against price fluctuation while items remain saved.</p>
</div>
<div className="p-space-sm rounded-lg bg-surface-container-high/60">
<span className="font-label-sm text-label-sm text-primary uppercase block font-semibold flex items-center gap-1">
<Lightbulb className="text-[14px]" /> Hypothesis
          </span>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">Improving price and promotion transparency may reduce hesitation during consideration (Hypothesis — requires primary research and experimentation before being treated as a conversion driver).</p>
</div>
</div>
<div className="pt-space-xs flex items-center justify-between">
<span className="font-code-sm text-code-sm text-tertiary">3 Direct Evidence, 16 Indirect</span>
<Link to="/evidence" className="px-space-md py-space-xs rounded bg-secondary text-on-secondary font-label-sm text-label-sm flex items-center gap-space-xs hover:bg-secondary-container active:scale-95 transition-all shadow-sm">
<span className="">View Opportunity Detail</span>
<Eye className="text-[16px]" />
</Link>
</div>
</div>

<div className="p-space-base rounded-xl bg-surface-container-lowest shadow-sm flex flex-col gap-space-sm transition-all duration-300 border border-outline-variant/20" id="card-quality">
<div className="flex items-start justify-between gap-space-sm">
<div className="flex flex-col min-w-0">
<div className="flex items-center gap-space-xs">
<span className="w-2 h-2 rounded-full bg-tertiary-container shrink-0"></span>
<span className="font-headline-sm text-headline-sm text-on-surface truncate">Quality / Authenticity</span>
</div>
<span className="font-code-sm text-code-sm text-on-surface-variant mt-space-2xs">15 Established Records (0 Direct, 15 Indirect)</span>
</div>
<span className="px-space-xs py-space-2xs rounded bg-surface-container-high text-tertiary font-label-sm text-label-sm uppercase tracking-wider shrink-0 font-medium">Indirect Evidence Only</span>
</div>

<div className="w-full h-1.5 rounded-full bg-surface-container overflow-hidden flex">
<div className="h-full bg-tertiary-container" style={{width: "100%"}}></div>
</div>
<div className="flex flex-col gap-space-xs mt-space-xs">
<div className="p-space-sm rounded-lg bg-surface-container-low">
<span className="font-label-sm text-label-sm text-tertiary uppercase block font-semibold">Evidence Signal</span>
<p className="font-body-md text-body-md text-on-surface mt-space-2xs">Recurring concerns relate to product quality, authenticity, durability, and differences between catalog representation and received-product expectations.</p>
</div>
<div className="p-space-sm rounded-lg bg-surface-container-high/60">
<span className="font-label-sm text-label-sm text-primary uppercase block font-semibold flex items-center gap-1">
<Lightbulb className="text-[14px]" /> Hypothesis
          </span>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">Stronger product representation, quality signals, and authenticity reassurance may increase confidence in saved products (Hypothesis — requires primary research and experimentation before being treated as a conversion driver).</p>
</div>
</div>
<div className="pt-space-xs flex items-center justify-between">
<span className="font-code-sm text-code-sm text-tertiary">0 Direct Evidence, 15 Indirect</span>
<Link to="/evidence" className="px-space-md py-space-xs rounded bg-surface-container text-on-surface font-label-sm text-label-sm flex items-center gap-space-xs hover:bg-surface-container-high active:scale-95 transition-all">
<span className="">Explore 15 Records</span>
<ArrowRight className="text-[16px]" />
</Link>
</div>
</div>

<div className="p-space-base rounded-xl bg-surface-container-lowest shadow-sm flex flex-col gap-space-sm transition-all duration-300 border border-outline-variant/20" id="card-avail">
<div className="flex items-start justify-between gap-space-sm">
<div className="flex flex-col min-w-0">
<div className="flex items-center gap-space-xs">
<span className="w-2 h-2 rounded-full bg-tertiary shrink-0"></span>
<span className="font-headline-sm text-headline-sm text-on-surface truncate">Availability / Stock</span>
</div>
<span className="font-code-sm text-code-sm text-on-surface-variant mt-space-2xs">10 Established Records (0 Direct, 10 Indirect)</span>
</div>
<span className="px-space-xs py-space-2xs rounded bg-surface-container-high text-tertiary font-label-sm text-label-sm uppercase tracking-wider shrink-0 font-medium">Indirect Evidence Only</span>
</div>

<div className="w-full h-1.5 rounded-full bg-surface-container overflow-hidden flex">
<div className="h-full bg-tertiary" style={{width: "100%"}}></div>
</div>
<div className="flex flex-col gap-space-xs mt-space-xs">
<div className="p-space-sm rounded-lg bg-surface-container-low">
<span className="font-label-sm text-label-sm text-tertiary uppercase block font-semibold">Evidence Signal</span>
<p className="font-body-md text-body-md text-on-surface mt-space-2xs">Recurring signals relate to stock availability, size depletion, delivery reliability, and uncertainty around fulfillment.</p>
</div>
<div className="p-space-sm rounded-lg bg-surface-container-high/60">
<span className="font-label-sm text-label-sm text-primary uppercase block font-semibold flex items-center gap-1">
<Lightbulb className="text-[14px]" /> Hypothesis
          </span>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">More reliable availability and delivery information may reduce abandonment during consideration (Hypothesis — requires primary research and experimentation before being treated as a conversion driver).</p>
</div>
</div>
<div className="pt-space-xs flex items-center justify-between">
<span className="font-code-sm text-code-sm text-tertiary">0 Direct Evidence, 10 Indirect</span>
<Link to="/evidence" className="px-space-md py-space-xs rounded bg-surface-container text-on-surface font-label-sm text-label-sm flex items-center gap-space-xs hover:bg-surface-container-high active:scale-95 transition-all">
<span className="">Explore 10 Records</span>
<ArrowRight className="text-[16px]" />
</Link>
</div>
</div>

<div className="p-space-base rounded-xl bg-surface-container-lowest shadow-sm flex flex-col gap-space-sm transition-all duration-300 border border-outline-variant/20" id="card-fit">
<div className="flex items-start justify-between gap-space-sm">
<div className="flex flex-col min-w-0">
<div className="flex items-center gap-space-xs">
<span className="w-2 h-2 rounded-full bg-outline shrink-0"></span>
<span className="font-headline-sm text-headline-sm text-on-surface truncate">Fit / Size</span>
</div>
<span className="font-code-sm text-code-sm text-on-surface-variant mt-space-2xs">5 Established Records (0 Direct, 5 Indirect)</span>
</div>
<span className="px-space-xs py-space-2xs rounded bg-surface-container text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wider shrink-0 font-medium">Emerging Evidence Signal</span>
</div>

<div className="w-full h-1.5 rounded-full bg-surface-container overflow-hidden flex">
<div className="h-full bg-outline" style={{width: "100%"}}></div>
</div>
<div className="flex flex-col gap-space-xs mt-space-xs">
<div className="p-space-sm rounded-lg bg-surface-container-low">
<span className="font-label-sm text-label-sm text-on-surface-variant uppercase block font-semibold">Evidence Signal</span>
<p className="font-body-md text-body-md text-on-surface mt-space-2xs">Smaller-volume signals relate to sizing consistency, measurement uncertainty, and return-related confidence.</p>
</div>
<div className="p-space-sm rounded-lg bg-surface-container-high/60">
<span className="font-label-sm text-label-sm text-primary uppercase block font-semibold flex items-center gap-1">
<Lightbulb className="text-[14px]" /> Hypothesis
          </span>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">Better sizing confidence may reduce hesitation before purchasing saved apparel (Hypothesis — requires primary research and experimentation before being treated as a conversion driver).</p>
</div>
</div>
<div className="pt-space-xs flex items-center justify-between">
<span className="font-code-sm text-code-sm text-tertiary">0 Direct Evidence, 5 Indirect</span>
<Link to="/evidence" className="px-space-md py-space-xs rounded bg-surface-container text-on-surface font-label-sm text-label-sm flex items-center gap-space-xs hover:bg-surface-container-high active:scale-95 transition-all">
<span className="">Explore 5 Records</span>
<ArrowRight className="text-[16px]" />
</Link>
</div>
</div>
</div>

<div className="px-space-base pb-space-lg">
<div className="p-space-md rounded-xl bg-surface-container flex items-center justify-between gap-space-sm flex-wrap">
<div className="flex items-center gap-space-sm">
<div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
<Brain className="text-primary text-[18px]" />
</div>
<span className="font-body-sm text-body-sm text-on-surface">Need deeper cluster breakdown? Run discovery copilot analysis.</span>
</div>
<ChevronRight className="text-on-surface-variant text-[20px] shrink-0" />
</div>
</div>
</div>
</main><nav className="fixed bottom-0 w-full z-50 pb-safe bg-surface/90 backdrop-blur-xl shadow-[0_-1px_8px_rgba(0,0,0,0.04)]" data-active-classes="text-primary font-medium"><div className="flex items-center justify-around h-16 px-space-xs"><Link to="/"  className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors"  ><LayoutDashboard className="text-[20px]" /><span className="font-label-sm text-label-sm">Overview</span></Link><Link to="/copilot"  className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors"  ><Bot className="text-[20px]" /><span className="font-label-sm text-label-sm">Copilot</span></Link><Link to="/radar"  aria-current="page" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 transition-colors text-primary font-medium"  ><Radar className="text-[20px]" /><span className="font-label-sm text-label-sm">Radar</span></Link><Link to="/evidence"  className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors"  ><FolderOpen className="text-[20px]" /><span className="font-label-sm text-label-sm">Evidence</span></Link><Link to="/settings"  className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors"  ><Settings className="text-[20px]" /><span className="font-label-sm text-label-sm">Settings</span></Link></div></nav>
    </>
  );
}
