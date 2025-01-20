<template>
  <div class="landing">
    <div class="center">
      <h3>All Venues</h3>

      <router-link to="/" tag="button" class="btn btn-primary">
        <b-icon icon="arrow-left" aria-hidden="true"></b-icon> Back to Home
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
              </b-card>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import store from "@/store";

export default {
  data() {
    return {
      venues: [],
    };
  },
  mounted() {
    this.fetchAllVenues();
  },
  methods: {
    fetchAllVenues() {
      const token = store.getters.getToken;
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
      this.selectedVenue = venue;
      this.showEditVenueModal = true;
    },
  },
};
</script>
