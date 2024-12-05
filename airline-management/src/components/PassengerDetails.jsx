import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { bookFlight } from "../api"; // Import the API call
import { getAuthToken } from "../auth"; // Import authentication utilities
import "./PassengerDetails.css";

const PassengerDetails = ({ flight }) => {
  const [formData, setFormData] = useState({
    name: "",
    age: "",
    passport: "",
  });
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  if (!flight) {
    return (
      <div className="no-flight">
        <p>No flight selected. Please go back and select a flight.</p>
        <button onClick={() => navigate("/")}>Go Back</button>
      </div>
    );
  }

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
    setErrorMessage(""); // Clear error on input change
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const token = getAuthToken();
    const { name, age, passport } = formData;

    if (!name || !age || !passport) {
      setErrorMessage("Please fill out all fields.");
      return;
    }

    try {
      // Call the backend API to book the flight
      await bookFlight({ flight_id: flight.id, passenger: formData }, token);
      navigate("/my-bookings");
    } catch (error) {
      setErrorMessage(
        error.response?.data?.message || "Booking failed. Please try again."
      );
    }
  };

  return (
    <div className="passenger-details-container">
      <h2>Passenger Details</h2>
      <p>
        Booking for Flight:{" "}
        <strong>
          {flight.from} to {flight.to}
        </strong>
      </p>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label>Name</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            placeholder="Enter your name"
            required
          />
        </div>
        <div className="input-group">
          <label>Age</label>
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={handleInputChange}
            placeholder="Enter your age"
            required
          />
        </div>
        <div className="input-group">
          <label>Passport Number</label>
          <input
            type="text"
            name="passport"
            value={formData.passport}
            onChange={handleInputChange}
            placeholder="Enter passport number"
            required
          />
        </div>
        <button type="submit" className="details-button">
          Confirm Booking
        </button>
      </form>
    </div>
  );
};

export default PassengerDetails;