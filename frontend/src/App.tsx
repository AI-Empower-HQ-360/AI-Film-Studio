import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import ScriptEditor from './pages/ScriptEditor';
import Scenes from './pages/Scenes';
import Shots from './pages/Shots';
import Export from './pages/Export';
import './index.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/script" element={<ScriptEditor />} />
          <Route path="/scenes" element={<Scenes />} />
          <Route path="/shots" element={<Shots />} />
          <Route path="/export" element={<Export />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
