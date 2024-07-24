import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';


const TasksPage = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/tasks') 
      .then((res) => res.json())
      .then((data) => setTasks(data));
  }, []);

  return (
    <div className="tasks-page">
      <h1>Tasks</h1>
      <table className="table">
        <thead>
          <tr>
            <th>Task ID</th>
            <th>Name</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => (
            <tr key={task.id}>
              <td>{task.id}</td>
              <td>
                <Link to={`/tasks/${task.id}`}>{task.name}</Link>
              </td>
              <td>{task.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TasksPage;
