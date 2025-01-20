<template>
  <div>
    <h2>Create Venue</h2>
    <form @submit.prevent="createVenue">
      <div>
        <label for="name">Venue Name:</label>
        <input type="text" id="name" v-model="name" required />
      </div>
      <div>
        <label for="place">Venue Place:</label>
        <input type="text" id="place" v-model="place" required />
      </div>
      <div>
        <label for="capacity">Venue Capacity:</label>
        <input type="number" id="capacity" v-model="capacity" required />
      </div>
      <button type="submit">Create Venue</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      name: "",
      place: "",
      capacity: 0,
    };
  },
  methods: {
    createVenue() {
      const venueData = {
        name: this.name,
        place: this.place,
        capacity: this.capacity,
      };

      // Send POST request to create venue
      axios
        .post("/api/venue", venueData, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          console.log(response.data.message);
          // Optionally, navigate to another page after successful creation
          this.$router.push("/venues");
        })
        .catch((error) => {
          // Handle error
          console.error("Error creating Venue:", error);
        });
    },
  },
};
</script>
