import React from 'react';
import NavBar from '../components/NavBar';
import PredictionComponent from '../components/PredictionComponent';

const App: React.FC = () => {
  return (
    <div className="bg-[#000475] min-h-screen flex flex-col">
      <NavBar />
      <main className="p-8 flex flex-col items-center justify-center text-white flex-grow">
      <div className="bg-white shadow-lg rounded-lg p-6 max-w-4xl w-full h-30">
            <PredictionComponent />
        </div>
      </main>
    </div>
  );
};

export default App;
