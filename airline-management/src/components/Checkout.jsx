import React, { useState, useEffect } from "react";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
import { useNavigate, useLocation } from "react-router-dom";
import "./Checkout.css";

const Checkout = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // Extract passenger and flight details from location state
  const { passenger, flightId, flightPrice, flightDetails } = location.state || {
    passenger: { name: "", age: "", passport: "" },
    flightId: "Unknown Flight",
    flightPrice: "0.00",
    flightDetails: { from: "N/A", to: "N/A", time: "N/A" },
  };

  const [paymentSuccess, setPaymentSuccess] = useState(false);

  // If passenger or flight details are missing, show an error message
  useEffect(() => {
    if (!passenger?.name || !flightId) {
      alert("Missing passenger or flight details. Please go back and fill the form.");
      navigate("/passenger-details"); // Redirect back to the passenger form
    }
  }, [passenger, flightId, navigate]);

  const handlePaymentSuccess = (details) => {
    // Perform backend operations like saving payment details
    console.log("Payment Details:", details);
    alert(`Payment successful! Transaction ID: ${details.id}`);
    setPaymentSuccess(true);
    navigate("/my-bookings"); // Redirect to bookings page
  };

  return (
    <PayPalScriptProvider
      options={{
        "client-id": "Abrw0xkAkLNHz9GVo5GeuAY2jjsfU4yqgU4TqT_LKQbNPgaC-xDZ2iIFy-8GjwQnDJWLtBfTfaUiIHXY", // Replace with your PayPal Client ID
        currency: "EUR",
      }}
    >
      <div className="checkout-container">
        <h2>Checkout</h2>
        <div className="checkout-details">
          <h3>Passenger Details</h3>
          <p><strong>Name:</strong> {passenger.name}</p>
          <p><strong>Age:</strong> {passenger.age}</p>
          <p><strong>Passport Number:</strong> {passenger.passport}</p>
          <h3>Flight Details</h3>
          <p><strong>From:</strong> {flightDetails.from}</p>
          <p><strong>To:</strong> {flightDetails.to}</p>
          <p><strong>Time:</strong> {flightDetails.time}</p>
          <p><strong>Price:</strong> ${flightPrice}</p>
        </div>

        <h3>Pay with PayPal</h3>
        <PayPalButtons
          style={{ layout: "vertical" }}
          createOrder={(data, actions) => {
            return actions.order.create({
              purchase_units: [
                {
                  amount: {
                    value: flightPrice, // Use dynamic flight price
                  },
                },
              ],
            });
          }}
          onApprove={async (data, actions) => {
            const details = await actions.order.capture();
            handlePaymentSuccess(details); // Handle successful payment
          }}
          onError={(err) => {
            console.error("PayPal Payment Error:", err);
            alert("Payment failed. Please try again.");
          }}
        />

        {paymentSuccess && <p className="success-message">Payment completed successfully!</p>}
      </div>
    </PayPalScriptProvider>
  );
};

export default Checkout;