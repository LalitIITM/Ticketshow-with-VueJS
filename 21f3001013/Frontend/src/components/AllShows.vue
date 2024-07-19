/* eslint-disable */
<template>
  <div class="landing">
    <div class="center">
      <h3>All Shows</h3>

      <router-link to="/" tag="button" class="btn btn-primary">
        <b-icon icon="arrow-left" aria-hidden="true"></b-icon> Back to Home
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

export default {
  data() {
    return {
      shows: [],
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
  },
};
</script>
