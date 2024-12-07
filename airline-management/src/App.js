import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/RegistrationForm";
import AirlineReservation from "./components/AirlineReservation";
import MyBookings from "./components/MyBookings";
import Navbar from "./components/Navbar";
import "./App.css";

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    const sessionID = sessionStorage.getItem("sessionid"); // Match key used
    if (sessionID) {
      setIsAuthenticated(true);
      setSessionId(sessionID);
    } else {
      console.error("Session ID not found. User may not be logged in.");
    }
  }, []);  
  

  const handleLogin = (sessionKey) => {
    setIsAuthenticated(true);
    setSessionId(sessionKey);
    sessionStorage.setItem('sessionID', sessionKey);  // Store session ID in sessionStorage
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    sessionStorage.removeItem('sessionID');  // Clear session ID from sessionStorage
    setSessionId(null);
  };

  return (
    <Router>
      <div className="app">
        {isAuthenticated && <Navbar onLogout={handleLogout} />}
        <Routes>
          {!isAuthenticated ? (
            <>
              <Route path="/login" element={<Login onLogin={handleLogin} />} />
              <Route path="/register" element={<Register />} />
              <Route path="*" element={<Navigate to="/login" replace />} />
            </>
          ) : (
            <>
              <Route path="/flights" element={<AirlineReservation />} />
              <Route path="/bookings" element={<MyBookings />} />
              <Route path="*" element={<Navigate to="/flights" replace />} />
            </>
          )}
        </Routes>
      </div>
    </Router>
  );
};

export default App;