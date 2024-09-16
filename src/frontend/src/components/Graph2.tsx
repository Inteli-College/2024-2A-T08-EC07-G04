import React from 'react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from 'recharts';

const data = [
  { month: 'Jan', status_10: 20, status_13: 15, status_718: 30 },
  { month: 'Feb', status_10: 30, status_13: 25, status_718: 35 },
  { month: 'Mar', status_10: 50, status_13: 30, status_718: 40 },
  { month: 'Apr', status_10: 60, status_13: 40, status_718: 50 },
];

const AreaStatusChart: React.FC = () => {
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
