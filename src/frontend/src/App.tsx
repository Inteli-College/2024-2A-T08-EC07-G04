import React from 'react';
import Header from './components/Header';

const App: React.FC = () => {
  return (
    <div>
      <Header />
      <main className="p-8">
        <h1 className="text-4xl font-bold mb-4">Welcome to MySite</h1>
        <p className="text-lg text-gray-700">Here is where your content goes...</p>
      </main>
    </div>
  );
};

export default App;
