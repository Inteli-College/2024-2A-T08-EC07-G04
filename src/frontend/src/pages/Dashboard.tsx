import React, { useState, useEffect } from 'react';
import NavBar from '../components/NavBar';
import Graphs from '../components/Graph';
import axios from 'axios';

const Dashboard: React.FC = () => {
    // const [weekData, setWeekData] = useState<number>(0);
    // const [dayData, setDayData] = useState<number>(0);
    const [predictionsMonthData, setPredictionsMonthData] = useState<number>(0);
    const [knrMonthData, setKnrMonthData] = useState<number>(0);
    const [accuracy, setAccuracy] = useState<number>(0);
    const [falseNegative, setFalseNegative] = useState<number>(0);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [
                    predictionsMonthResponse, 
                    knrMonthResponse, 
                    accuracyResponse, 
                    falseNegativeResponse
                ] = await Promise.all([
                    axios.get('http://localhost:8001/dashboard/predictions_month'),
                    axios.get('http://localhost:8001/dashboard/knr_month'),
                    axios.get('http://localhost:8001/dashboard/accuracy'),
                    axios.get('http://localhost:8001/dashboard/false_negatives')
                ]);
                // Fazer requisições para as rotas relevantes
                /*const [/* weekResponse, dayResponse, predictionsMonthResponse, knrMonthResponse] = await Promise.all([
                    // axios.get('http://localhost:8001/dashboard/week'),
                    // axios.get('http://localhost:8001/dashboard/day'),
                    axios.get('http://localhost:8001/dashboard/predictions_month'),
                    axios.get('http://localhost:8001/dashboard/knr_month')
                    axios.get('http://localhost:8001/dashboard/accuracy'),
                    axios.get('http://localhost:8001/dashboard/false_negatives')
                ]);*/
                console.log("Xablau")

                // Logs para depuração
                // console.log('Week Response:', weekResponse.data);
                // console.log('Day Response:', dayResponse.data);
                console.log('Predictions Month Response:', predictionsMonthResponse.data);
                console.log('KNR Month Response:', knrMonthResponse.data);
                console.log('Accuracy Response:', accuracyResponse.data);
                console.log('False Negatives Response:', falseNegativeResponse.data);

                // Atualizar estados com base na estrutura da resposta
                // setWeekData(typeof weekResponse.data === 'number' ? weekResponse.data : 0);
                // setDayData(typeof dayResponse.data === 'number' ? dayResponse.data : 0);
                setPredictionsMonthData(
                    typeof predictionsMonthResponse.data === 'number' 
                        ? predictionsMonthResponse.data 
                        : predictionsMonthResponse.data.value
                );
                setKnrMonthData(
                    typeof knrMonthResponse.data === 'number' 
                        ? knrMonthResponse.data 
                        : knrMonthResponse.data.value
                );
                setAccuracy(
                    typeof accuracyResponse.data.accuracy === 'number' 
                        ? accuracyResponse.data.accuracy 
                        : 0
                );
                setFalseNegative(
                    typeof falseNegativeResponse.data.falseNegative === 'number' 
                        ? falseNegativeResponse.data.falseNegative 
                        : 0
                );
            } catch (error) {
                console.error("Error fetching dashboard data:", error);
            }
        };

        fetchData();
    }, []);

    return (
        <div>
            <NavBar />
            <div className="container mx-auto mt-10">
                <h1 className="text-3xl font-bold mb-4">Dashboard de Previsões</h1>
                {/* Cards Section */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                    {/* <div className="bg-white shadow-md rounded-lg p-6">
                        <h2 className="text-xl font-semibold">Previsões da Semana</h2>
                        <p className="text-3xl">{weekData}</p>
                    </div>
                    <div className="bg-white shadow-md rounded-lg p-6">
                        <h2 className="text-xl font-semibold">Previsões do Dia</h2>
                        <p className="text-3xl">{dayData}</p>
                    </div> */}
                    <div className="bg-white shadow-md rounded-lg p-6">
                        <h2 className="text-xl font-semibold">Previsões do Mês</h2>
                        <p className="text-3xl">{predictionsMonthData}</p>
                    </div>
                    <div className="bg-white shadow-md rounded-lg p-6">
                        <h2 className="text-xl font-semibold">KNRs do Mês</h2>
                        <p className="text-3xl">{knrMonthData}</p>
                    </div>
                    <div className="bg-white shadow-md rounded-lg p-6">
                        <h2 className="text-xl font-semibold">Precisão do modelo</h2>
                        <p className="text-3xl">{accuracy.toFixed(2)}</p>
                    </div>
                    <div className="bg-white shadow-md rounded-lg p-6">
                        <h2 className="text-xl font-semibold">Falsos negativos</h2>
                        <p className="text-3xl">{falseNegative}</p>
                    </div>
                </div>
                <Graphs />
            </div>
        </div>
    );
};

export default Dashboard;