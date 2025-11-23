import Navigation from "./Navigation";
import Sidebar from "./Sidebar";
import React from 'react';

export default function MainLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col min-h-screen bg-gray-100 font-sans">
      <Navigation />
      <div className="flex flex-1">
        <Sidebar />
        {children} 
      </div>
    </div>
  );
}