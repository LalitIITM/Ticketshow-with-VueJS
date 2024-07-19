<template>
  <div class="landing">
    <div class="center">
      <h4>Add New Venue ( For Admin Only )</h4>
      <h4>Enter Venue Details</h4>

      <div class="mt-5">
        <b-container>
          <b-row>
            <b-col cols="8" offset-md="2">
              <b-card>
                <b-card-body>
                  <b-form @submit.prevent="createVenue">
                    <b-form-group label="Venue Name" label-for="name">
                      <b-form-input
                        id="name"
                        v-model="venueName"
                        required
                      ></b-form-input>
                    </b-form-group>

                    <b-form-group label="Venue Place" label-for="place">
                      <b-form-input
                        id="place"
                        v-model="venuePlace"
                        required
                      ></b-form-input>
                    </b-form-group>

                    <b-form-group label="Venue Capacity" label-for="capacity">
                      <b-form-input
                        id="capacity"
                        type="number"
                        v-model="venueCapacity"
                        required
                      ></b-form-input>
                    </b-form-group>

                    <div class="text-center">
                      <b-button type="submit" variant="primary">
                        Create Venue
                      </b-button>
                    </div>
                  </b-form>
                </b-card-body>
              </b-card>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </div>
    <div v-if="venueCreated" class="success-message">
      Venue Created Successfully
    </div>
    <div v-if="venueMessage" class="venue-message">
      {{ venueMessage }}
    </div>
  </div>
</template>

<script>
import axios from "axios";
import store from "@/store"; // Import your Vuex store instance

export default {
  data() {
    return {
      venueName: "",
      venuePlace: "",
      venueCapacity: null,
      venueCreated: false,
      venueMessage: "",
    };
  },
  methods: {
    async createVenue() {
      const token = store.getters.getToken; // Get the token from the store
      //console.log("Token Sent to Backend:", token);

      const venueData = {
        name: this.venueName,
        place: this.venuePlace,
        capacity: this.venueCapacity,
      };

      const config = {
        headers: {
          Authorization: `Bearer ${token}`, // Include the token in the request header
          "Content-Type": "application/json",
        },
      };

      try {
        const response = await axios.post(
          "http://localhost:8080/api/venue/create",
          venueData,
          config
        );
        console.log("Venue created successfully", response.data);
        this.venueMessage = response.data.message;
        this.venueCreated = true;
        console.log("venueCreated:", this.venueCreated);
        this.$router.push("/admindashboard1");
      } catch (error) {
        console.error("Error creating venue:", error);
      }
    },
  },
};
</script>

<style scoped>
.success-message {
  margin-top: 15px;
  color: green;
  font-weight: bold;
}
</style>
