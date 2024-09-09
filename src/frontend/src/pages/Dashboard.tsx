import React, { useState } from 'react';
import NavBar from '../components/NavBar';
import DateFilter from '../components/DateFilter'; // Import do componente de filtro de data

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

const App: React.FC = () => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const handleDateFilter = (startDate: string, endDate: string) => {
    setStartDate(startDate);
    setEndDate(endDate);
    console.log('Filtering data from:', startDate, 'to:', endDate);
    // Aqui você pode realizar a lógica de filtragem dos dados com base nas datas selecionadas
  };

  return (
    <div>
      <NavBar />
      <main className="p-8 bg-gray-100 min-h-screen">
        <h1 className="text-4xl font-bold mb-8">Dashboard</h1>

        {/* Componente de Filtro de Data */}
        <div className="mb-8">
          <DateFilter onFilter={handleDateFilter} />
        </div>

        {/* Cards de Estatísticas */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <DashboardCard
            title={`Total Falhas - Janeiro`}
            value="1,200"
            icon={<i className="fas fa-users"></i>}
          />
          <DashboardCard
            title="Total Carros"
            value="40,000"
            icon={<i className="fas fa-dollar-sign"></i>}
          />
          <DashboardCard
            title="Novas Falhas"
            value="320"
            icon={<i className="fas fa-shopping-cart"></i>}
          />
          <DashboardCard
            title="Falhas Hoje"
            value="12"
            icon={<i className="fas fa-tasks"></i>}
          />
        </div>

        {/* Gráficos Placeholder */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Sales Overview</h2>
            <div className="h-64 bg-gray-200 flex items-center justify-center">
              {/* Placeholder for Chart */}
              <span className="text-gray-500">[Chart]</span>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">User Engagement</h2>
            <div className="h-64 bg-gray-200 flex items-center justify-center">
              {/* Placeholder for Chart */}
              <span className="text-gray-500">[Chart]</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;
