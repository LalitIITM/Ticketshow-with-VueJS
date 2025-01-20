<template>
  <div class="landing">
    <div class="center">
      <h1>Admin Dashboard</h1>
      <h4>
        You are logged in as {{ this.$store.getters.getUsername }} in
        {{ this.$store.getters.getRole }} role
      </h4>
      <h2>Admin Features</h2>
      <router-link to="/" tag="button" class="btn btn-primary">
        <b-icon icon="arrow-left" aria-hidden="true"></b-icon> Back to Home
      </router-link>
      <router-link to="/logout" tag="button" class="btn btn-primary">
        <b-icon icon="lock-fill" aria-hidden="true"></b-icon> Logout
      </router-link>

      <div class="mt-5">
        <b-button-toolbar class="tab-buttons">
          <b-button @click="showTab('Users')" class="tab-button"
            >Users</b-button
          >
          <b-button @click="showTab('Venues')" class="tab-button"
            >Venues</b-button
          >
          <b-button @click="showTab('Shows')" class="tab-button"
            >Shows</b-button
          >
          <b-button @click="showTab('Bookings')" class="tab-button"
            >Bookings</b-button
          >
        </b-button-toolbar>
        <component :is="activeTab"></component>
      </div>
      <button @click="downloadAllBookingsReport">
        Download All Bookings Report
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import store from "@/store";
import VenuesView from "@/views/VenuesView.vue";
import ShowsView from "@/views/ShowsView.vue";
import UsersView from "@/views/UsersView.vue";
import AdminBookings from "@/views/AdminBookings.vue";

export default {
  components: {
    VenuesView,
    ShowsView,
    UsersView,
    AdminBookings,
  },
  data() {
    return {
      activeTab: null, // Default active tab
      tabComponents: {
        Users: UsersView,
        Venues: VenuesView,
        Shows: ShowsView,
        Bookings: AdminBookings,
      },
    };
  },
  methods: {
    showTab(tabName) {
      this.activeTab = this.tabComponents[tabName];
    },
    downloadAllBookingsReport() {
      const token = store.getters.getToken; // Get the token from your Vuex store
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        responseType: "blob", // Set the response type to 'blob' to handle binary data
      };

      // Make an HTTP request to the backend API to download the report
      axios
        .get("http://localhost:8080/api/export_all_bookings", config)
        .then((response) => {
          // Create a Blob object from the binary data received
          const blob = new Blob([response.data], { type: "application/csv" });

          // Create a URL for the Blob object
          const url = window.URL.createObjectURL(blob);

          // Create a link element to trigger the download
          const link = document.createElement("a");
          link.href = url;
          link.download = "all_bookings_report.csv"; // Specify the filename

          // Trigger a click event on the link to initiate the download
          link.click();

          // Clean up by revoking the URL
          window.URL.revokeObjectURL(url);
        })
        .catch((error) => {
          console.error("Error downloading all bookings report:", error);
        });
    },
  },
};
</script>
<style scoped>
.center {
  text-align: center;
}

.tab-buttons {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.tab-button {
  margin: 0 10px;
}
</style>
