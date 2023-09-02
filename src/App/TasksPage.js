import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';


const TasksPage = () => {
  const [tasks, setTasks] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [newTaskName, setNewTaskName] = useState('');
  const [newTaskDeadline, setNewTaskDeadline] = useState(new Date().toISOString().split('T')[0]);
  const [newTaskWeight, setNewTaskWeight] = useState(1);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = () => {
    fetch('http://127.0.0.1:5000/tasks') 
      .then((res) => res.json())
      .then((data) => setTasks(data));
  };


  const handleFormSubmit = (e) => {
    e.preventDefault();

    const newTask = {
      name: newTaskName,
      deadline: newTaskDeadline,
      weight: newTaskWeight,
    };
    console.log(newTaskDeadline)

    fetch('http://127.0.0.1:5000/add_task', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newTask),
    })
    .then((response) => response.json())
    .then((data) => {
      console.log('New task added:', data);
      fetchTasks(); 
    });

    setNewTaskName('');
    setNewTaskDeadline(new Date().toISOString().split('T')[0]);
    setShowForm(false);
  };

  return (
    <div className="tasks-page">
      <h1>Tasks</h1>
      <table className="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Status</th>
            <th>Deadline</th>
            <th>Weight</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => (
            <tr key={task.id}>
              <td>
                <Link to={`/tasks/${task.name}`}>{task.name}</Link>
                {console.log("task.name",task.id)}
              </td>
              <td>{task.status}</td>
              <td>{task.deadline}</td>
              <td>{task.weight}</td>

            </tr>
          ))}
        </tbody>
      </table>
      <div className="content-below-table" style={{ marginTop: '10px' }}>
      {showForm ? (
        <form className="new-task-form" onSubmit={handleFormSubmit}>
          <label className="app-form-label">
            Task Name:
            <input
              className="app-form-input"
              type="text"
              value={newTaskName}
              onChange={(e) => setNewTaskName(e.target.value)}
            />
          </label>
          <label className="app-form-label">
            Deadline:
            <input
              className="app-form-input"
              type="date"
              value={newTaskDeadline}
              onChange={(e) => setNewTaskDeadline(e.target.value)}
            />
          </label>
          <label className="app-form-label">
            Weight:
            <input
              className="app-form-input"
              type="number"
              value={newTaskWeight}
              onChange={(e) => setNewTaskWeight(e.target.value)}
            />
          </label>
          <button className="app-button" type="submit">Create Task</button>
          <button className="app-button" type="button" onClick={() => setShowForm(false)}>Cancel</button>
        </form>
      ) : (
        <button className="app-button" onClick={() => setShowForm(true)}>New Task</button>
      )}
    </div>
    </div>
  );
};

export default TasksPage;