import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Configuration from './pages/Configuration';
import Header from './components/Header';

const App = () => (
  <>
    <Header />
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/config" element={<Configuration />} />
    </Routes>
  </>
);

export default App;