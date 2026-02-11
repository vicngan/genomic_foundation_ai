import React from 'react';
import Chatbox from '@/components/Chatbox';

function App() {
  return (
    <div className="bg-gray-100 min-h-screen flex flex-col">
      <header className="bg-white shadow-md p-4">
        <h1 className="text-2xl font-bold text-gray-800">Genomic Model AI</h1>
      </header>

      <main className="flex-grow container mx-auto p-4 grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <h2 className="text-xl font-semibold mb-4">Main Content</h2>
          <div className="bg-white p-6 rounded-lg shadow">
            <p>Welcome to the Genomic Model AI platform. The main features will be displayed here.</p>
            <p className="mt-4">The chat interface is on the right.</p>
          </div>
        </div>

        <aside>
          <Chatbox />
        </aside>
      </main>

      <footer className="bg-white text-center p-4 mt-8">
        <p className="text-gray-600">&copy; 2024 Genomic Model AI. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;