import React, { Component } from "react";
import "./RegistrationForm.css"; // CSS for styling
import { Link } from "react-router-dom";

class RegistrationForm extends Component {
    constructor(props) {
      super(props);
      this.state = {
        username: "",
        password: "",
        email: "",
        
        
      };
    }
    
  
    handleInputChange = (event) => {
      const { name, value } = event.target;
      this.setState({ [name]: value });
    };
  
    handleSubmit = (event) => {
        event.preventDefault();
        const { username, password, email } = this.state;
      
        const isRegistered = this.props.onRegister({ username, password, email });
        if (isRegistered) {
          alert("Registration successful!");
          this.setState({ username: "", password: "", email: "" }); // Clear fields
          window.location.href = "/login"; // Or use React Router's navigation
        } else {
          alert("Registration failed. Username might already exist.");
        }
      };
      
      
  
    render() {
      const { username, password, email } = this.state;
        console.log(this);
      return (
        <div>
          <h2>Register</h2>
          <form onSubmit={this.handleSubmit}>
            <div>
              <label>Username:</label>
              <input
                type="text"
                name="username"
                value={username}
                onChange={this.handleInputChange}
                placeholder="Enter username"
                required
              />
            </div>
            <div>
              <label>Password:</label>
              <input
                type="password"
                name="password"
                value={password}
                onChange={this.handleInputChange}
                placeholder="Enter password"
                required
              />
            </div>
            
            <div>
              <label>Email:</label>
              <input
                type="email"
                name="email"
                value={email}
                onChange={this.handleInputChange}
                placeholder="Enter email"
                required
              />
            </div>
            <button type="submit">Register</button>
            
          </form>
          <Link to="/login">
            <button>Back to Login</button>
          </Link>
        </div>
      );
    }
  }
  
  export default RegistrationForm;
