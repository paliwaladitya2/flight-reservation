import React, { useEffect, useState } from "react";
import api from "../services/api";
import "./MyBookings.css";

const MyBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const response = await api.getMyBookings(); // Call updated API
        if (response.error) {
          setMessage(response.error);
        } else if (response.bookings.length === 0) {
          setMessage("You have no bookings.");
        } else {
          setBookings(response.bookings);
          setMessage("");
        }
      } catch (error) {
        setMessage("Error fetching bookings.");
      }
    };
    fetchBookings();
  }, []);  

  const handleCancelBooking = async (bookingId) => {
    try {
      const response = await api.cancelBooking({ booking_id: bookingId }); // Pass as object
      if (response.error) {
        alert(`Error: ${response.error}`);
      } else {
        alert("Booking cancelled successfully!");
        // Refresh bookings list
        const updatedBookings = await api.getMyBookings();
        setBookings(updatedBookings.bookings);
        if (updatedBookings.bookings.length === 0) {
          setMessage("You have no bookings.");
        }
      }
    } catch (error) {
      alert("Error cancelling booking.");
    }
  };

  return (
    <div>
      <h2>My Bookings</h2>
      {message && <p>{message}</p>}
      {bookings.length > 0 && !message ? (
        <table className="bookings-table">
          <thead>
            <tr>
              <th>Flight Number</th>
              <th>Departure</th>
              <th>Arrival</th>
              <th>Fare</th>
              <th>Booked At</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {bookings.map((booking) => (
              <tr key={booking.id}>
                <td>{booking.flight_number}</td>
                <td>{booking.departure}</td>
                <td>{booking.arrival}</td>
                <td>${booking.fare}</td>
                <td>{new Date(booking.booked_at).toLocaleString()}</td>
                <td>
                  <button
                    onClick={() => handleCancelBooking(booking.id)}
                    className="cancel-booking-button"
                  >
                    Cancel
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
    </div>
  );
};

export default MyBookings;