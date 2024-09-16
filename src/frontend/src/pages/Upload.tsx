import React from 'react';
import NavBar from '../components/NavBar';
import FileUpload from '../components/Upload';

const App: React.FC = () => {
  return (
    <div>
      <NavBar />
      <main className="p-8 bg-gray-100 min-h-screen">
        <FileUpload />
      </main>
    </div>
  );
};

export default App;
