import React from 'react';

const IssuesTable: React.FC = () => {
  const mockIssues = [
    { name: 'Falha no sistema de freio', color: 'Red', category: 'Safety', price: '$2000' },
    { name: 'Desgaste excessivo de pneus', color: 'Black', category: 'Tires', price: '$300' },
    { name: 'Problemas no motor', color: 'Blue', category: 'Engine', price: '$1500' },
  ];

  return (
    <div className="relative overflow-x-auto shadow-md sm:rounded-lg mt-8">
      <table className="w-full text-sm text-left text-gray-500">
        <thead className="text-xs text-gray-700 uppercase bg-gray-50">
          <tr>
            <th scope="col" className="px-6 py-3">
              Nome do Problema
            </th>
            <th scope="col" className="px-6 py-3">
              Cor
            </th>
            <th scope="col" className="px-6 py-3">
              Categoria
            </th>
            <th scope="col" className="px-6 py-3">
              Preço
            </th>
            <th scope="col" className="px-6 py-3">
              <span className="sr-only">Ação</span>
            </th>
          </tr>
        </thead>
        <tbody>
          {mockIssues.map((issue, index) => (
            <tr key={index} className="bg-white border-b hover:bg-gray-50">
              <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                {issue.name}
              </th>
              <td className="px-6 py-4">{issue.color}</td>
              <td className="px-6 py-4">{issue.category}</td>
              <td className="px-6 py-4">{issue.price}</td>
              <td className="px-6 py-4 text-right">
                <a href="#" className="font-medium text-blue-600 hover:underline">
                  Detalhes
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default IssuesTable;
