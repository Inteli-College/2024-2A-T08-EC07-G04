import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const data = [
  { kn: 'KNR001', status_10: 120, status_13: 30 },
  { kn: 'KNR002', status_10: 90, status_13: 50 },
  { kn: 'KNR003', status_10: 70, status_13: 40 },
  { kn: 'KNR004', status_10: 50, status_13: 60 },
];

const StatusChart: React.FC = () => {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h2 className="text-xl font-bold text-gray-800 mb-4 text-center">Status 10 (Sem Falha) vs Status 13 (Com Falha)</h2>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="kn" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="status_10" fill="#2f94bf" name="Sem Falha (Status 10)" />
          <Bar dataKey="status_13" fill="#ff4d4d" name="Com Falha (Status 13)" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default StatusChart;
