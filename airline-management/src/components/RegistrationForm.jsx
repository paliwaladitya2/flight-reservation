import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import "./RegistrationForm.css";

const RegistrationForm = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    phone_number: "",
  });

  const [message, setMessage] = useState("");
  const navigate = useNavigate(); // React Router's hook for navigation

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await api.register(formData);
    if (response.error) {
      setMessage(response.error);
    } else {
      setMessage("Registration successful! Redirecting to login...");
      setTimeout(() => {
        navigate("/login"); // Redirect to login page after 2 seconds
      }, 2000);
    }
  };

  return (
    <div className="registration-form">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="phone_number"
          placeholder="Phone Number"
          value={formData.phone_number}
          onChange={handleChange}
        />
        <button type="submit">Register</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default RegistrationForm;