import React, { Component } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./components/Login";
import AirlineReservation from "./components/AirlineReservation";
import RegistrationForm from "./components/RegistrationForm";
import PassengerDetails from "./components/PassengerDetails";
import Checkout from "./components/Checkout";
import MyBookings from "./components/MyBookings";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: false,
      users: [],
      bookedFlights: [],
      selectedFlight: null,
    };
  }

  componentDidMount() {
    const storedUsers = JSON.parse(localStorage.getItem("users")) || [];
    this.setState({ users: storedUsers });
  }

  handleRegister = (newUser) => {
    const { username } = newUser;

    const isDuplicate = this.state.users.some(
      (user) => user.username.trim().toLowerCase() === username.trim().toLowerCase()
    );

    if (isDuplicate) {
      alert("Username already exists. Please choose a different one.");
      return false;
    }

    const updatedUsers = [...this.state.users, newUser];
    localStorage.setItem("users", JSON.stringify(updatedUsers));
    this.setState({ users: updatedUsers });

    return true;
  };

  handleLogin = (username, password) => {
    const userExists = this.state.users.some(
      (user) =>
        user.username.trim().toLowerCase() === username.trim().toLowerCase() &&
        user.password === password
    );

    if (userExists) {
      this.setState({ isLoggedIn: true });
      return true;
    } else {
      return false;
    }
  };

  handleLogout = () => {
    this.setState({ isLoggedIn: false });
    window.location.href = "/login";
  };

  handleBookNow = (flight, navigate) => {
    this.setState({ selectedFlight: flight }, () => {
      navigate("/passenger-details");
    });
  };

  render() {
    const { isLoggedIn, selectedFlight } = this.state;

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
            element={<Login onLogin={this.handleLogin} />}
          />

          {/* Registration Page */}
          <Route
            path="/register"
            element={<RegistrationForm onRegister={this.handleRegister} />}
          />

          {/* Airline Reservation (Homepage) */}
          {isLoggedIn && (
            <Route
              path="/homepage"
              element={
                <AirlineReservation
                  onLogout={this.handleLogout}
                  onBookNow={(flight, navigate) => this.handleBookNow(flight, navigate)}
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
  }
}

export default App;
