<template>
  <div class="landing">
    <div class="center">
      <h1>Ticket Booking</h1>
      <h2>A VueJS + Flask (Python) Ticket Booking System</h2>
      <div class="mt-3">
        <!-- SearchView Container -->
        <b-container>
          <b-row>
            <b-col>
              <SearchView />
            </b-col>
          </b-row>
        </b-container>

        <!-- Login and About Us Container -->
        <b-container class="bv-example-row mb-3">
          <b-row cols="2">
            <b-col>
              <b-card
                title="Login"
                img-src="https://picsum.photos/600/300/?image=9"
                img-alt="Image"
                img-top
                tag="article"
                style="max-width: 20rem"
                class="mb-1"
              >
                <b-card-text></b-card-text>
                <router-link to="/login" tag="button" class="btn btn-primary"
                  >Login</router-link
                >
              </b-card>
            </b-col>
            <b-col>
              <b-card
                title="About Us"
                img-src="https://picsum.photos/600/300/?image=26"
                img-alt="Image"
                img-top
                tag="article"
                style="max-width: 20rem"
                class="mb-1"
              >
                <b-card-text></b-card-text>
                <router-link to="/aboutus" tag="button" class="btn btn-primary"
                  >About Us</router-link
                >
              </b-card>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </div>
  </div>
</template>

<script>
import SearchView from "@/views/SearchView.vue";

export default {
  components: {
    SearchView,
  },
  data() {
    return {};
  },
  methods: {},
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
