import store from "@/store/store"; // Import your Vuex store instance

const BASE_URL = "http://localhost:8080"; // Update with your backend server URL

// Helper function to handle response parsing
async function handleResponse(response) {
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || "An error occurred");
  }
  return response.json();
}

// Helper function to get the authorization header
function getAuthHeader() {
  const token = store.getters.getToken;
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
}
// User related API methods
export async function getAllUsers() {
  const response = await fetch(`${BASE_URL}/api/users`);
  return handleResponse(response);
}

// Venue related API methods
export async function getAllVenues() {
  const response = await fetch(`${BASE_URL}/api/venues`);
  return handleResponse(response);
}

// Show related API methods
export async function getAllShows() {
  const response = await fetch(`${BASE_URL}/api/shows`);
  return handleResponse(response);
}

// Booking related API methods
export async function createBooking(bookingData, token) {
  const response = await fetch(`${BASE_URL}/api/bookings/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: token,
    },
    body: JSON.stringify(bookingData),
  });
  return handleResponse(response);
}
// Booking related API methods
export async function getAllBookings() {
  const response = await fetch(`${BASE_URL}/api/admin_bookings`);
  return handleResponse(response);
}
// Admin related API methods
export async function approveUserRegistration(userId, token) {
  const response = await fetch(`${BASE_URL}/api/approve_user/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: token,
    },
  });
  return handleResponse(response);
}
