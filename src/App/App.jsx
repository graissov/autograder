import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import StudentsPage from './StudentsPage';
import TasksPage from './TasksPage';
import TaskDetailPage from './TaskDetailPage';
import BonusesPage from './BonusesPage';
import './style.css';

export const App = () => {
  return (
    <Router>
      <header className="header">
            <h1 className="website-name">Grader</h1>
          </header>
      <div className="app-container">

        <div className="sidenav" id="mySidenav">
          <Link to="/students" className="sidenav-link">Students Page</Link>
          <Link to="/tasks" className="sidenav-link">Tasks Page</Link>
          <Link to="/bonuses" className="sidenav-link">Bonuses Page</Link>
        </div>
          <Routes>
            <Route path="/students" element={<StudentsPage/>}/>
            <Route path="/tasks" element={<TasksPage/>}/>
            <Route path="/tasks/:taskId" element={<TaskDetailPage/>}/>
            <Route path="/bonuses" element={<BonusesPage/>}/>
          </Routes>
      </div>
    </Router>
  );
};

// JavaScript function to open the side navigation
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

// JavaScript function to close the side navigation
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}
