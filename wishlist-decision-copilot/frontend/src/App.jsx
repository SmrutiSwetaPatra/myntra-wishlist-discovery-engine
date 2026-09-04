import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AppLayout } from './components/layout/AppLayout';
import { Home } from './pages/Home';
import { Discover } from './pages/Discover';
import { ProductDetail } from './pages/ProductDetail';
import { Wishlist } from './pages/Wishlist';
import { DecisionCopilot } from './pages/DecisionCopilot';
import { Compare } from './pages/Compare';
import { Activity } from './pages/Activity';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Home />} />
          <Route path="discover" element={<Discover />} />
          <Route path="products/:id" element={<ProductDetail />} />
          <Route path="wishlist" element={<Wishlist />} />
          <Route path="copilot" element={<DecisionCopilot />} />
          <Route path="compare" element={<Compare />} />
          <Route path="activity" element={<Activity />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
