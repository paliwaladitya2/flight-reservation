import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser } from "../api";
import "./Login.css";

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name === "username") setUsername(value);
    if (name === "password") setPassword(value);
    setErrorMessage(""); // Clear error message on input change
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Call the backend API for login
      const response = await loginUser({ username, password });
      const token = response.data.token;

      // Trigger login action and navigate to homepage
      onLogin(token);
      navigate("/homepage");
    } catch (error) {
      setErrorMessage(
        error.response?.data?.message || "Invalid username or password."
      );
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2 className="login-title">Welcome Back</h2>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Username</label>
            <input
              type="text"
              name="username"
              value={username}
              onChange={handleInputChange}
              placeholder="Enter your username"
              required
            />
          </div>
          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={password}
              onChange={handleInputChange}
              placeholder="Enter your password"
              required
            />
          </div>
          <button type="submit" className="login-button">
            Login
          </button>
        </form>
        <div className="register-link">
          <p>
            Don't have an account?{" "}
            <Link to="/register" className="register-link-button">
              Register
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;