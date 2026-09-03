import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Overview from './pages/Overview';
import OpportunityRadar from './pages/OpportunityRadar';
import OpportunityDetail from './pages/OpportunityDetail';
import EvidenceExplorer from './pages/EvidenceExplorer';
import DiscoveryCopilot from './pages/DiscoveryCopilot';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background">
        <nav className="p-4 bg-surface border-b border-outline-variant flex gap-4 overflow-x-auto">
          <Link to="/" className="text-primary font-medium hover:underline whitespace-nowrap">Overview</Link>
          <Link to="/radar" className="text-primary font-medium hover:underline whitespace-nowrap">Opportunity Radar</Link>
          <Link to="/detail" className="text-primary font-medium hover:underline whitespace-nowrap">Opportunity Detail</Link>
          <Link to="/evidence" className="text-primary font-medium hover:underline whitespace-nowrap">Evidence Explorer</Link>
          <Link to="/copilot" className="text-primary font-medium hover:underline whitespace-nowrap">Discovery Copilot</Link>
        </nav>
        <main>
          <Routes>
            <Route path="/" element={<Overview />} />
            <Route path="/radar" element={<OpportunityRadar />} />
            <Route path="/detail" element={<OpportunityDetail />} />
            <Route path="/evidence" element={<EvidenceExplorer />} />
            <Route path="/copilot" element={<DiscoveryCopilot />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
