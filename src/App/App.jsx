import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import StudentsPage from './StudentsPage';
import TasksPage from './TasksPage';
import TaskDetailPage from './TaskDetailPage';
import './style.css';


export const App = () => {
  return (
    <Router>
      <div className="app-container">
        <div className="app-content">
          <h1 className="app-title">Navigation</h1>
          <nav className="app-nav">
            <Link to="/students" className="app-nav-link">
              Students Page
            </Link>
            <Link to="/tasks" className="app-nav-link">
              Tasks Page
            </Link>
          </nav>

          <Routes>
            <Route path="/students"  element={<StudentsPage/>}/>
            <Route path="/tasks" element={<TasksPage/>}/>" 
            <Route path="/tasks/:taskId" element={<TaskDetailPage/>}/> 

          </Routes>
        </div>
      </div>
    </Router>
  );
};





