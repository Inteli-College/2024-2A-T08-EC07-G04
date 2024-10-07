import React from 'react';
import NavBar from '../components/NavBar'; // Assumindo que você já tem o componente
import Graphs from '../components/Graph';

const Dashboard: React.FC = () => {
    return (
        <div>
            <NavBar />
            <div className="container mx-auto mt-10">
                <h1 className="text-3xl font-bold mb-4">Dashboard de Previsões</h1>
                <Graphs />
            </div>
        </div>
    );
};

export default Dashboard;
