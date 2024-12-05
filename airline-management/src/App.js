import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./components/Login";
import AirlineReservation from "./components/AirlineReservation";
import RegistrationForm from "./components/RegistrationForm";
import PassengerDetails from "./components/PassengerDetails";
import Checkout from "./components/Checkout";
import MyBookings from "./components/MyBookings";
import { getAuthToken, saveAuthToken, removeAuthToken } from "./auth";
import { fetchBookings } from "./api";

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!getAuthToken());
  const [selectedFlight, setSelectedFlight] = useState(null);

  useEffect(() => {
    if (isLoggedIn) {
      // Optionally preload user data, bookings, or other details here
      fetchBookings(getAuthToken()).catch((error) => {
        console.error("Error fetching bookings:", error);
        handleLogout();
      });
    }
  }, [isLoggedIn]);

  const handleLogin = (token) => {
    saveAuthToken(token);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    removeAuthToken();
    setIsLoggedIn(false);
  };

  const handleBookNow = (flight, navigate) => {
    setSelectedFlight(flight);
    navigate("/passenger-details");
  };

  return (
    <Router>
      <Routes>
        {/* Redirect root path to login or homepage */}
        <Route
          path="/"
          element={<Navigate to={isLoggedIn ? "/homepage" : "/login"} />}
        />

        {/* Login Page */}
        <Route
          path="/login"
          element={<Login onLogin={handleLogin} />}
        />

        {/* Registration Page */}
        <Route
          path="/register"
          element={<RegistrationForm />}
        />

        {/* Airline Reservation (Homepage) */}
        {isLoggedIn && (
          <Route
            path="/homepage"
            element={
              <AirlineReservation
                onLogout={handleLogout}
                onBookNow={(flight, navigate) => handleBookNow(flight, navigate)}
              />
            }
          />
        )}

        {/* Passenger Details */}
        {isLoggedIn && (
          <Route
            path="/passenger-details"
            element={<PassengerDetails flight={selectedFlight} />}
          />
        )}

        {/* My Bookings */}
        {isLoggedIn && (
          <Route
            path="/my-bookings"
            element={<MyBookings />}
          />
        )}

        {/* Checkout Page */}
        {isLoggedIn && (
          <Route
            path="/checkout"
            element={<Checkout />}
          />
        )}

        {/* Catch-all Route */}
        <Route
          path="*"
          element={<Navigate to={isLoggedIn ? "/homepage" : "/login"} />}
        />
      </Routes>
    </Router>
  );
};

export default App;