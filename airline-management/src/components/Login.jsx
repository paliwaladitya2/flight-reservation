import React, { Component } from "react";
import { Link, Navigate } from "react-router-dom";
import "./Login.css";

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      password: "",
      errorMessage: "",
      redirect: false, // Add redirect state
    };
  }

  handleInputChange = (event) => {
    const { name, value } = event.target;
    this.setState({ [name]: value, errorMessage: "" });
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { username, password } = this.state;

    // Call the login handler passed via props
    const loginSuccess = this.props.onLogin(username, password);

    if (loginSuccess) {
      this.setState({ redirect: true }); // Set redirect to true on success
    } else {
      this.setState({ errorMessage: "Invalid username or password." });
    }
  };

  render() {
    const { username, password, errorMessage, redirect } = this.state;

    // Redirect if login is successful
    if (redirect) {
      return <Navigate to="/homepage" />;
    }

    return (
      <div className="login-container">
        <div className="login-box">
          <h2 className="login-title">Welcome Back</h2>
          {errorMessage && <p className="error-message">{errorMessage}</p>}
          <form onSubmit={this.handleSubmit}>
            <div className="input-group">
              <label>Username</label>
              <input
                type="text"
                name="username"
                value={username}
                onChange={this.handleInputChange}
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
                onChange={this.handleInputChange}
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
  }
}

export default Login;