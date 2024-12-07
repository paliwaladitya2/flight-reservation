import React, { useEffect, useState } from "react";
import api from "../services/api";
import "./AirlineReservation.css";


const AirlineReservation = () => {
  const [flights, setFlights] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchFlights = async () => {
      try {
        const response = await api.getFlights();
        if (response.error) {
          setMessage(response.error); // Handle backend error
        } else {
          setFlights(response.flights);
        }
      } catch (error) {
        setMessage("Error fetching flights.");
      }
    };
    fetchFlights();
  }, []);

  const handleBookNow = (flightId) => {
    console.log(`Booking flight with ID: ${flightId}`);
    // Add your API call for booking here
  };

  return (
    <div>
      <h2>Available Flights</h2>
      {message && <p>{message}</p>}
      {flights.length > 0 ? (
        <table className="flights-table">
          <thead>
            <tr>
              <th>Flight Number</th>
              <th>Departure</th>
              <th>Arrival</th>
              <th>Seats</th>
              <th>Fare</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {flights.map((flight) => (
              <tr key={flight.id}>
                <td>{flight.flight_number}</td>
                <td>{flight.departure}</td>
                <td>{flight.arrival}</td>
                <td>{flight.seats}</td>
                <td>${flight.fare}</td>
                <td>
                  <button
                    onClick={() => handleBookNow(flight.id)}
                    className="book-now-button"
                  >
                    Book Now
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No flights available.</p>
      )}
    </div>
  );
};

export default AirlineReservation;