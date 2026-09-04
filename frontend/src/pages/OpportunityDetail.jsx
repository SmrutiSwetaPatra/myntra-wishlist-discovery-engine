import React from 'react';
import { ArrowLeft, BadgeDollarSign, Box, CheckCircle, ChevronRight, ClipboardCheck, Eye, FileCheck, FlaskConical, HelpCircle, Hourglass, Info, Lightbulb, MonitorPlay, Play, Smartphone, Ticket, TrendingUp, User } from 'lucide-react';


export default function OpportunityDetail() {
  return (
    <>
<header className="fixed top-0 w-full z-50 pt-safe bg-surface/90 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.04)]"><div className="h-16 px-space-base flex items-center justify-between gap-space-sm"><div className="flex items-center gap-space-xs"><button className="min-h-[44px] min-w-[44px] flex items-center justify-center text-on-surface-variant hover:text-on-surface transition-colors" onclick="history.back()"><ArrowLeft className="text-[22px]" /></button><div className="flex flex-col"><span className="font-title text-title text-on-surface tracking-tight leading-tight line-clamp-1">Opportunity Detail</span><span className="font-code-sm text-code-sm text-on-surface-variant leading-none">PM Fellowship / Myntra Discovery</span></div></div><div className="flex items-center gap-space-xs"><div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center"><User className="text-on-primary text-[18px]" /></div></div></div></header><main className="flex flex-col relative w-full pt-16 pb-safe bg-surface min-h-screen"><div className="flex flex-col w-full pb-28">

<section className="px-margin-mobile pt-space-md flex flex-col gap-space-xs">
<div className="flex items-center gap-space-xs text-on-surface-variant font-label-sm text-label-sm">
<span className="hover:text-primary transition-colors cursor-pointer">Opportunity Radar</span>
<ChevronRight className="text-[14px]" />
<span className="text-primary font-medium">Price / Value</span>
</div>
<div className="flex items-start justify-between gap-space-sm mt-space-xs">
<div className="flex flex-col">
<h1 className="font-headline-lg-mobile text-headline-lg-mobile text-on-surface font-bold tracking-tight">Price / Value</h1>
<p className="font-body-md text-body-md text-on-surface-variant mt-1 leading-snug">
          Recurring price and promotion uncertainty appears across the established evidence base.
        </p>
</div>
<div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-primary-fixed text-on-primary-fixed shrink-0 mt-1 shadow-sm">
<span className="w-1.5 h-1.5 rounded-full bg-primary"></span>
<span className="font-label-sm text-[11px] font-semibold tracking-tight">Direct + Indirect Evidence</span>
</div>
</div>
</section>

<section className="px-margin-mobile mt-space-lg flex flex-col gap-space-md">
<div className="flex items-center gap-2">
<Eye className="text-primary text-[22px]" />
<h2 className="font-title text-title text-on-surface font-bold">What We Observed</h2>
</div>

<div className="bg-surface-container-low rounded-xl p-space-base flex flex-col gap-space-md shadow-sm">
<div className="flex items-center justify-between">
<span className="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant font-semibold">
          Established Evidence Base
        </span>
<span className="font-code-sm text-code-sm font-semibold text-primary px-2.5 py-0.5 rounded bg-surface-container-lowest shadow-sm">
          19 Records Logged
        </span>
</div>
<div className="grid grid-cols-2 gap-space-sm">
<div className="bg-surface-container-lowest p-3 rounded-lg flex flex-col justify-between shadow-sm">
<div className="flex items-center justify-between">
<span className="font-label-sm text-label-sm text-on-surface-variant">Direct Evidence</span>
<span className="w-2.5 h-2.5 rounded-full bg-primary"></span>
</div>
<div className="flex items-baseline gap-1.5 mt-2">
<span className="font-headline-md text-headline-md text-on-surface font-bold">3</span>
<span className="font-code-sm text-code-sm text-on-surface-variant">records</span>
</div>
</div>
<div className="bg-surface-container-lowest p-3 rounded-lg flex flex-col justify-between shadow-sm">
<div className="flex items-center justify-between">
<span className="font-label-sm text-label-sm text-on-surface-variant">Indirect Evidence</span>
<span className="w-2.5 h-2.5 rounded-full bg-tertiary"></span>
</div>
<div className="flex items-baseline gap-1.5 mt-2">
<span className="font-headline-md text-headline-md text-on-surface font-bold">16</span>
<span className="font-code-sm text-code-sm text-on-surface-variant">records</span>
</div>
</div>
</div>

<div className="flex items-center gap-2 flex-wrap pt-0.5">
<div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface-container-lowest text-on-surface font-label-sm text-label-sm shadow-sm">
<Play className="text-[16px] text-primary" />
<span className="">Google Play</span>
<span className="font-semibold text-primary ml-0.5">8</span>
</div>
<div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface-container-lowest text-on-surface font-label-sm text-label-sm shadow-sm">
<Smartphone className="text-[16px] text-secondary" />
<span className="">App Store</span>
<span className="font-semibold text-secondary ml-0.5">7</span>
</div>
<div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface-container-lowest text-on-surface font-label-sm text-label-sm shadow-sm">
<MonitorPlay className="text-[16px] text-error" />
<span className="">YouTube</span>
<span className="font-semibold text-error ml-0.5">4</span>
</div>
</div>
</div>

<div className="bg-surface-container-lowest p-space-base rounded-xl border border-outline-variant/40 shadow-sm flex items-start gap-space-sm">
<div className="w-7 h-7 rounded-full bg-primary-fixed text-primary flex items-center justify-center shrink-0 mt-0.5">
<TrendingUp className="text-[17px]" />
</div>
<div className="flex flex-col">
<span className="font-label-sm text-label-sm uppercase tracking-wider text-primary font-bold">Evidence Signal</span>
<p className="font-body-md text-body-md text-on-surface mt-0.5 leading-snug">Recurring price and promotion uncertainty appears across the established evidence base.</p>
</div>
</div>

<div className="flex flex-col gap-2.5">
<span className="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant font-semibold px-0.5">Observed Friction Patterns</span>
<div className="bg-surface-container-lowest p-space-base rounded-xl shadow-sm flex items-start gap-space-sm">
<div className="w-7 h-7 rounded-full bg-error-container text-on-error-container flex items-center justify-center shrink-0 mt-0.5">
<BadgeDollarSign className="text-[16px]" />
</div>
<div className="flex flex-col">
<span className="font-label-md text-label-md text-on-surface font-semibold">Sudden Price Shifts</span>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">Divergent prices displayed between the wishlist overview tile and cart checkout correlates with immediate cognitive hesitation and distrust.</p>
</div>
</div>
<div className="bg-surface-container-lowest p-space-base rounded-xl shadow-sm flex items-start gap-space-sm">
<div className="w-7 h-7 rounded-full bg-surface-container-high text-primary flex items-center justify-center shrink-0 mt-0.5">
<Ticket className="text-[16px]" />
</div>
<div className="flex flex-col">
<span className="font-label-md text-label-md text-on-surface font-semibold">Banner vs. Cart Coupon Mismatch</span>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">
            Confusion surrounding broad sale banners vs brand-specific exclusions leads shoppers to save items expecting unfulfilled discounts.
          </p>
</div>
</div>
<div className="bg-surface-container-lowest p-space-base rounded-xl shadow-sm flex items-start gap-space-sm">
<div className="w-7 h-7 rounded-full bg-tertiary-fixed text-on-tertiary-fixed flex items-center justify-center shrink-0 mt-0.5">
<Hourglass className="text-[16px]" />
</div>
<div className="flex flex-col">
<span className="font-label-md text-label-md text-on-surface font-semibold">Price History Blind Spots</span>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">
            Total absence of historical price trajectory or drop reassurance leaves shoppers uncertain whether current pricing will discount further.
          </p>
</div>
</div>
</div>
</section>

<section className="px-margin-mobile mt-space-lg flex flex-col gap-space-sm">
<div className="flex items-center justify-between">
<div className="flex items-center gap-2">
<ClipboardCheck className="text-primary text-[20px]" />
<h2 className="font-title text-title text-on-surface font-bold">Representative Evidence</h2>
</div>
<span className="font-code-sm text-code-sm text-on-surface-variant font-medium">3 Representative</span>
</div>

<div className="bg-surface-container-lowest rounded-xl p-space-base flex flex-col gap-space-xs shadow-sm border border-outline-variant/30">
<div className="flex items-center justify-between gap-2">
<span className="px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider bg-surface-container-highest text-primary">
          Direct Evidence
        </span>
<div className="flex items-center gap-1 text-on-surface-variant font-code-sm text-code-sm">
<Play className="text-[15px] text-primary" />
<span className="">Google Play</span>
</div>
</div>
<p className="font-body-md text-body-md text-on-surface font-normal mt-1 leading-relaxed">
        “Coupon did not apply to saved items at checkout despite banner promises. Spent 20 minutes curating 4 dresses in my wishlist only to see ₹600 surge added at payment review.”
      </p>
<div className="flex items-center justify-between text-on-surface-variant font-code-sm text-code-sm mt-2 pt-2 border-t border-surface-container">
<span className="">Stage: Resolve Uncertainty</span>
<span className="font-medium text-primary">Intent: High</span>
</div>
</div>

<div className="bg-surface-container-lowest rounded-xl p-space-base flex flex-col gap-space-xs shadow-sm border border-outline-variant/30">
<div className="flex items-center justify-between gap-2">
<span className="px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider bg-surface-container-highest text-primary">
          Direct Evidence
        </span>
<div className="flex items-center gap-1 text-on-surface-variant font-code-sm text-code-sm">
<Smartphone className="text-[15px] text-secondary" />
<span className="">Apple App Store</span>
</div>
</div>
<p className="font-body-md text-body-md text-on-surface font-normal mt-1 leading-relaxed">
        “Wishlist price was ₹1,299 but product detail showed ₹1,899 when clicking in. Why show a discounted sticker price in the wishlist if the size variant is excluded? Left the app.”
      </p>
<div className="flex items-center justify-between text-on-surface-variant font-code-sm text-code-sm mt-2 pt-2 border-t border-surface-container">
<span className="">Stage: Revisit</span>
<span className="font-medium text-secondary">Intent: Medium</span>
</div>
</div>

<div className="bg-surface-container-lowest rounded-xl p-space-base flex flex-col gap-space-xs shadow-sm border border-outline-variant/30">
<div className="flex items-center justify-between gap-2">
<span className="px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider bg-surface-container text-tertiary">
          Indirect Evidence
        </span>
<div className="flex items-center gap-1 text-on-surface-variant font-code-sm text-code-sm">
<MonitorPlay className="text-[15px] text-error" />
<span className="">YouTube</span>
</div>
</div>
<p className="font-body-md text-body-md text-on-surface font-normal mt-1 leading-relaxed">
        “Users save items during sales waiting to see if prices drop further on the final day. Multiple haul creators advise subscribers never to purchase wishlist items on Day 1.”
      </p>
<div className="flex items-center justify-between text-on-surface-variant font-code-sm text-code-sm mt-2 pt-2 border-t border-surface-container">
<span className="">Stage: Evaluate</span>
<span className="font-medium text-tertiary">Intent: Low / Observation</span>
</div>
</div>
</section>

<section className="px-margin-mobile mt-space-lg">
<div className="bg-surface-container p-space-base rounded-xl flex flex-col gap-space-xs shadow-sm relative overflow-hidden">
<div className="absolute -right-6 -bottom-6 w-24 h-24 rounded-full bg-primary-fixed-dim/40 pointer-events-none"></div>
<div className="flex items-center gap-1.5 text-primary">
<CheckCircle className="text-[18px]" />
<span className="font-label-sm text-label-sm uppercase tracking-wider font-bold">Unmet Need Statement</span>
</div>
<blockquote className="font-headline-sm text-headline-sm text-on-surface font-medium italic mt-1 leading-snug">
        “Shoppers may need immediate transparency into promotional eligibility, net checkout price, and reassurance against near-term price drops before committing to a purchase from their wishlist.”
      </blockquote>
<div className="flex items-center gap-2 mt-2 pt-2 text-on-surface-variant font-label-sm text-label-sm">
<Lightbulb className="text-[16px] text-secondary" />
<span className="">Anchor for Wishlist Intelligence Pricing Architecture</span>
</div>
</div>
</section>

<section className="px-margin-mobile mt-space-lg">
<div className="bg-surface-container-high rounded-xl p-space-base flex flex-col gap-2.5 shadow-sm border border-primary/20">
<div className="flex items-center gap-2">
<span className="px-2 py-0.5 rounded bg-primary text-on-primary font-code-sm text-code-sm font-semibold tracking-wider">
          EVIDENCE-BACKED HYPOTHESIS
        </span>
</div>
<p className="font-body-md text-body-md text-on-surface font-semibold leading-relaxed">
        Improving price and promotion transparency may reduce hesitation during consideration.
      </p>
<div className="bg-surface-container-lowest/80 rounded-lg p-2.5 text-body-sm text-on-surface-variant font-normal leading-snug"><span className="font-semibold text-primary">Label:</span> Hypothesis — requires primary research and experimentation before being treated as a conversion driver.</div>
</div>
</section>

<section className="px-margin-mobile mt-space-lg flex flex-col gap-space-sm">
<div className="flex items-center gap-2">
<HelpCircle className="text-primary text-[20px]" />
<h2 className="font-title text-title text-on-surface font-bold">Questions to Validate</h2>
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant -mt-1">
      Framed as research inquiries without assumed causality.
    </p>
<div className="flex flex-col gap-2.5">
<div className="bg-surface-container-lowest p-space-base rounded-xl shadow-sm flex items-start gap-space-sm">
<div className="w-6 h-6 rounded-md bg-surface-container-high text-primary flex items-center justify-center shrink-0 font-code-sm text-code-sm font-bold">
          Q1
        </div>
<div className="flex flex-col">
<span className="font-label-md text-label-md text-on-surface font-medium">
            Does price uncertainty meaningfully delay purchase of saved items?
          </span>
<span className="font-code-sm text-[11px] text-on-surface-variant mt-1">Metric: User hesitation duration &amp; post-wishlist abandon interviews</span>
</div>
</div>
<div className="bg-surface-container-lowest p-space-base rounded-xl shadow-sm flex items-start gap-space-sm">
<div className="w-6 h-6 rounded-md bg-surface-container-high text-primary flex items-center justify-center shrink-0 font-code-sm text-code-sm font-bold">
          Q2
        </div>
<div className="flex flex-col">
<span className="font-label-md text-label-md text-on-surface font-medium">
            Does showing clearer price history reduce wishlist-to-cart hesitation?
          </span>
<span className="font-code-sm text-[11px] text-on-surface-variant mt-1">Metric: Revisit-to-bag velocity</span>
</div>
</div>
<div className="bg-surface-container-lowest p-space-base rounded-xl shadow-sm flex items-start gap-space-sm">
<div className="w-6 h-6 rounded-md bg-surface-container-high text-primary flex items-center justify-center shrink-0 font-code-sm text-code-sm font-bold">
          Q3
        </div>
<div className="flex flex-col">
<span className="font-label-md text-label-md text-on-surface font-medium">
            Which pricing information is most important before checkout?
          </span>
<span className="font-code-sm text-[11px] text-on-surface-variant mt-1">Metric: Feature utility ranking from user validation</span>
</div>
</div>
<div className="bg-surface-container-lowest p-space-base rounded-xl shadow-sm flex items-start gap-space-sm">
<div className="w-6 h-6 rounded-md bg-surface-container-high text-primary flex items-center justify-center shrink-0 font-code-sm text-code-sm font-bold">
          Q4
        </div>
<div className="flex flex-col">
<span className="font-label-md text-label-md text-on-surface font-medium">
            How often does unexpected coupon ineligibility cause abandonment of wishlisted items?
          </span>
<span className="font-code-sm text-[11px] text-on-surface-variant mt-1">Metric: Drop-off correlation during checkout price reveal</span>
</div>
</div>
</div>
</section>

<section className="px-margin-mobile mt-space-lg mb-space-base">
<div className="bg-surface-container-low rounded-xl p-space-base flex flex-col gap-space-md shadow-sm">
<div className="flex items-center gap-2">
<FileCheck className="text-tertiary text-[20px]" />
<h2 className="font-title text-title text-on-surface font-bold">Research Limitations &amp; Governance</h2>
</div>
<div className="bg-surface-container-lowest p-3.5 rounded-lg border border-outline-variant/30 flex items-start gap-2.5">
<Info className="text-secondary text-[18px] shrink-0 mt-0.5" />
<p className="font-body-sm text-body-sm text-on-surface leading-relaxed">
<strong className="font-semibold text-on-surface">Research Limitation:</strong> Public conversation evidence is directional and may not represent the full user population. Evidence volume does not establish business impact or causality. Opportunity areas are hypotheses requiring primary research.
        </p>
</div>

<div className="bg-surface-container-lowest p-space-base rounded-lg flex flex-col gap-space-sm shadow-sm">
<span className="font-label-sm text-label-sm uppercase tracking-wider text-primary font-bold">
          Validation Backlog
        </span>
<div className="flex flex-col gap-2">
<div className="flex items-center justify-between text-body-sm font-body-sm">
<span className="text-on-surface flex items-center gap-1.5">
<Box className="text-[16px] text-primary" />
              Scheduled 1-on-1 discovery interviews (n=12)
            </span>
<span className="font-code-sm text-code-sm text-on-surface-variant font-medium">Scheduled</span>
</div>
<div className="flex items-center justify-between text-body-sm font-body-sm">
<span className="text-on-surface flex items-center gap-1.5">
<FlaskConical className="text-[16px] text-primary" />
              A/B coupon transparency experiment
            </span>
<span className="font-code-sm text-code-sm text-on-surface-variant font-medium">Backlog</span>
</div>
</div>
</div>

<div className="pt-2 flex items-center gap-space-sm">
<button className="flex-1 bg-primary text-on-primary font-label-md text-label-md py-2.5 px-space-base rounded-lg flex items-center justify-center gap-2 shadow-sm active:scale-[0.98] transition-transform">
<Box className="text-[18px]" />
<span className="">Draft User Interview Script</span>
</button>
<button className="bg-surface-container-highest text-on-surface-variant hover:text-on-surface p-2.5 rounded-lg flex items-center justify-center transition-colors">
<Box className="text-[20px]" />
</button>
</div>
</div>
</section>
</div></main>
    </>
  );
}
