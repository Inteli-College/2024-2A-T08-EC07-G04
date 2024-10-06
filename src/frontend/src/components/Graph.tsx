import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  ResponsiveContainer,
  BarChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  Bar
} from 'recharts';

interface CarData {
  month: string;
  totalCars: number;
  faultyCars: number;
}

const CarFailureChart: React.FC = () => {
  const [data, setData] = useState<CarData[]>([]);

  useEffect(() => {
    axios.get('/api/dashboard/knr_5_months')
      .then((response) => {
        const formattedData = response.data.map((item: any) => ({
          month: item.month,
          totalCars: item.totalCars,
          faultyCars: item.faultyCars,
        }));
        setData(formattedData);
      })
      .catch((error) => {
        console.error('Erro ao buscar dados:', error);
      });
  }, []);

  return (
    <div className="bg-gradient-to-br from-white to-gray-100 p-6 rounded-xl shadow-lg transition duration-300 ease-in-out transform hover:scale-105">
      <h2 className="text-2xl font-bold text-gray-700 mb-6 text-center">Falhas de Carros por Mês</h2>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis dataKey="month" tick={{ fill: '#555555' }} />
          <YAxis tick={{ fill: '#555555' }} />
          <Tooltip contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #dddddd', borderRadius: '8px', padding: '10px' }} />
          <Legend verticalAlign="top" wrapperStyle={{ paddingBottom: 10 }} />
          <Bar dataKey="totalCars" fill="#2f94bf" name="Total de Carros" radius={[10, 10, 0, 0]} animationDuration={1500} />
          <Bar dataKey="faultyCars" fill="#ff4d4d" name="Carros com Falha" radius={[10, 10, 0, 0]} animationDuration={1500} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CarFailureChart;
