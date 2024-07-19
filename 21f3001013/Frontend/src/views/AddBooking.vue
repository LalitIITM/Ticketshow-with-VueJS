<template>
  <div class="add-booking">
    <h5>Add Booking (For User Only)</h5>
    <form @submit.prevent="createBooking">
      <div class="form-group">
        <label for="showName">Show Name:</label>
        <input type="text" id="showName" v-model="showName" required />
      </div>
      <div class="form-group">
        <label for="venueName">Venue Name:</label>
        <select
          id="venueName"
          v-model="selectedVenue"
          required
          @focus="fetchVenue"
        >
          <option v-for="venue in venues1" :key="venue.id" :value="venue.name">
            {{ venue.name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="quantity">Quantity:</label>
        <input type="number" id="quantity" v-model="quantity" required />
      </div>
      <button type="submit">Create Booking</button>
    </form>
    <div v-if="bookingCreated" class="success-message">
      Booking Created Successfully
    </div>
    <div v-if="bookingMessage" class="booking-message">
      {{ bookingMessage }}
    </div>
  </div>
</template>

<script>
import axios from "axios";
import store from "@/store";

export default {
  data() {
    return {
      showName: "",
      selectedVenue: "",
      quantity: 0,
      bookingCreated: false,
      showVenues: [],
      bookingMessage: "",
      venues1: [],
    };
  },
  methods: {
    // Define the fetchVenue method here
    fetchVenue() {
      // Get the show ID based on the selected show name
      const selectedShowName = this.showName;
      // Make an API request to get venues by show name
      axios
        .get(
          `http://localhost:8080/api/venues-by-show-name?show_name=${selectedShowName}`
        )
        .then((response) => {
          this.venues1 = response.data;
          if (this.venues1.length > 0) {
            this.selectedVenue = this.venues1[0].name;
          }
        })
        .catch((error) => {
          console.error("Error fetching venues:", error);
        });
    },

    createBooking() {
      const token = store.getters.getToken;
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };

      const bookingData = {
        show_name: this.showName,
        venue_name: this.selectedVenue,
        quantity: this.quantity,
      };

      axios
        .post("http://localhost:8080/api/create_booking", bookingData, config)
        .then((response) => {
          this.bookingMessage = response.data.message;
          this.bookingCreated = true;
          console.log("New Booking created successfully");
          this.$router.push("/userdashboard");
        })
        .catch((error) => {
          if (error.response) {
            // The request was made, but the server responded with an error status
            this.bookingMessage = error.response.data.message;
          } else if (error.request) {
            // The request was made, but no response was received
            this.bookingMessage = "No response received from the server.";
          } else {
            // Something happened in setting up the request
            this.bookingMessage = "An error occurred while making the request.";
          }
          console.error("Error creating booking:", error);
        });
    },
  },
};
</script>

<style scoped>
.add-booking {
  text-align: center;
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
}

input,
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.success-message {
  margin-top: 15px;
  color: green;
  font-weight: bold;
}
</style>
