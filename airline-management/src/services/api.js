const BASE_URL = "http://127.0.0.1:8000/";

const api = {
  login: async (data) => {
    const response = await fetch(`${BASE_URL}api/v1/reservations/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
      credentials: "include"
    });
    const result = await response.json();
    console.log("Login Response:", result); // Log the response
  
    if (response.ok && result.sessionid) {
      sessionStorage.setItem("sessionid", result.sessionid); // Store sessionid
      console.log("Session ID stored:", result.sessionid); // Log stored sessionid
    }
    return result;
  },  

  register: async (data) => {
    const response = await fetch(`${BASE_URL}api/v1/reservations/register/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    return response.json();
  },

  logout: async () => {
    const response = await fetch(`${BASE_URL}api/v1/reservations/logout/`, {
      method: "GET",
    });
    return response.json();
  },

  getFlights: async () => {
    const response = await fetch(`${BASE_URL}api/flights/`, {
      method: "POST", // Matches backend method
      headers: { "Content-Type": "application/json" },
    });
    return response.json();
  },

  bookFlight: async (data) => {
    const response = await fetch(`${BASE_URL}api/v1/reservations/book-flight/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }, // Removed token
      body: JSON.stringify(data),
    });
    return response.json();
  },

  getMyBookings: async () => {
    const sessionid = sessionStorage.getItem("sessionid");
    console.log("Session ID used for API call:", sessionid); // Debug log
  
    const response = await fetch(`${BASE_URL}api/my-bookings/`, {
      method: "GET",
      // headers: {
      //   "Cookie": `sessionid=${sessionid};`, // Manually include sessionid
      // },
      credentials: "include",
    });
  
    if (response.ok) {
      const data = await response.json();
      console.log("Bookings:", data);
    } else {
      console.error("Error fetching bookings:", response.status, response.statusText);
    }
  },
  

  cancelBooking: async (data) => {
    const response = await fetch(`${BASE_URL}api/v1/reservations/cancel-booking/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }, // Removed token
      body: JSON.stringify(data),
    });
    return response.json();
  },
};

export default api;