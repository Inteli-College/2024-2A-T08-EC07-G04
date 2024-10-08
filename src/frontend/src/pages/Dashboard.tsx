import { useEffect, useState } from 'react';
import axios, { AxiosResponse } from 'axios';
import CarFailureChart from '../components/Graph';
import AreaStatusChart from '../components/Graph2';

interface DashboardCardProps {
  title: string;
  value: string;
  icon: JSX.Element;
}

const DashboardCard: React.FC<DashboardCardProps> = ({ title, value, icon }) => (
  <div className="bg-gradient-to-br from-white to-gray-50 p-6 rounded-lg shadow-md flex items-center space-x-4 transition duration-300 transform hover:scale-105 hover:shadow-lg">
    <div className="text-blue-500 text-4xl">{icon}</div>
    <div>
      <h3 className="text-2xl font-semibold">{title}</h3>
      <p className="text-gray-600 text-lg">{value}</p>
    </div>
  </div>
);

const Dashboard = () => {
  const [carFailureData, setCarFailureData] = useState<any[]>([]);
  const [statusData, setStatusData] = useState<any[]>([]);
  const [weeklyPredictions, setWeeklyPredictions] = useState<number>(0);
  const [dailyPredictions, setDailyPredictions] = useState<number>(0);
  const [uniqueKnrLastMonth, setUniqueKnrLastMonth] = useState<number>(0);
  const [predictionsLastMonth, setPredictionsLastMonth] = useState<number>(0);

  useEffect(() => {
    axios.get('/dashboard/knr_5_months')
      .then((response: AxiosResponse<any[]>) => setCarFailureData(response.data))
      .catch((error: any) => console.error('Erro ao buscar KNR 5 meses:', error));

    axios.get('/dashboard/week')
      .then((response: AxiosResponse<number>) => setWeeklyPredictions(response.data))
      .catch((error: any) => console.error('Erro ao buscar previsões semanais:', error));

    axios.get('/dashboard/day')
      .then((response: AxiosResponse<number>) => setDailyPredictions(response.data))
      .catch((error: any) => console.error('Erro ao buscar previsões diárias:', error));

    axios.get('/dashboard/knr_month')
      .then((response: AxiosResponse<number>) => setUniqueKnrLastMonth(response.data))
      .catch((error: any) => console.error('Erro ao buscar KNR do mês passado:', error));

    axios.get('/dashboard/predictions_month')
      .then((response: AxiosResponse<number>) => setPredictionsLastMonth(response.data))
      .catch((error: any) => console.error('Erro ao buscar previsões do mês passado:', error));

    axios.get('/dashboard/status_data')
      .then((response: AxiosResponse<any[]>) => setStatusData(response.data))
      .catch((error: any) => console.error('Erro ao buscar dados de status:', error));
  }, []);

  return (
    <div>
      <main className="p-8 bg-gray-100 min-h-screen">
        <h1 className="text-4xl font-bold mb-8 text-center">Dashboard</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <DashboardCard title="Falhas na Semana" value={weeklyPredictions.toString()} icon={<i className="fas fa-chart-line"></i>} />
          <DashboardCard title="Falhas no Dia" value={dailyPredictions.toString()} icon={<i className="fas fa-calendar-day"></i>} />
          <DashboardCard title="KNR Mês Passado" value={uniqueKnrLastMonth.toString()} icon={<i className="fas fa-car"></i>} />
          <DashboardCard title="Previsões Mês Passado" value={predictionsLastMonth.toString()} icon={<i className="fas fa-exclamation-triangle"></i>} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Carros e Falhas Detectadas nos Últimos 5 Meses</h2>
            <CarFailureChart data={carFailureData} />
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Acumulação de Ocorrências de Status</h2>
            <AreaStatusChart data={statusData} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
