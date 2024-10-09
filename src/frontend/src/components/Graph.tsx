import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface PredictionData {
    carros: number;
    falhas: number;
    mes: string;
}

interface ApiResponse {
    [key: string]: {
        carros: number;
        falhas: number;
    };
}

const Graphs: React.FC = () => {
    const [monthlyData, setMonthlyData] = useState<PredictionData[]>([]);

    // Função para converter números de meses em nomes
    const getMonthName = (monthNumber: number) => {
        const months = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ];
        return months[monthNumber - 1]; // Ajuste para índice zero
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get<ApiResponse>('http://100.29.57.65:8001/dashboard/knr_5_months');

                // Verifique o que está sendo retornado pela API
                console.log("API Response:", response.data);

                const data = Object.entries(response.data).map(([key, value]) => {
                    // Extrai o número do mês da string "mesX"
                    const monthNumber = parseInt(key.replace('mes', ''), 10);

                    // Converte o número para o nome do mês
                    const monthName = getMonthName(monthNumber);

                    return {
                        mes: monthName,
                        carros: value.carros,
                        falhas: value.falhas,
                    };
                });

                setMonthlyData(data);
            } catch (error) {
                console.error("Error fetching data: ", error);
            }
        };

        fetchData();
    }, []);

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white p-4 rounded-lg shadow-md">
                <h2 className="text-xl font-bold mb-4">Carros Únicos nos Últimos 5 Meses</h2>
                <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={monthlyData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="mes" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="carros" stroke="#8884d8" activeDot={{ r: 8 }} />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            <div className="bg-white p-4 rounded-lg shadow-md">
                <h2 className="text-xl font-bold mb-4">Falhas Previstos nos Últimos 5 Meses</h2>
                <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={monthlyData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="mes" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="falhas" stroke="#82ca9d" activeDot={{ r: 8 }} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default Graphs;
