<template>
  <div class="landing">
    <div class="center">
      <h3>All Venues</h3>
      <!-- Add the button to navigate to the AddVenue component -->
      <router-link to="/addvenue" tag="button" class="btn btn-primary">
        Add a New Venue ( For Admin Only )
      </router-link>

      <div class="mt-5">
        <b-container class="bv-example-row mb-3">
          <b-row cols="4">
            <b-col v-for="venue in venues" :key="venue.id">
              <b-card
                :title="venue.name"
                img-src="https://picsum.photos/600/300/?image=117"
                img-alt="Image"
                img-top
                tag="article"
                style="max-width: 20rem"
                class="mb-2"
              >
                <b-card-text>
                  <h6>ID - {{ venue.id }}</h6>
                  <h6>Place - {{ venue.place }}</h6>
                  <h6>Capacity - {{ venue.capacity }}</h6>
                </b-card-text>
                <div class="btn-group">
                  <button @click="editVenue(venue)">Edit</button>
                  <button @click="deleteVenue(venue)">Delete</button>
                </div>
              </b-card>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </div>
    <b-modal
      v-if="showEditVenueModal"
      v-model="showEditVenueModal"
      @hide="closeEditVenueModal"
    >
      <template #modal-title>Edit Venue</template>
      <EditVenue
        v-if="selectedVenue"
        :venueId="selectedVenue.id"
        @venue-updated="fetchAllVenues"
      />
      <template #modal-footer>
        <button class="btn btn-secondary" @click="closeEditVenueModal">
          Close
        </button>
      </template>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import store from "@/store";
import EditVenue from "@/views/EditVenue.vue";

export default {
  components: {
    EditVenue,
  },
  data() {
    return {
      venues: [],
      showEditVenueModal: false, // Add this property
      selectedVenue: null,
    };
  },
  mounted() {
    this.fetchAllVenues();
  },
  methods: {
    fetchAllVenues() {
      const token = store.getters.getToken;
      //console.log(token);
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      axios
        .get("http://localhost:8080/api/venues", config)
        .then((response) => {
          this.venues = response.data;
        })
        .catch((error) => {
          console.error("Error fetching venues:", error);
        });
    },

    editVenue(venue) {
      console.log("This function activated on clicking Edit button");
      this.selectedVenue = venue;
      console.log(venue.name);
      this.showEditVenueModal = true;
    },

    deleteVenue(venue) {
      const venue_id = venue.id;
      console.log(" Deleting Venue with id", venue_id);
      const token = store.getters.getToken;
      console.log(" Token from Frontend", token);
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };

      // Make a DELETE request to delete the venue
      axios
        .delete(`http://localhost:8080/api/venue/${venue_id}`, config)
        .then(() => {
          console.log(`Venue ${venue.name} deleted successfully`);
          // Update the venues list after deletion
          this.fetchAllVenues();
        })
        .catch((error) => {
          console.error(`Error deleting VENUE ${venue.name}:`, error);
        });
    },
    closeEditVenueModal() {
      this.showEditVenueModal = false;
      this.selectedVenue = null;
    },
    closeDeleteVenueModal() {
      this.showDeleteVenueModal = false;
      this.selectedVenue = null;
    },
  },
};
</script>
