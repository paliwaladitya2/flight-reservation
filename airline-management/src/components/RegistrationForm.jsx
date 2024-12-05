import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../api"; // Import API call
import "./RegistrationForm.css"; // CSS for styling

const RegistrationForm = () => {
  const [formData, setFormData] = useState({ username: "", password: "", phone_number: "" });
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const navigate = useNavigate();

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
    setErrorMessage(""); // Clear error on input change
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      // Call the backend API for registration
      const response = await registerUser(formData);
      setSuccessMessage(response.data.message);
      setFormData({ username: "", password: "", phone_number: "" }); // Clear the form
      setTimeout(() => navigate("/login"), 2000); // Redirect to login after success
    } catch (error) {
      setErrorMessage(
        error.response?.data?.message || "Registration failed. Please try again."
      );
    }
  };

  return (
    <div className="registration-container">
      <div className="registration-box">
        <h2>Register</h2>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Username:</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              placeholder="Enter username"
              required
            />
          </div>
          <div className="input-group">
            <label>Password:</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Enter password"
              required
            />
          </div>
          <div className="input-group">
            <label>Phone Number:</label>
            <input
              type="text"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleInputChange}
              placeholder="Enter phone number"
              required
            />
          </div>
          <button type="submit" className="register-button">
            Register
          </button>
        </form>
        <div className="login-link">
          <Link to="/login">
            <button className="back-to-login-button">Back to Login</button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default RegistrationForm;