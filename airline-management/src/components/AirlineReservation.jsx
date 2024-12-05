import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { fetchFlights } from "../api"; // Import API call
import "./AirlineReservation.css";

const AirlineReservation = ({ onLogout, onBookNow }) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [flights, setFlights] = useState([]);
  const [filteredFlights, setFilteredFlights] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch flights from backend when component mounts
    const loadFlights = async () => {
      try {
        const response = await fetchFlights();
        setFlights(response.data);
        setFilteredFlights(response.data); // Initialize filtered flights
      } catch (error) {
        console.error("Error fetching flights:", error);
      }
    };

    loadFlights();
  }, []);

  const handleSearch = () => {
    const filtered = flights.filter(
      (flight) =>
        flight.from.toLowerCase().includes(searchQuery.toLowerCase()) ||
        flight.to.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredFlights(filtered);
  };

  const handleInputChange = (event) => {
    setSearchQuery(event.target.value);
    // Clear filter when search query is empty
    if (event.target.value === "") {
      setFilteredFlights(flights);
    }
  };

  const displayFlights = filteredFlights;

  return (
    <div className="airline-reservation">
      <header className="navbar">
        <h1 className="logo">Airline Reservation</h1>
        <div className="nav-actions">
          <button
            className="my-bookings"
            onClick={() => navigate("/my-bookings")}
          >
            My Bookings
          </button>
          <button className="logout-button" onClick={onLogout}>
            Logout
          </button>
        </div>
      </header>

      <main className="main-content">
        <div className="search-section">
          <h2>Find Your Flight</h2>
          <input
            type="text"
            placeholder="Search by city or destination"
            value={searchQuery}
            onChange={handleInputChange}
          />
          <button onClick={handleSearch} className="search-button">
            Search
          </button>
        </div>

        <div className="flight-list">
          {displayFlights.length > 0 ? (
            displayFlights.map((flight) => (
              <div key={flight.id} className="flight-card">
                <p>
                  <strong>From:</strong> {flight.from}
                </p>
                <p>
                  <strong>To:</strong> {flight.to}
                </p>
                <p>
                  <strong>Time:</strong> {flight.time}
                </p>
                <p>
                  <strong>Price:</strong> {flight.price}
                </p>
                <button
                  className="book-button"
                  onClick={() => onBookNow(flight, navigate)}
                >
                  Book Now
                </button>
              </div>
            ))
          ) : (
            <p>No flights found.</p>
          )}
        </div>
      </main>

      <footer className="footer">
        <p>&copy; 2024 Airline Reservation System. All Rights Reserved.</p>
      </footer>
    </div>
  );
};

export default AirlineReservation;