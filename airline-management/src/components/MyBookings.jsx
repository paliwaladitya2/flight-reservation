import React, { Component } from "react";

class MyBookings extends Component {
  render() {
    const { bookings } = this.props;

    return (
      <div className="my-bookings">
        <h2>My Bookings</h2>
        {bookings.length > 0 ? (
          <div className="booking-list">
            {bookings.map((booking) => (
              <div key={booking.id} className="booking-card">
                <p>
                  <strong>From:</strong> {booking.from}
                </p>
                <p>
                  <strong>To:</strong> {booking.to}
                </p>
                <p>
                  <strong>Time:</strong> {booking.time}
                </p>
                <p>
                  <strong>Price:</strong> {booking.price}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <p>You have no bookings yet.</p>
        )}
      </div>
    );
  }
}

export default MyBookings;
