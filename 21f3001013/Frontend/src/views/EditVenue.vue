<template>
  <div>
    <h4>Edit Venue ( For Admin Only )</h4>

    <template v-if="!updateSuccess">
      <form @submit.prevent="updateVenue">
        <label for="name">Venue Name:</label>
        <input type="text" id="name" v-model="venue.name" required />

        <label for="place">Place:</label>
        <input type="text" id="place" v-model="venue.place" required />

        <label for="capacity">Capacity:</label>
        <input type="number" id="capacity" v-model="venue.capacity" required />

        <button type="submit">Update Venue</button>
      </form>
    </template>
    <div v-else class="success-message">
      {{ updateMessage }}
    </div>
    <button @click="$emit('close')">Close</button>
  </div>
</template>

<script>
import axios from "axios";
import store from "@/store";

export default {
  props: {
    venueId: Number, // Accept the venue ID as a prop
  },
  data() {
    return {
      venue: {
        name: "",
        place: "",
        capacity: 0,
      },
      updateSuccess: false,
      updateMessage: "",
    };
  },

  methods: {
    async updateVenue() {
      const token = store.getters.getToken;

      // Convert the venue object to JSON string
      const data = JSON.stringify(this.venue);
      //console.log(data);
      //console.log("Venue ID type:", typeof this.venueId);
      //console.log(this.venueId);
      axios

        .patch(`http://localhost:8080/api/venue/${this.venueId}`, data, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        })
        .then(() => {
          console.log(`Venue ${this.venueId} updated successfully`);
          this.updateSuccess = true;
          this.updateMessage = "Venue updated successfully";
          //  update the user list to reflect the changes
          this.$emit("venue-updated");
        })
        .catch((error) => {
          console.error(`Error updating ${this.venueId}:`, error);
        });
    },

    async fetchVenueData() {
      try {
        const token = store.getters.getToken;
        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };

        const response = await axios.get(
          `http://localhost:8080/api/venue/${this.venueId}`,
          config
        );
        this.venue = response.data;
        console.log("Made THIS venue", this.venue.id);
        console.log("VENUE NAME", this.venue.name);
      } catch (error) {
        console.error("Error fetching venue data:", error);
      }
    },
  },
  created() {
    this.fetchVenueData(); // Fetch venue data when component is created
  },
};
</script>
