import React, { Component } from "react";
import { withRouter } from "./withRouter"; // Ensure this is imported correctly

class Checkout extends Component {
  constructor(props) {
    super(props);

    // Safely access location.state
    const state = props.location?.state;

    this.state = {
      passenger: state?.passenger || { name: "", age: "", passport: "" },
      flightId: state?.flightId || "Unknown Flight",
    };
  }

  render() {
    const { passenger, flightId } = this.state;

    // If passenger details are missing, show an error message
    if (!passenger.name) {
      return (
        <div className="checkout-container">
          <p>No passenger details found. Please go back and fill the form.</p>
        </div>
      );
    }

    return (
      <div className="checkout-container">
        <h2>Checkout</h2>
        <div className="checkout-details">
          <h3>Passenger Details</h3>
          <p><strong>Name:</strong> {passenger.name}</p>
          <p><strong>Age:</strong> {passenger.age}</p>
          <p><strong>Passport Number:</strong> {passenger.passport}</p>
          <h3>Flight Details</h3>
          <p><strong>Flight ID:</strong> {flightId}</p>
        </div>
        <button className="checkout-button">Confirm Booking</button>
      </div>
    );
  }
}

export default withRouter(Checkout);
