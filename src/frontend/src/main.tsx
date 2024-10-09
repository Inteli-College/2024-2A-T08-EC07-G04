// main.tsx or main.js (depending on your setup)
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import  App  from './App'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import './index.css'
import NoIssuesPage from './pages/NoIssuesPage.tsx';
import IssuesPage from './pages/IssuesPage.tsx';
import Predict from './pages/Predict.tsx';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/no-issues" element={<NoIssuesPage />} />
        <Route path="/issues" element={<IssuesPage />} />
        <Route path="/predict" element={<Predict />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)