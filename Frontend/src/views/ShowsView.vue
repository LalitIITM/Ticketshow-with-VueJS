/* eslint-disable */
<template>
  <div class="landing">
    <div class="center">
      <h3>All Shows</h3>
      <!-- Add the button to navigate to the AddShow component -->
      <router-link to="/addshow" tag="button" class="btn btn-primary">
        Add a New Show( For Admin Only )
      </router-link>

      <div class="mt-5">
        <b-container class="bv-example-row mb-3">
          <b-row cols="4">
            <b-col v-for="show in shows" :key="show.id">
              <b-card
                :title="show.name"
                img-src="https://picsum.photos/600/300/?image=117"
                img-alt="Image"
                img-top
                tag="article"
                style="max-width: 20rem"
                class="mb-2"
              >
                <b-card-text>
                  <b-form-rating
                    v-model="show.rating"
                    stars="10"
                    variant="warning"
                    class="mb-2"
                  ></b-form-rating>
                  <h6>Tags - {{ show.tags }}</h6>
                  <h6>ID - {{ show.id }}</h6>
                  <h6>
                    <b-button variant="info"
                      >₹ {{ show.ticket_price }}</b-button
                    >
                  </h6>
                  <h6>Playing at {{ show.venue_name }}</h6>
                </b-card-text>
                <div class="btn-group">
                  <button @click="editShow(show)">Edit</button>
                  <button @click="deleteShow(show)">Delete</button>
                </div>
              </b-card>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </div>
    <b-modal
      v-if="showEditShowModal"
      v-model="showEditShowModal"
      @hide="closeEditShowModal"
    >
      <template #modal-title>Edit Show</template>
      <EditShow
        v-if="selectedShow"
        :showId="selectedShow.id"
        @show-updated="fetchAllShows"
      />
      <template #modal-footer>
        <button class="btn btn-secondary" @click="closeEditShowModal">
          Close
        </button>
      </template>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import store from "@/store";
import EditShow from "@/views/EditShow.vue";

export default {
  components: {
    EditShow,
  },
  data() {
    return {
      shows: [],
      showEditShowModal: false, // Add this property
      selectedShow: null,
    };
  },
  mounted() {
    this.fetchAllShows();
  },
  methods: {
    fetchAllShows() {
      axios
        .get("http://localhost:8080/api/shows")
        .then((response) => {
          this.shows = response.data;
        })
        .catch((error) => {
          console.error("Error fetching shows:", error);
        });
    },

    editShow(show) {
      console.log("This function activated on clicking Edit button");
      this.selectedShow = show;
      console.log(show.name);
      console.log(show.id);
      this.showEditShowModal = true;
    },

    deleteShow(show) {
      const show_id = show.id;
      console.log(" Deleting Show with id", show_id);
      const token = store.getters.getToken;
      console.log(" Token from Frontend", token);
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };

      // Make a DELETE request to delete the venue
      axios
        .delete(`http://localhost:8080/api/show/${show_id}`, config)
        .then(() => {
          console.log(`Show ${show.name} deleted successfully`);
          // Update the venues list after deletion
          this.fetchAllShows();
        })
        .catch((error) => {
          console.error(`Error deleting SHOW ${show.name}:`, error);
        });
    },

    // Listen for the show-updated event and update the shows array
    updateShowsAfterEdit() {
      this.fetchAllShows(); // This fetches updated show data from the server
      this.closeEditShowModal();
      this.closeDeleteShowModal();
    },

    closeEditShowModal() {
      this.showEditShowModal = false;
      this.selectedShow = null;
    },

    closeDeleteShowModal() {
      this.showDeleteShowModal = false;
      this.selectedShow = null;
    },
  },
  created() {
    this.fetchAllShows();
    // Listen for the show-updated event and update the shows array
    this.$on("show-updated", this.updateShowsAfterEdit);
  },

  // Don't forget to clean up the event listener when the component is destroyed
  beforeDestroy() {
    this.$off("show-updated", this.updateShowsAfterEdit);
  },
};
</script>
