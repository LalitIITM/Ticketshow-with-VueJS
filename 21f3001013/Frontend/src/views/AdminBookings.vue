<template>
  <div class="admin-bookings">
    <h1 class="table-heading">All Bookings ( For Admin Only )</h1>

    <div class="table-container">
      <table class="booking-table">
        <thead>
          <tr>
            <th class="table-header">Booking ID</th>
            <th class="table-header">User Name</th>
            <th class="table-header">Show Name</th>
            <th class="table-header">Venue Name</th>
            <th class="table-header">Quantity</th>
            <th class="table-header">Place</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in bookings" :key="booking.id">
            <td>{{ booking.id }}</td>
            <td>{{ booking.user_name }}</td>
            <td>{{ booking.show_name }}</td>
            <td>{{ booking.venue_name }}</td>
            <td>{{ booking.quantity }}</td>
            <td>{{ booking.place }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination-container">
      <b-pagination
        v-model="currentPage"
        :total-rows="totalRows"
        :per-page="perPage"
        :align="'center'"
        size="md"
        class="mt-3"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import store from "@/store";

export default {
  data() {
    return {
      currentPage: 1,
      perPage: 10, // Number of items per page
      totalRows: 0, // Total number of rows in the table
      bookings: [], // Your booking data goes here
    };
  },
  mounted() {
    this.fetchAllBookings();
  },
  methods: {
    fetchAllBookings() {
      const token = store.getters.getToken;
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };

      axios
        .get("http://localhost:8080/api/admin_bookings", config)
        .then((response) => {
          this.bookings = response.data.map((booking) => ({
            id: booking.id,
            user_name: booking.user_name,
            show_name: booking.show_name,
            venue_name: booking.venue_name,
            quantity: booking.quantity,
            place: booking.place,
          }));
        })
        .catch((error) => {
          console.error("Error fetching bookings:", error);
        });
    },
  },
};
</script>

<style scoped>
/* Your styles */
</style>

<style scoped>
.admin-bookings {
  text-align: center;
  padding: 20px;
}

.table-heading {
  font-size: 24px;
  margin-bottom: 20px;
}

.table-container {
  max-width: 800px;
  margin: 0 auto;
}

.booking-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #1c3a5e; /* Dark blue background color */
  color: #fff; /* Text color */
}

.table-header {
  background-color: #000; /* Black background color for table header */
  color: #fff; /* Text color for table header */
  padding: 10px;
  font-weight: bold;
  text-align: center; /* Center the text in table header */
}

.booking-table td {
  padding: 10px;
  border: 1px solid #ccc;
  text-align: center; /* Center the text in table cells */
}

.booking-table tr:hover {
  background-color: #2b506f; /* Darker blue on hover */
}

.button-container {
  text-align: center;
  margin-top: 20px;
}

.button-container button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.button-container button:hover {
  background-color: #0056b3;
}
</style>
