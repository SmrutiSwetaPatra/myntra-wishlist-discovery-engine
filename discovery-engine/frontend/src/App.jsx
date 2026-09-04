import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Overview from './pages/Overview';
import OpportunityRadar from './pages/OpportunityRadar';
import OpportunityDetail from './pages/OpportunityDetail';
import EvidenceExplorer from './pages/EvidenceExplorer';
import DiscoveryCopilot from './pages/DiscoveryCopilot';
import Settings from './pages/Settings';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background text-on-background">
        <main>
          <Routes>
            <Route path="/" element={<Overview />} />
            <Route path="/radar" element={<OpportunityRadar />} />
            <Route path="/detail" element={<OpportunityDetail />} />
            <Route path="/evidence" element={<EvidenceExplorer />} />
            <Route path="/copilot" element={<DiscoveryCopilot />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
