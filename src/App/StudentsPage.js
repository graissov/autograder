import React, { useState, useEffect } from 'react';

const StudentsPage = () => {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/students')
      .then((res) => res.json())
      .then((data) => setStudents(data));
  }, []);

  return (
    <div className="students-page">
      <h1>Students</h1>
      <table className="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {students.map((student) => (
            <tr key={student.id}>
              <td>{student.name}</td>
              <td>{student.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StudentsPage;
