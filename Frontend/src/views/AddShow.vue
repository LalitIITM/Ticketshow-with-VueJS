<template>
  <div class="landing">
    <div class="center">
      <h4>Add New Show ( For Admin Only )</h4>
      <h4>Enter Show Details</h4>

      <div class="mt-5">
        <b-container>
          <b-row>
            <b-col cols="8" offset-md="2">
              <b-card>
                <b-card-body>
                  <b-form @submit.prevent="createShow">
                    <b-form-group label="Show Name" label-for="name">
                      <b-form-input
                        id="name"
                        type="text"
                        v-model="showName"
                        required
                      ></b-form-input>
                    </b-form-group>

                    <b-form-group label="Rating" label-for="rating">
                      <b-form-input
                        id="rating"
                        type="number"
                        v-model="showRating"
                        required
                      ></b-form-input>
                    </b-form-group>

                    <b-form-group label="Tags" label-for="tags">
                      <b-form-input
                        id="tags"
                        type="text"
                        v-model="showTags"
                        required
                      ></b-form-input>
                    </b-form-group>

                    <b-form-group label="Ticket Price" label-for="ticket_price">
                      <b-form-input
                        id="ticket_price"
                        type="number"
                        v-model="showTicketPrice"
                        required
                      ></b-form-input>
                    </b-form-group>

                    <b-form-group label="Venue" label-for="venue_name">
                      <b-form-input
                        id="venue_name"
                        type="text"
                        v-model="showVenueName"
                        required
                      ></b-form-input>
                    </b-form-group>

                    <b-form-group label="Image Path" label-for="image_path">
                      <b-form-input
                        id="image_path"
                        type="text"
                        v-model="showImage"
                      ></b-form-input>
                    </b-form-group>

                    <div class="text-center">
                      <b-button type="submit" variant="primary">
                        Create Show
                      </b-button>
                    </div>
                  </b-form>
                  <div v-if="showCreated" class="success-message">
                    Show Created Successfully
                  </div>
                </b-card-body>
              </b-card>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </div>
    <button @click="$emit('close')">Close</button>
  </div>
</template>

<script>
import axios from "axios";
import store from "@/store"; // Import your Vuex store instance

export default {
  data() {
    return {
      showName: "",
      showRating: null,
      showTags: "",
      showTicketPrice: null,
      showVenueName: "", // Initialize selectedVenue with a name property
      showImage: "",
      showCreated: false,
    };
  },
  methods: {
    async createShow() {
      const token = store.getters.getToken; // Get the token from the store
      console.log("Token Sent to Backend:", token);

      const showData = {
        name: this.showName,
        rating: this.showRating,
        tags: this.showTags,
        ticket_price: this.showTicketPrice,
        venue_name: this.showVenueName,
        image_path: this.showImage,
      };
      console.log("data in frontend:", showData);

      const config = {
        headers: {
          Authorization: `Bearer ${token}`, // Include the token in the request header
          "Content-Type": "application/json",
        },
      };

      try {
        const response = await axios.post(
          "http://localhost:8080/api/show/create",
          showData,
          config
        );
        console.log("Show created successfully", response.data);
        this.showCreated = true;
        this.$router.push("/admindashboard1");
      } catch (error) {
        console.error("Error creating show:", error);
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
