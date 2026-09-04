import React from 'react';
import { Link } from 'react-router-dom';
import { LayoutDashboard, Bot, Radar, FolderOpen, Settings as SettingsIcon, ShieldAlert, Users, Database, AlertCircle } from 'lucide-react';

export default function Settings() {
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
            <div className="flex items-center gap-space-sm">
              <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                <Users className="text-on-primary text-[18px]" />
              </div>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-space-xs min-w-0">
              <span className="inline-block w-1.5 h-1.5 rounded-full bg-secondary shrink-0"></span>
              <span className="font-label-sm text-label-sm text-on-surface-variant truncate">PM Fellowship / Myntra Discovery</span>
            </div>
            <div className="flex items-center gap-space-xs text-on-surface-variant shrink-0">
              <span className="font-code-sm text-code-sm text-on-surface-variant"><span className="text-primary font-medium">1,447</span> analyzed / <span className="text-secondary font-medium">72</span> established</span>
            </div>
          </div>
        </div>
      </header>

      <main className="flex flex-col relative w-full pt-28 pb-28 bg-surface min-h-screen">
        <div className="flex flex-col w-full px-space-base gap-space-lg pb-space-xl">
          
          <div className="flex flex-col gap-space-2xs">
            <div className="flex items-center gap-space-xs">
              <SettingsIcon className="text-primary text-[20px]" />
              <h1 className="font-headline-sm text-headline-sm text-on-surface tracking-tight">Configuration & Policies</h1>
            </div>
            <p className="font-body-sm text-body-sm text-on-surface-variant">Review workspace settings and evidence limits.</p>
          </div>

          <div className="flex flex-col gap-space-sm">
            <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm border border-outline-variant/30 flex flex-col gap-space-sm">
              <div className="flex items-center gap-space-xs pb-space-xs border-b border-outline-variant/20">
                <Users className="text-primary text-[18px]" />
                <h2 className="font-label-md text-label-md text-on-surface font-semibold">Workspace</h2>
              </div>
              <div className="flex flex-col gap-space-2xs">
                <span className="font-label-sm text-label-sm text-on-surface-variant">Project Name</span>
                <span className="font-body-md text-body-md text-on-surface">Wishlist Intelligence</span>
              </div>
              <div className="flex flex-col gap-space-2xs">
                <span className="font-label-sm text-label-sm text-on-surface-variant">Organization</span>
                <span className="font-body-md text-body-md text-on-surface">PM Fellowship / Myntra Discovery</span>
              </div>
            </div>

            <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm border border-outline-variant/30 flex flex-col gap-space-sm">
              <div className="flex items-center gap-space-xs pb-space-xs border-b border-outline-variant/20">
                <ShieldAlert className="text-secondary text-[18px]" />
                <h2 className="font-label-md text-label-md text-on-surface font-semibold">Evidence Policy</h2>
              </div>
              <div className="flex flex-col gap-space-2xs">
                <div className="flex items-center justify-between">
                  <span className="font-label-sm text-label-sm text-on-surface font-medium">Direct Evidence</span>
                  <span className="px-space-xs py-space-2xs rounded bg-surface-container-high text-primary font-code-sm text-code-sm">HIGH CONFIDENCE</span>
                </div>
                <p className="font-body-sm text-body-sm text-on-surface-variant">Explicit mentions of wishlist behavior, saving items for later, or cart abandonment.</p>
              </div>
              <div className="flex flex-col gap-space-2xs mt-space-xs">
                <div className="flex items-center justify-between">
                  <span className="font-label-sm text-label-sm text-on-surface font-medium">Indirect Evidence</span>
                  <span className="px-space-xs py-space-2xs rounded bg-surface-container text-on-surface-variant font-code-sm text-code-sm">MODERATE CONFIDENCE</span>
                </div>
                <p className="font-body-sm text-body-sm text-on-surface-variant">Friction points during consideration that strongly correlate with purchase hesitation (e.g. price drops, fit uncertainty).</p>
              </div>
            </div>

            <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm border border-outline-variant/30 flex flex-col gap-space-sm">
              <div className="flex items-center gap-space-xs pb-space-xs border-b border-outline-variant/20">
                <Database className="text-primary text-[18px]" />
                <h2 className="font-label-md text-label-md text-on-surface font-semibold">Data Sources</h2>
              </div>
              <ul className="flex flex-col gap-space-xs text-on-surface-variant font-body-sm text-body-sm">
                <li className="flex items-center gap-space-xs before:content-[''] before:block before:w-1.5 before:h-1.5 before:bg-primary before:rounded-full">Google Play Reviews</li>
                <li className="flex items-center gap-space-xs before:content-[''] before:block before:w-1.5 before:h-1.5 before:bg-primary before:rounded-full">Apple App Store Reviews</li>
                <li className="flex items-center gap-space-xs before:content-[''] before:block before:w-1.5 before:h-1.5 before:bg-primary before:rounded-full">YouTube Transcripts</li>
              </ul>
            </div>

            <div className="bg-error-container/20 p-space-md rounded-xl border border-error/20 flex flex-col gap-space-sm">
              <div className="flex items-center gap-space-xs">
                <AlertCircle className="text-error text-[18px]" />
                <h2 className="font-label-md text-label-md text-on-error-container font-semibold">Research Limitations</h2>
              </div>
              <ul className="flex flex-col gap-space-xs text-on-surface-variant font-body-sm text-body-sm">
                <li className="flex items-start gap-space-xs before:content-[''] before:block before:w-1.5 before:h-1.5 before:bg-error before:rounded-full before:mt-1.5 before:shrink-0">
                  Public conversation evidence is directional and may not represent the full Myntra user population.
                </li>
                <li className="flex items-start gap-space-xs before:content-[''] before:block before:w-1.5 before:h-1.5 before:bg-error before:rounded-full before:mt-1.5 before:shrink-0">
                  Evidence volume does not establish business impact or causality.
                </li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      <nav className="fixed bottom-0 w-full z-50 pb-safe bg-surface/90 backdrop-blur-xl shadow-[0_-1px_8px_rgba(0,0,0,0.04)]">
        <div className="flex items-center justify-around h-16 px-space-xs">
          <Link to="/" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors">
            <LayoutDashboard className=" text-[20px]" />
            <span className="font-label-sm text-label-sm">Overview</span>
          </Link>
          <Link to="/copilot" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors">
            <Bot className=" text-[20px]" />
            <span className="font-label-sm text-label-sm">Copilot</span>
          </Link>
          <Link to="/radar" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors">
            <Radar className=" text-[20px]" />
            <span className="font-label-sm text-label-sm">Radar</span>
          </Link>
          <Link to="/evidence" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 text-on-surface-variant hover:text-on-surface transition-colors">
            <FolderOpen className=" text-[20px]" />
            <span className="font-label-sm text-label-sm">Evidence</span>
          </Link>
          <Link to="/settings" aria-current="page" className="min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-0.5 transition-colors text-primary font-semibold">
            <SettingsIcon className=" text-[20px]" />
            <span className="font-label-sm text-label-sm">Settings</span>
          </Link>
        </div>
      </nav>
    </>
  );
}
