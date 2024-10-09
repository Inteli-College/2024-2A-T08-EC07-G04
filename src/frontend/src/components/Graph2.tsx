import React from 'react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from 'recharts';

// Define the props type
interface AreaStatusChartProps {
  data: { month: string; status_10: number; status_13: number; status_718: number }[]; // Adjust the types based on your actual data
}

const AreaStatusChart: React.FC<AreaStatusChartProps> = ({ data }) => {
  return (
    <div className="bg-gray-100 p-6 rounded-xl shadow-lg">
      <h2 className="text-2xl font-semibold text-gray-700 mb-4 text-center">
        Acumulação de Ocorrências de Status
      </h2>
      <ResponsiveContainer width="100%" height={400}>
        <AreaChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis dataKey="month" stroke="#808080" />
          <YAxis stroke="#808080" />
          <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderRadius: '10px', borderColor: '#d0d0d0' }} />
          <Legend verticalAlign="top" height={36} iconType="circle" />
          <Area type="monotone" dataKey="status_10" stackId="1" stroke="#5b8bf7" fill="rgba(91, 139, 247, 0.2)" />
          <Area type="monotone" dataKey="status_13" stackId="1" stroke="#f77474" fill="rgba(247, 116, 116, 0.2)" />
          <Area type="monotone" dataKey="status_718" stackId="1" stroke="#6bcf95" fill="rgba(107, 207, 149, 0.2)" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AreaStatusChart;
