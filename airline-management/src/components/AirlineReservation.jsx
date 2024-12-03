import React, { Component } from "react";
import { withRouter } from "./withRouter"; // Import the utility
import "./AirlineReservation.css"

class AirlineReservation extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searchQuery: "",
      flights: [
        { id: 1, from: "Dublin", to: "London", time: "10:00 AM", price: "$50" },
        { id: 2, from: "San Francisco", to: "Tokyo", time: "2:00 PM", price: "$800" },
        { id: 3, from: "Los Angeles", to: "Paris", time: "6:00 PM", price: "$600" },
        { id: 4, from: "Delhi", to: "Dublin", time: "9:20 PM", price: "$600" },
        { id: 5, from: "Munich", to: "Madrid", time: "5:40 PM", price: "$60" },
      ],
      filteredFlights: [],
    };
  }

  handleSearch = () => {
    const { searchQuery, flights } = this.state;
    const filteredFlights = flights.filter(
      (flight) =>
        flight.from.toLowerCase().includes(searchQuery.toLowerCase()) ||
        flight.to.toLowerCase().includes(searchQuery.toLowerCase())
    );
    this.setState({ filteredFlights });
  };

  handleInputChange = (event) => {
    this.setState({ searchQuery: event.target.value });
  };

  render() {
    const { onLogout } = this.props; // Ensure onLogout is accessed here
    const { onBookNow, navigate } = this.props; // `navigate` is injected by withRouter
    const { searchQuery, filteredFlights, flights } = this.state;
    const displayFlights = filteredFlights.length > 0 ? filteredFlights : flights;

    return (
      <div className="airline-reservation">
        <header className="navbar">
          <h1 className="logo">Airline Reservation</h1>
          <div className="nav-actions">
          <button className="my-bookings">
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
            
            
          </div>

          <div className="flight-list">
            {displayFlights.length > 0 ? (
              displayFlights.map((flight) => (
                <div key={flight.id} className="flight-card">
                  <p><strong>From:</strong> {flight.from}</p>
                  <p><strong>To:</strong> {flight.to}</p>
                  <p><strong>Time:</strong> {flight.time}</p>
                  <p><strong>Price:</strong> {flight.price}</p>
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
        {/* Footer */}
        <footer className="footer">
          <p>&copy; 2024 Airline Reservation System. All Rights Reserved.</p>
        </footer>
      </div>
    );
  }
}

export default withRouter(AirlineReservation);
