import React, { useState } from 'react';
import Navbar from '../navbar';
import './register.css';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();

    const response = await fetch('http://localhost:5001/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password, confirm_password: confirmPassword, email }),
    });

    if (response.ok) {
      // Redirect to homepage on successful registration
      window.location.href = '/'; // Redirect to homepage
    } else {
      const data = await response.json();
      setStatus(data.error);
    }
  };

  return (
    <div className="registerContainer">
      <Navbar/>
      <div className="registerForm">
        <h1>Register</h1>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
        />
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Confirm Password"
          required
        />
        <button onClick={handleRegister}>Register</button>
        <p>{status}</p>
      </div>
    </div>
  );
};

export default Register;
