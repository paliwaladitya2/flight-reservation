import React, { useState, useEffect } from "react";
import { fetchBookings } from "../api"; // Import the API call
import { getAuthToken } from "../auth"; // Import authentication utilities
import "./MyBookings.css"; // Optional: Include CSS for styling

const MyBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadBookings = async () => {
      try {
        const token = getAuthToken(); // Get the user's token from storage
        const response = await fetchBookings(token); // Fetch bookings from the backend
        setBookings(response.data.my_bookings); // Set bookings in state
      } catch (err) {
        setError("Failed to fetch bookings. Please try again.");
      } finally {
        setLoading(false); // Stop the loading spinner
      }
    };

    loadBookings();
  }, []);

  if (loading) {
    return <p>Loading your bookings...</p>; // Loading state
  }

  if (error) {
    return <p className="error-message">{error}</p>; // Error state
  }

  return (
    <div className="my-bookings">
      <h2>My Bookings</h2>
      {bookings.length > 0 ? (
        <div className="booking-list">
          {bookings.map((booking) => (
            <div key={booking.id} className="booking-card">
              <p>
                <strong>From:</strong> {booking.flight_number} - {booking.departure}
              </p>
              <p>
                <strong>To:</strong> {booking.arrival}
              </p>
              <p>
                <strong>Booked At:</strong> {new Date(booking.booked_at).toLocaleString()}
              </p>
              <p>
                <strong>Price:</strong> ${booking.fare}
              </p>
            </div>
          ))}
        </div>
      ) : (
        <p>You have no bookings yet.</p>
      )}
    </div>
  );
};

export default MyBookings;