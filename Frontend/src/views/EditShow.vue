<template>
  <div class="landing">
    <div class="center">
      <h5>Edit a Show (For Admin Only)</h5>
      <h5>Enter Show Details</h5>

      <div class="mt-5">
        <b-container>
          <b-row>
            <b-col cols="8" offset-md="2">
              <b-card>
                <b-card-body>
                  <template v-if="!updateSuccess">
                    <b-form @submit.prevent="updateShow">
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
                      <b-form-group
                        label="Ticket Price"
                        label-for="ticket_price"
                      >
                        <b-form-input
                          id="ticket_price"
                          type="number"
                          v-model="showTicketPrice"
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
                        <b-button type="submit" variant="primary"
                          >Update Show</b-button
                        >
                      </div>
                    </b-form>
                  </template>
                  <div v-else class="success-message">
                    {{ updateMessage }}
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
import store from "@/store";

export default {
  props: {
    showId: Number, // Accept the show ID as a prop
  },

  data() {
    return {
      showName: "",
      showRating: null,
      showTags: "",
      showTicketPrice: null,
      showVenueName: "",
      showImage: "",
      updateSuccess: false,
      updateMessage: "",
    };
  },

  methods: {
    async updateShow() {
      const token = store.getters.getToken;
      const showData = {
        id: this.showId,
        name: this.showName,
        rating: this.showRating,
        tags: this.showTags,
        ticket_price: this.showTicketPrice,
        venue_name: this.showVenueName,
        image_path: this.showImage,
      };

      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      };

      try {
        const response = await axios.patch(
          `http://localhost:8080/api/show/${this.showId}`,
          showData,
          config
        );
        console.log("Show updated successfully", response.data);
        this.updateSuccess = true;
        this.updateMessage = "Show updated successfully";
        this.$emit("show-updated");
        this.$router.push("/admindashboard1");
      } catch (error) {
        console.error("Error updating show:", error);
        this.updateMessage = "Error updating show";
      }
    },

    // Other methods...

    async fetchShowData() {
      try {
        const token = store.getters.getToken;
        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };

        const response = await axios.get(
          `http://localhost:8080/api/show/${this.showId}`,
          config
        );

        // Set data properties with retrieved values
        const showData = response.data;
        this.showName = showData.name;
        this.showRating = showData.rating;
        this.showTags = showData.tags;
        this.showTicketPrice = showData.ticket_price;
        this.showImage = showData.image_path;
      } catch (error) {
        console.error("Error fetching show data:", error);
      }
    },
  },

  created() {
    this.fetchShowData(); // Fetch show data when component is created
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>
