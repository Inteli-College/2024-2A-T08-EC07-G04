import React, { useState } from 'react';
import NavBar from '../components/NavBar';

const NoIssuesPage: React.FC = () => {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <div className="bg-[#000475] min-h-screen flex flex-col">
      <NavBar />

      <div className="flex flex-grow flex-col items-center justify-center">
        <div className="bg-white rounded-lg shadow-lg px-8 py-10 flex flex-col items-center justify-center w-full max-w-lg">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-40 w-40 text-green-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
          </svg>
          <p className="text-lg font-semibold mt-6 text-[#000475]">Não há necessidade de testes longos</p>
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="mt-6 bg-[#2f94bf] text-white px-6 py-3 rounded-full hover:bg-[#2381a6] transition duration-300 ease-in-out"
          >
            {showDetails ? 'Ocultar Detalhes' : 'Detalhes'}
          </button>
        </div>

        {showDetails && (
          <div className="mt-6 bg-white rounded-lg shadow-lg p-6 w-full max-w-lg">
            <h3 className="text-lg font-semibold mb-2 text-[#000475]">Detalhes:</h3>
            <p className="text-sm text-gray-700">
              Detalhes do resultado do modelo: Nenhuma falha foi detectada após análise completa.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default NoIssuesPage;
