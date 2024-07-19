<template>
  <div class="edit-booking">
    <h2>Edit Booking( For User Only )</h2>
    <form @submit.prevent="createBooking">
      <div class="form-group">
        <label for="showName">Show Name:</label>
        <input type="text" id="showName" v-model="showName" required />
      </div>
      <div class="form-group">
        <label for="venueName">Venue Name:</label>
        <input type="text" id="venueName" v-model="venueName" required />
      </div>
      <div class="form-group">
        <label for="quantity">Quantity:</label>
        <input type="number" id="quantity" v-model="quantity" required />
      </div>
      <button type="submit">Update Booking</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import store from "@/store";

export default {
  props: {
    bookingId: Number, // Accept the booking ID as a prop
  },
  data() {
    return {
      // Define your form fields here
      // For example:
      showName: "",
      venueName: "",
      quantity: null,
    };
  },
  methods: {
    async editBooking() {
      const token = store.getters.getToken;
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };

      const updatedBookingData = {
        show_name: this.showName,
        venue_name: this.venueName,
        quantity: this.quantity,
      };

      try {
        const response = await axios.patch(
          `http://localhost:8080/api/booking/${this.bookingId}`,
          updatedBookingData,
          config
        );
        console.log("Booking updated successfully", response.data);
        this.$emit("booking-updated"); // Emit an event to notify the parent component
      } catch (error) {
        console.error("Error updating booking:", error);
      }
    },
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>
