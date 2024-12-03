import React, { Component } from "react";
import { withRouter } from "./withRouter";

class PassengerDetails extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: "",
      age: "",
      passport: "",
    };
  }

  handleInputChange = (event) => {
    const { name, value } = event.target;
    this.setState({ [name]: value });
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { flight, onBookingComplete } = this.props;
    const { name, age, passport } = this.state;

    if (name && age && passport) {
      const booking = { ...flight, passenger: { name, age, passport } };
      onBookingComplete(booking);
      this.props.navigate("/my-bookings");
    } else {
      alert("Please fill out all fields.");
    }
  };

  render() {
    const { flight, navigate } = this.props;

    if (!flight) {
      return <p>No flight selected. Please go back and select a flight.</p>;
      <button onClick={() => navigate("/")}>Go Back</button>
    }

    return (
      <div className="passenger-details-container">
        <h2>Passenger Details</h2>
        <p>Booking for Flight: <strong>{flight.from} to {flight.to}</strong></p>
        <form onSubmit={this.handleSubmit}>
          <div className="input-group">
            <label>Name</label>
            <input
              type="text"
              name="name"
              value={this.state.name}
              onChange={this.handleInputChange}
              placeholder="Enter your name"
              required
            />
          </div>
          <div className="input-group">
            <label>Age</label>
            <input
              type="number"
              name="age"
              value={this.state.age}
              onChange={this.handleInputChange}
              placeholder="Enter your age"
              required
            />
          </div>
          <div className="input-group">
            <label>Passport Number</label>
            <input
              type="text"
              name="passport"
              value={this.state.passport}
              onChange={this.handleInputChange}
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
  }
}

export default withRouter(PassengerDetails);