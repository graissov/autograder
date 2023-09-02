import React, { useState, useEffect } from 'react';

const BonusesPage = () => {
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [selectedBonuses, setSelectedBonuses] = useState([]);
  const [availableBonuses, setAvailableBonuses] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/students')
      .then((res) => res.json())
      .then((data) => setStudents(data));
  }, []);

  useEffect(() => {
    fetchBonuses();
  }, []);

  const fetchBonuses = () => {
    fetch('http://127.0.0.1:5000/get_bonuses')
      .then((res) => {
        if (!res.ok) {
          throw new Error('Network response was not ok');
        }
        return res.json();
      })
      .then((data) => {
        console.log('Fetched Bonuses:', data);
        setAvailableBonuses(data);
      })
      .catch((error) => {
        console.error('Error fetching bonuses:', error);
      });
  };
  
  
  const handleStudentClick = (student) => {
    setSelectedStudent(student);
    console.log(student,"click")
    setSelectedBonuses([]); 
  };

  const handleCheckboxChange = (value) => {
    setSelectedBonuses(
        [...selectedBonuses, value]
      
    );
  };
  

  const handleSubmit = () => {
    if (!selectedStudent) {
      console.error('No student selected.');
      return;
    }

    const studentIdentifier = selectedStudent.andrewid;
    const postData = {
      studentIdentifier,
      selectedBonuses,
    };

    fetch('http://127.0.0.1:5000/save_student_bonuses', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postData),
    })
      .then((res) => res.json())
      .then((response) => {
        console.log('Saved bonuses for student:', response);
      })
      .catch((error) => {
        console.error('Error saving student bonuses:', error);
      });
  };
  
  return (
    <div>
      <h1>Bonuses</h1>
      <div>
        <h2>Select a student</h2>
        <ul>
          {students.map((student) => (
            <li key={student.andrewid} onClick={() => handleStudentClick(student)}>
              {student.name}
              {selectedStudent && selectedStudent.andrewid === student.andrewid && (
                <div>
                  <h3>Select Bonuses</h3>
                  {console.log("bonuses",availableBonuses)}
                  {availableBonuses.map((bonus) => (
                    <div key={bonus.description}>
                      <label>
                        <input
                          type="checkbox"
                          value={bonus}
                          checked={selectedBonuses.includes(bonus)}
                          onChange={() => handleCheckboxChange(bonus)}
                        />
                        {bonus.description}
                      </label>
                    </div>
                  ))}
                  <button onClick={handleSubmit}>Submit</button>
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default BonusesPage;