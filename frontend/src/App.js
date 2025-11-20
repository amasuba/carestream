// src/App.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [sessions, setSessions] = useState([]);
  useEffect(() => {
    axios.get('http://localhost:8000/api/sessions/').then(res => setSessions(res.data));
  }, []);
  return (
    <div>
      <h1>CareStream360 Dashboard</h1>
      <ul>
        {sessions.map(sess => (
          <li key={sess.id}>
            {sess.customer} | {sess.qoe_score} | {sess.status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
