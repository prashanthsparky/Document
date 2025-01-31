  import React, { useState } from 'react';
  import { useNavigate } from 'react-router-dom';

  function Login({ onLogin }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
      e.preventDefault();

      try {
        const response = await fetch('http://localhost:5001/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, password }),
        });

        const data = await response.json();

        if (response.ok) {
          localStorage.setItem('token', data.token); // Store the token
          onLogin();
          navigate('/file-upload'); // Redirect to file upload page after successful login
        } else {
          setError(data.error || 'An error occurred');
        }
      } catch (err) {
        setError('An error occurred. Please try again later.');
      }
    };

    return (
      <div className="container">
        <h1>Login</h1>
        <form onSubmit={handleSubmit} className="custom-form">
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Login</button>
          {error && <p className="error-message">{error}</p>}
        </form>
      </div>
    );
  }

  export default Login;