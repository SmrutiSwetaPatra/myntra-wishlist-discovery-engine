import React from 'react';
import { Link } from 'react-router-dom';
import { AlertTriangle, Archive, Bot, Brain, CheckCircle, ChevronRight, Database, FlaskConical, FolderOpen, Heart, LayoutDashboard, MessageSquare, Network, Radar, Settings, Tag, User } from 'lucide-react';


export default function Overview() {
  return (
    <>
<header className="fixed top-0 w-full z-50 pt-safe bg-surface/90 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.04)] border-b border-surface-container">
<div className="py-2.5 px-space-base flex flex-col justify-center gap-1">
<div className="flex items-center justify-between">
<div className="flex flex-col">
<div className="flex items-center gap-space-xs">
<span className="font-title text-title text-on-surface tracking-tight leading-none">Wishlist Intelligence</span>
<span className="px-space-xs py-0.5 rounded bg-surface-container-high text-primary font-code-sm text-code-sm uppercase font-medium">AI Discovery Engine</span>
</div>
<span className="font-body-sm text-body-sm text-on-surface-variant">Research workspace for wishlist-to-purchase discovery</span>
</div>
<div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center shrink-0">
<User className="text-on-primary text-[18px]" />
</div>
</div>
<div className="flex items-center justify-between pt-0.5 border-t border-surface-container/60">
<div className="flex items-center gap-1.5 min-w-0">
<span className="inline-block w-1.5 h-1.5 rounded-full bg-secondary shrink-0"></span>
<span className="font-label-sm text-label-sm text-on-surface-variant truncate">PM Fellowship / Myntra Discovery</span>
</div>
<div className="flex items-center gap-space-xs text-on-surface-variant shrink-0">
<span className="font-code-sm text-code-sm text-on-surface-variant">
<span className="text-primary font-semibold">1,447</span> analyzed / <span className="text-secondary font-semibold">72</span> established
          </span>
</div>
</div>
</div>
</header>

<main className="flex flex-col relative w-full pt-24 pb-28 bg-surface min-h-screen">
<div className="flex flex-col w-full px-space-base gap-space-lg">

<div className="bg-surface-container-low rounded-xl p-space-lg flex flex-col gap-space-md shadow-sm relative overflow-hidden">
<div className="absolute -right-8 -bottom-8 w-36 h-36 rounded-full bg-primary-fixed-dim/30 pointer-events-none blur-2xl"></div>
<div className="flex items-center gap-space-xs self-start">
<span className="px-space-sm py-space-2xs rounded-full bg-surface-container-high text-primary font-label-sm text-label-sm font-medium">
            Product Research Workspace • PM Fellowship
          </span>
</div>
<div className="flex flex-col gap-space-xs">
<h2 className="font-headline-lg-mobile text-headline-lg-mobile text-on-surface tracking-tight">
            Understand what stands between wishlist and purchase.
          </h2>
<p className="font-body-md text-body-md text-on-surface-variant leading-relaxed">
            Explore public user conversations, uncover recurring barriers, and identify evidence-backed opportunities across the shopper decision journey.
          </p>
</div>
<div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-space-sm pt-space-xs">
<Link to="/copilot"  className="h-10 px-space-md bg-primary hover:bg-primary-container text-on-primary rounded-lg font-label-md text-label-md flex items-center justify-center gap-space-xs shadow-sm transition-colors active:scale-[0.99]"  >
<Bot className="text-[18px]" />
<span className="">Ask Discovery Copilot</span>
</Link>
<Link to="/radar"  className="h-10 px-space-md bg-surface-container hover:bg-surface-container-high text-on-surface rounded-lg font-label-md text-label-md flex items-center justify-center gap-space-xs transition-colors active:scale-[0.99]"  >
<Radar className="text-[18px]" />
<span className="">Explore Opportunity Radar</span>
</Link>
</div>
</div>

<div className="flex flex-col gap-space-sm">
<div className="flex items-center justify-between">
<div className="flex items-center gap-space-xs">
<Database className="text-primary text-[20px]" />
<h3 className="font-title text-title text-on-surface">Discovery Engine Dataset</h3>
</div>
<span className="font-code-sm text-code-sm text-on-surface-variant bg-surface-container-low px-2 py-0.5 rounded text-right">
            Verified Dataset
          </span>
</div>
<div className="text-xs text-on-surface-variant -mt-1 flex items-center gap-1">
<FlaskConical className="text-[15px] text-tertiary" />
<span className="">Research corpus: Google Play · Apple App Store · YouTube</span>
</div>

<div className="grid grid-cols-1 sm:grid-cols-2 gap-space-sm">

<div className="bg-surface-container-lowest rounded-xl p-space-md flex flex-col justify-between shadow-sm relative overflow-hidden border border-surface-container/60">
<div className="flex flex-col">
<div className="flex items-center justify-between">
<span className="font-label-sm text-label-sm text-on-surface-variant font-medium">Public conversations analyzed</span>
<MessageSquare className="text-primary text-[18px]" />
</div>
<div className="font-headline-md text-headline-md text-on-surface mt-space-xs font-bold">1,447</div>
<span className="font-body-sm text-body-sm text-on-surface-variant">Standardized multi-source public conversations</span>
</div>
<div className="mt-space-md bg-surface-container-low rounded-lg p-2.5 flex flex-col gap-1.5">
<div className="flex justify-between items-center text-on-surface-variant font-code-sm text-code-sm">
<span className="">Google Play:</span>
<span className="font-semibold text-on-surface">500</span>
</div>
<div className="flex justify-between items-center text-on-surface-variant font-code-sm text-code-sm">
<span className="">Apple App Store:</span>
<span className="font-semibold text-on-surface">500</span>
</div>
<div className="flex justify-between items-center text-on-surface-variant font-code-sm text-code-sm">
<span className="">YouTube:</span>
<span className="font-semibold text-on-surface">447</span>
</div>
<div className="flex justify-between items-center text-on-surface-variant/70 font-code-sm text-code-sm pt-0.5 border-t border-surface-container">
<span className="">Reddit:</span>
<span className="text-tertiary">0 (Excluded)</span>
</div>
</div>
</div>

<div className="bg-surface-container-lowest rounded-xl p-space-md flex flex-col justify-between shadow-sm relative overflow-hidden border border-surface-container/60">
<div className="flex flex-col">
<div className="flex items-center justify-between">
<span className="font-label-sm text-label-sm text-secondary font-medium">Established pre-purchase evidence</span>
<span className="px-space-xs py-0.5 rounded bg-secondary-fixed text-on-secondary-fixed font-code-sm text-code-sm font-semibold">Verified Signals</span>
</div>
<div className="font-headline-md text-headline-md text-secondary mt-space-xs font-bold">72</div>
<span className="font-body-sm text-body-sm text-on-surface-variant">Pre-purchase barrier signals qualified</span>
</div>
<div className="mt-space-md flex flex-col gap-space-xs">
<div className="flex items-center justify-between p-2 rounded bg-surface-container-low">
<div className="flex items-center gap-space-xs">
<span className="w-2 h-2 rounded-full bg-primary"></span>
<span className="font-body-sm text-body-sm text-on-surface font-medium">Direct Evidence</span>
</div>
<span className="font-code-sm text-code-sm text-on-surface font-semibold">6</span>
</div>
<div className="flex items-center justify-between p-2 rounded bg-surface-container-low">
<div className="flex items-center gap-space-xs">
<span className="w-2 h-2 rounded-full bg-secondary"></span>
<span className="font-body-sm text-body-sm text-on-surface font-medium">Indirect Evidence</span>
</div>
<span className="font-code-sm text-code-sm text-on-surface font-semibold">66</span>
</div>
</div>
</div>
</div>

<div className="bg-surface-container-lowest rounded-xl p-space-md shadow-sm flex flex-col gap-space-xs border border-surface-container/60">
<span className="font-label-sm text-label-sm text-on-surface-variant font-medium">Corpus Pipeline Classification Outcomes</span>
<div className="grid grid-cols-3 gap-space-xs pt-space-2xs">
<div className="bg-surface-container-low p-2 rounded flex flex-col">
<span className="font-body-sm text-body-sm text-tertiary">Needs Validation</span>
<span className="font-title text-title text-on-surface mt-0.5 font-bold">23</span>
</div>
<div className="bg-surface-container-low p-2 rounded flex flex-col">
<span className="font-body-sm text-body-sm text-tertiary">Excluded</span>
<span className="font-title text-title text-on-surface mt-0.5 font-bold">920</span>
</div>
<div className="bg-surface-container-low p-2 rounded flex flex-col">
<span className="font-body-sm text-body-sm text-tertiary">Processing Error</span>
<span className="font-title text-title text-error mt-0.5 font-bold">1</span>
</div>
</div>
</div>
</div>

<div className="flex flex-col gap-space-sm">
<div className="flex flex-col">
<h3 className="font-title text-title text-on-surface">Core Shopper Decision Journey</h3>
<p className="font-body-sm text-body-sm text-on-surface-variant">Six progression gates from initial discovery to final checkout</p>
</div>

<div className="flex gap-space-xs overflow-x-auto pb-space-xs snap-x">
<Link to="/evidence?stage=save" className="min-w-[140px] bg-surface-container-lowest rounded-lg p-space-sm flex flex-col gap-1 shadow-sm snap-start shrink-0 border border-surface-container/60 hover:border-primary/40 hover:bg-surface-container-low transition-colors">
<span className="font-code-sm text-code-sm text-primary font-semibold">Gate 01</span>
<span className="font-label-md text-label-md text-on-surface font-semibold">Save</span>
<span className="font-body-sm text-body-sm text-on-surface-variant">Intent anchor</span>
</Link>
<Link to="/evidence?stage=revisit" className="min-w-[140px] bg-surface-container-lowest rounded-lg p-space-sm flex flex-col gap-1 shadow-sm snap-start shrink-0 border border-surface-container/60 hover:border-primary/40 hover:bg-surface-container-low transition-colors">
<span className="font-code-sm text-code-sm text-primary font-semibold">Gate 02</span>
<span className="font-label-md text-label-md text-on-surface font-semibold">Revisit</span>
<span className="font-body-sm text-body-sm text-on-surface-variant">Passive retrieval</span>
</Link>
<Link to="/evidence?stage=evaluate" className="min-w-[140px] bg-surface-container-lowest rounded-lg p-space-sm flex flex-col gap-1 shadow-sm snap-start shrink-0 border border-surface-container/60 hover:border-primary/40 hover:bg-surface-container-low transition-colors">
<span className="font-code-sm text-code-sm text-primary font-semibold">Gate 03</span>
<span className="font-label-md text-label-md text-on-surface font-semibold">Evaluate</span>
<span className="font-body-sm text-body-sm text-on-surface-variant">Attribute scrutiny</span>
</Link>
<Link to="/evidence?stage=uncertainty" className="min-w-[155px] bg-surface-container-lowest rounded-lg p-space-sm flex flex-col gap-1 shadow-sm snap-start shrink-0 border border-secondary/30 bg-secondary-fixed/10 hover:border-secondary/60 transition-colors">
<span className="font-code-sm text-code-sm text-secondary font-semibold">Gate 04</span>
<span className="font-label-md text-label-md text-on-surface font-semibold">Resolve Uncertainty</span>
<span className="font-body-sm text-body-sm text-secondary font-medium">Critical drop-off</span>
</Link>
<Link to="/evidence?stage=decide" className="min-w-[140px] bg-surface-container-lowest rounded-lg p-space-sm flex flex-col gap-1 shadow-sm snap-start shrink-0 border border-surface-container/60 hover:border-primary/40 hover:bg-surface-container-low transition-colors">
<span className="font-code-sm text-code-sm text-primary font-semibold">Gate 05</span>
<span className="font-label-md text-label-md text-on-surface font-semibold">Decide</span>
<span className="font-body-sm text-body-sm text-on-surface-variant">Trade-off balancing</span>
</Link>
<div className="min-w-[140px] bg-surface-container-lowest/50 rounded-lg p-space-sm flex flex-col gap-1 border border-surface-container/30 border-dashed snap-start shrink-0 opacity-70">
<span className="font-code-sm text-code-sm text-tertiary font-semibold">Outcome</span>
<span className="font-label-md text-label-md text-on-surface font-semibold">Purchase</span>
<span className="font-body-sm text-body-sm text-on-surface-variant">Cart transition</span>
</div>
</div>

<div className="bg-surface-container-low rounded-xl p-space-md flex flex-col gap-space-sm border border-surface-container">
<div className="flex items-center gap-space-xs">
<Brain className="text-primary text-[20px]" />
<span className="font-label-md text-label-md text-on-surface font-semibold">Four Product-Outcome Drivers</span>
</div>
<div className="grid grid-cols-1 sm:grid-cols-2 gap-space-xs">
<div className="bg-surface-container-lowest p-space-sm rounded-lg flex flex-col border border-surface-container/60">
<div className="flex items-center justify-between">
<span className="font-label-sm text-label-sm text-primary font-semibold">Driver: Want</span>
<Heart className="text-on-surface-variant text-[18px]" />
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-1">Sustained consumer desire vs. momentary novelty or impulse.</p>
</div>
<div className="bg-surface-container-lowest p-space-sm rounded-lg flex flex-col border border-surface-container/60">
<div className="flex items-center justify-between">
<span className="font-label-sm text-label-sm text-primary font-semibold">Driver: Confidence</span>
<CheckCircle className="text-on-surface-variant text-[18px]" />
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-1">Fit accuracy, measurement clarity, review reliability, and brand authenticity.</p>
</div>
<div className="bg-surface-container-lowest p-space-sm rounded-lg flex flex-col border border-surface-container/60">
<div className="flex items-center justify-between">
<span className="font-label-sm text-label-sm text-primary font-semibold">Driver: Value</span>
<Tag className="text-on-surface-variant text-[18px]" />
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-1">Price volatility, discount transparency, coupon terms, and catalog alternatives.</p>
</div>
<div className="bg-surface-container-lowest p-space-sm rounded-lg flex flex-col border border-surface-container/60">
<div className="flex items-center justify-between">
<span className="font-label-sm text-label-sm text-primary font-semibold">Driver: Availability</span>
<Archive className="text-on-surface-variant text-[18px]" />
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-1">Active inventory, size run stability, delivery timelines, and exchange confidence.</p>
</div>
</div>
</div>
</div>

<div className="flex flex-col gap-space-sm">
<div className="flex flex-col gap-0.5">
<h3 className="font-title text-title text-on-surface">Recurring Opportunity Areas</h3>
<p className="font-body-sm text-body-sm text-on-surface-variant">5 recurring opportunity areas identified in the analyzed pre-purchase evidence</p>
</div>
<div className="flex flex-col gap-space-sm">

<div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex flex-col gap-2 border border-surface-container/70">
<div className="flex items-start justify-between gap-2">
<div className="flex flex-col">
<span className="font-label-md text-label-md text-on-surface font-semibold">Other / System Friction</span>
<span className="font-code-sm text-code-sm text-on-surface-variant mt-0.5">3 Direct Evidence · 20 Indirect Evidence</span>
</div>
<div className="flex flex-col items-end shrink-0">
<span className="font-code-sm text-code-sm text-primary font-bold">23 records</span>
<span className="px-2 py-0.5 mt-1 rounded bg-surface-container-high text-on-surface-variant font-code-sm text-code-sm">HETEROGENEOUS</span>
</div>
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant bg-surface-container-low p-2 rounded leading-relaxed">Mixed platform, service, returns, support, and wishlist-related friction requiring further validation and sub-theme analysis. Mixed themes — requires sub-theme validation.</p>
</div>

<div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex flex-col gap-2 border border-surface-container/70">
<div className="flex items-start justify-between gap-2">
<div className="flex flex-col">
<span className="font-label-md text-label-md text-on-surface font-semibold">Price / Value</span>
<span className="font-code-sm text-code-sm text-on-surface-variant mt-0.5">3 Direct Evidence · 16 Indirect Evidence</span>
</div>
<div className="flex flex-col items-end shrink-0">
<span className="font-code-sm text-code-sm text-secondary font-bold">19 records</span>
<span className="px-2 py-0.5 mt-1 rounded bg-secondary-fixed text-on-secondary-fixed font-code-sm text-code-sm">Direct + Indirect Evidence Signal</span>
</div>
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant bg-surface-container-low p-2 rounded leading-relaxed">
              Recurring price and promotion uncertainty appears across the established evidence base.
            </p>
</div>

<div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex flex-col gap-2 border border-surface-container/70">
<div className="flex items-start justify-between gap-2">
<div className="flex flex-col">
<span className="font-label-md text-label-md text-on-surface font-semibold">Quality / Authenticity</span>
<span className="font-code-sm text-code-sm text-on-surface-variant mt-0.5">0 Direct Evidence · 15 Indirect Evidence</span>
</div>
<div className="flex flex-col items-end shrink-0">
<span className="font-code-sm text-code-sm text-primary font-bold">15 records</span>
<span className="px-2 py-0.5 mt-1 rounded bg-surface-container text-tertiary font-code-sm text-code-sm">Indirect Evidence Signal</span>
</div>
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant bg-surface-container-low p-2 rounded leading-relaxed">
              Recurring concerns relate to product quality, authenticity, durability, and differences between catalog representation and received expectations.
            </p>
</div>

<div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex flex-col gap-2 border border-surface-container/70">
<div className="flex items-start justify-between gap-2">
<div className="flex flex-col">
<span className="font-label-md text-label-md text-on-surface font-semibold">Availability / Stock</span>
<span className="font-code-sm text-code-sm text-on-surface-variant mt-0.5">0 Direct Evidence · 10 Indirect Evidence</span>
</div>
<div className="flex flex-col items-end shrink-0">
<span className="font-code-sm text-code-sm text-primary font-bold">10 records</span>
<span className="px-2 py-0.5 mt-1 rounded bg-surface-container text-tertiary font-code-sm text-code-sm">Indirect Evidence Signal</span>
</div>
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant bg-surface-container-low p-2 rounded leading-relaxed">
              Recurring signals relate to stock availability, size depletion, delivery reliability, and uncertainty around fulfillment.
            </p>
</div>

<div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex flex-col gap-2 border border-surface-container/70">
<div className="flex items-start justify-between gap-2">
<div className="flex flex-col">
<span className="font-label-md text-label-md text-on-surface font-semibold">Fit / Size</span>
<span className="font-code-sm text-code-sm text-on-surface-variant mt-0.5">0 Direct Evidence · 5 Indirect Evidence</span>
</div>
<div className="flex flex-col items-end shrink-0">
<span className="font-code-sm text-code-sm text-primary font-bold">5 records</span>
<span className="px-2 py-0.5 mt-1 rounded bg-surface-container-high text-primary font-code-sm text-code-sm">Emerging Evidence Signal</span>
</div>
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant bg-surface-container-low p-2 rounded leading-relaxed">
              Smaller-volume signals relate to sizing consistency, measurement uncertainty, and return-related confidence.
            </p>
</div>
</div>
</div>

<div className="flex flex-col gap-space-sm">

<div className="bg-surface-container-low rounded-xl p-space-md flex flex-col gap-space-xs border border-secondary/20 shadow-sm">
<div className="flex items-center gap-space-xs">
<AlertTriangle className="text-secondary text-[20px]" />
<h4 className="font-label-md text-label-md text-on-surface font-semibold">Research Limitation</h4>
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant leading-relaxed">Public conversation evidence is directional and may not represent the full Myntra user population. Evidence volume does not establish business impact or causality. Opportunity areas require primary research and experimentation before prioritization.</p>
<div className="flex items-center justify-between pt-space-xs border-t border-surface-container/60 mt-1">
<span className="font-code-sm text-code-sm text-tertiary">Grade: Directional Synthesis</span>
<Link to="/evidence"  className="font-label-sm text-label-sm text-primary hover:underline flex items-center gap-0.5 font-medium"  >
<span className="">Inspect Evidence Records</span>
<ChevronRight className="text-[14px]" />
</Link>
</div>
</div>

<div className="bg-surface-container-lowest rounded-xl p-space-md flex flex-col gap-2.5 shadow-sm border border-surface-container/70">
<div className="flex items-center gap-1.5">
<Network className="text-primary text-[18px]" />
<h4 className="font-label-md text-label-md text-on-surface font-semibold">Research Progression Chain</h4>
</div>
<div className="flex flex-col gap-1.5 pt-1">

<div className="flex items-start gap-2 text-body-sm">
<span className="w-5 h-5 rounded-full bg-primary/10 text-primary font-code-sm text-[11px] flex items-center justify-center shrink-0 mt-0.5 font-semibold">1</span>
<div>
<span className="font-medium text-on-surface">Business Metric:</span>
<span className="text-on-surface-variant"> Wishlist → Purchase Conversion</span>
</div>
</div>

<div className="flex items-start gap-2 text-body-sm">
<span className="w-5 h-5 rounded-full bg-primary/10 text-primary font-code-sm text-[11px] flex items-center justify-center shrink-0 mt-0.5 font-semibold">2</span>
<div>
<span className="font-medium text-on-surface">Shopper Journey:</span>
<span className="text-on-surface-variant"> 6 psychological progression gates from Save to Purchase</span>
</div>
</div>

<div className="flex items-start gap-2 text-body-sm">
<span className="w-5 h-5 rounded-full bg-primary/10 text-primary font-code-sm text-[11px] flex items-center justify-center shrink-0 mt-0.5 font-semibold">3</span>
<div>
<span className="font-medium text-on-surface">AI Discovery:</span>
<span className="text-on-surface-variant"> 1,447 public conversations across app stores and platforms</span>
</div>
</div>

<div className="flex items-start gap-2 text-body-sm">
<span className="w-5 h-5 rounded-full bg-primary/10 text-primary font-code-sm text-[11px] flex items-center justify-center shrink-0 mt-0.5 font-semibold">4</span>
<div>
<span className="font-medium text-on-surface">Established Evidence:</span>
<span className="text-on-surface-variant"> 72 records (6 Direct Evidence, 66 Indirect Evidence)</span>
</div>
</div>

<div className="flex items-start gap-2 text-body-sm">
<span className="w-5 h-5 rounded-full bg-primary/10 text-primary font-code-sm text-[11px] flex items-center justify-center shrink-0 mt-0.5 font-semibold">5</span>
<div>
<span className="font-medium text-on-surface">Opportunity Areas:</span>
<span className="text-on-surface-variant"> 5 verified friction themes</span>
</div>
</div>

<div className="flex items-start gap-2 text-body-sm">
<span className="w-5 h-5 rounded-full bg-primary/10 text-primary font-code-sm text-[11px] flex items-center justify-center shrink-0 mt-0.5 font-semibold">6</span>
<div>
<span className="font-medium text-on-surface">Hypotheses:</span>
<span className="text-on-surface-variant"> Structured barrier statements &amp; proposed interventions</span>
</div>
</div>

<div className="flex items-start gap-2 text-body-sm">
<span className="w-5 h-5 rounded-full bg-secondary/15 text-secondary font-code-sm text-[11px] flex items-center justify-center shrink-0 mt-0.5 font-semibold">7</span>
<div>
<span className="font-medium text-secondary">Primary Validation:</span>
<span className="text-on-surface-variant"> User interviews, analytics funnels, &amp; target A/B tests</span>
</div>
</div>

<div className="flex items-start gap-2 text-body-sm">
<span className="w-5 h-5 rounded-full bg-primary text-on-primary font-code-sm text-[11px] flex items-center justify-center shrink-0 mt-0.5 font-semibold">8</span>
<div>
<span className="font-semibold text-primary">Product Opportunity:</span>
<span className="text-on-surface-variant"> Prioritized roadmap bets for high conversion uplift</span>
</div>
</div>
</div>
</div>
</div>
</div>
</main>

<nav className="fixed bottom-0 w-full z-50 pb-safe bg-surface/95 backdrop-blur-xl border-t border-surface-container shadow-[0_-1px_8px_rgba(0,0,0,0.04)]" data-active-classes="text-primary font-semibold">
<div className="flex items-center justify-around h-16 px-space-xs">
<Link to="/"  aria-current="page" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 transition-colors text-primary font-semibold"  >
<LayoutDashboard className="text-[20px]" />
<span className="font-label-sm text-label-sm">Overview</span>
</Link>
<Link to="/copilot"  className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors"  >
<Bot className="text-[20px]" />
<span className="font-label-sm text-label-sm">Copilot</span>
</Link>
<Link to="/radar"  className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors"  >
<Radar className="text-[20px]" />
<span className="font-label-sm text-label-sm">Radar</span>
</Link>
<Link to="/evidence"  className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors"  >
<FolderOpen className="text-[20px]" />
<span className="font-label-sm text-label-sm">Evidence</span>
</Link>
<Link to="/settings"  className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors"  >
<Settings className="text-[20px]" />
<span className="font-label-sm text-label-sm">Settings</span>
</Link>
</div>
</nav>
    </>
  );
}
