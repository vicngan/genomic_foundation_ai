import React from 'react';
import ParlantChatbox from 'parlant-chat-react';

export function Dashboard() {
  return (
    <main className="flex-grow container mx-auto p-4 grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="lg:col-span-2">
        <h2 className="text-xl font-semibold mb-4">Main Content</h2>
        <div className="bg-white p-6 rounded-lg shadow">
          <p>Welcome to the GFM Platform. The main features will be displayed here.</p>
          <p className="mt-4">The AI chat interface is on the right.</p>
        </div>
      </div>

      <aside>
        {/* 
          You will need to replace these placeholder values with your actual 
          Parlant server URL and Agent ID.
        */}
        <ParlantChatbox server="PARLANT_SERVER_URL" agentId="AGENT_ID" />
      </aside>
    </main>
  );
}