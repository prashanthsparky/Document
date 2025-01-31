import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import Registration from './components/Registration';
import Login from './components/Login';
import FileUpload from './components/FileUpload';
import CustomForm from './components/CustomForm';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await fetch('http://localhost:5001/verify-token', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`, // Attach token to the request
            },
          });

          if (response.ok) {
            setIsAuthenticated(true);
          } else {
            localStorage.removeItem('token');
            setIsAuthenticated(false);
          }
        } catch (error) {
          console.error('Token verification failed:', error);
          localStorage.removeItem('token');
          setIsAuthenticated(false);
        }
      }
    };

    verifyToken();
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleRegister = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          {isAuthenticated ? (
            <>
              <ul>
                <li><Link to="/file-upload">File Upload</Link></li>
                <li><Link to="/custom-form">Custom Form</Link></li>
              </ul>
              <button onClick={handleLogout}>Logout</button>
            </>
          ) : (
            <ul>
              <li><Link to="/login">Login</Link></li>
              <li><Link to="/register">Register</Link></li>
            </ul>
          )}
        </nav>
        <div className="content">
          <Routes>
            <Route path="/" element={isAuthenticated ? <Navigate to="/file-upload" /> : <Navigate to="/login" />} />
            <Route path="/register" element={<Registration onRegister={handleRegister} />} />
            <Route path="/login" element={!isAuthenticated ? <Login onLogin={handleLogin} /> : <Navigate to="/file-upload" />} />
            <Route path="/file-upload" element={isAuthenticated ? <FileUpload onLogout={handleLogout} /> : <Navigate to="/login" />} />
            <Route path="/custom-form" element={isAuthenticated ? <CustomForm /> : <Navigate to="/login" />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
