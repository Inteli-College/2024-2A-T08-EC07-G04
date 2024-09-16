import React, { useState } from 'react';
import NavBar from '../components/NavBar';
import DateFilter from '../components/DateFilter';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Legend, ResponsiveContainer } from 'recharts';
import AreaStatusChart from '../components/Graph2'; 
import Graph3 from '../components/Graph3';

// Componente de card para exibir estatísticas
const DashboardCard: React.FC<{ title: string; value: string; icon: React.ReactNode }> = ({ title, value, icon }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md flex items-center space-x-4">
      <div className="text-blue-500 text-3xl">{icon}</div>
      <div>
        <h3 className="text-xl font-semibold">{title}</h3>
        <p className="text-gray-600 text-lg">{value}</p>
      </div>
    </div>
  );
};

// Dados de exemplo para o gráfico
const data = [
  { month: 'Jan', totalCars: 4000, faultyCars: 240 },
  { month: 'Feb', totalCars: 3000, faultyCars: 139 },
  { month: 'Mar', totalCars: 2000, faultyCars: 98 },
  { month: 'Apr', totalCars: 2780, faultyCars: 390 },
  { month: 'May', totalCars: 1890, faultyCars: 48 },
];

const CarFailureChart: React.FC = () => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="totalCars" fill="#2f94bf" name="Total de Carros" />
        <Bar dataKey="faultyCars" fill="#ff4d4d" name="Carros com Falha" />
      </BarChart>
    </ResponsiveContainer>
  );
};

const App: React.FC = () => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const handleDateFilter = (startDate: string, endDate: string) => {
    setStartDate(startDate);
    setEndDate(endDate);
    console.log('Filtrando dados de:', startDate, 'até:', endDate);
  };

  return (
    <div>
      <NavBar />
      <main className="p-8 bg-gray-100 min-h-screen">
        <h1 className="text-4xl font-bold mb-8">Dashboard</h1>

        {/* Filtro de Data */}
        <div className="mb-8">
          <DateFilter onFilter={handleDateFilter} />
        </div>

        {/* Cards de Estatísticas */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <DashboardCard
            title="Total Falhas - Janeiro"
            value="1,200"
            icon={<i className="fas fa-users"></i>}
          />
          <DashboardCard
            title="Total Carros"
            value="40,000"
            icon={<i className="fas fa-car"></i>}
          />
          <DashboardCard
            title="Novas Falhas"
            value="320"
            icon={<i className="fas fa-exclamation-triangle"></i>}
          />
          <DashboardCard
            title="Falhas Hoje"
            value="12"
            icon={<i className="fas fa-tasks"></i>}
          />
        </div>

        {/* Gráficos */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Carros e Falhas Detectadas por Mês</h2>
            <CarFailureChart />
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Acumulação de Ocorrências de Status</h2>
            <AreaStatusChart />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Sem Falha vs Com Falha</h2>
            <Graph3 />
          </div>
      
      </main>
    </div>
  );
};

export default App;
