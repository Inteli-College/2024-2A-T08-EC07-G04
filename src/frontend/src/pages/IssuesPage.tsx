import React from 'react';
import NavBar from '../components/NavBar';
import IssuesTable from '../components/IssuesTable';
import { HiX } from 'react-icons/hi';

const IssuesPage: React.FC = () => {
  const mockIssues = ['Falha no sistema de freio', 'Desgaste excessivo de pneus', 'Problemas no motor'];

  const exportDetails = () => {
    const data = JSON.stringify(mockIssues, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'falhas.json');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="min-h-screen bg-[#000475]">
      <NavBar />
      <div className="flex flex-col items-center justify-center mt-8">
        
        <div className="relative bg-white shadow-lg rounded-lg p-4 mb-6">
          <div className="flex justify-between items-center mb-4"> {/* Flex container para o título e ícone */}
            <div className="text-black text-xl font-bold">Possíveis falhas</div>
            <div className="text-red-600 cursor-pointer">
              <HiX size={30} />
            </div>
          </div>
          <div className="overflow-x-auto w-full max-w-4xl">
            <IssuesTable />
          </div>
        </div>

        <button
          onClick={exportDetails}
          className="mt-6 bg-[#2f94bf] text-white px-6 py-2 rounded-md hover:bg-[#2a8da4]"
        >
          Exportar Informações
        </button>
      </div>
    </div>
  );
};

export default IssuesPage;