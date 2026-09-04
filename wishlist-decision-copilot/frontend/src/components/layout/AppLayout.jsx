import React from 'react';
import { Outlet } from 'react-router-dom';
import { Navbar } from './Navbar';
import { BottomNav } from './BottomNav';
import '../../index.css';

export const AppLayout = () => {
  return (
    <div className="app-layout">
      <Navbar />
      <main className="main-content container">
        <Outlet />
      </main>
      <BottomNav />
    </div>
  );
};
