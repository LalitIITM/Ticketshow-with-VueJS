<template>
  <div class="landing">
    <div class="center">
      <h1>User Dashboard</h1>
      <h4>
        You are logged in as {{ this.$store.getters.getUsername }} in
        {{ this.$store.getters.getRole }} role
      </h4>
      <h2>User Features</h2>
      <router-link to="/" tag="button" class="btn btn-primary">
        <b-icon icon="arrow-left" aria-hidden="true"></b-icon> Back to Home
      </router-link>
      <router-link to="/logout" tag="button" class="btn btn-primary">
        <b-icon icon="lock-fill" aria-hidden="true"></b-icon> Logout
      </router-link>
      <div class="mt-5">
        <b-button-toolbar class="tab-buttons">
          <b-button @click="showTab('SearchView')" class="tab-button"
            >Search</b-button
          >
          >
          <b-button @click="showTab('MyBookings')" class="tab-button"
            >My Bookings</b-button
          >

          <b-button @click="showTab('AddBooking')" class="tab-button"
            >Add New Bookings</b-button
          >
          >
        </b-button-toolbar>
        <component :is="activeTab"></component>
        <button @click="downloadBookingsReport">
          Download Bookings Report
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import store from "@/store";
import MyBookings from "@/views/MyBookings.vue";
import SearchView from "@/views/SearchView.vue";
import AddBooking from "@/views/AddBooking.vue";

export default {
  components: {
    SearchView,
    MyBookings,
    AddBooking,
  },
  data() {
    return {
      activeTab: null,
      tabComponents: {
        SearchView: SearchView,
        MyBookings: MyBookings,
        AddBooking: AddBooking,
      },
    };
  },
  methods: {
    showTab(tabName) {
      this.activeTab = this.tabComponents[tabName];
    },
    downloadBookingsReport() {
      const user_id = store.getters.getUserId;
      const token = store.getters.getToken;
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        responseType: "blob", // Set the response type to 'blob' to handle binary data
      };

      // Make a GET request to the backend endpoint that generates the report
      axios
        .get(`http://localhost:8080/api/export_bookings/${user_id}`, config)
        .then((response) => {
          // Create a Blob object from the binary data received
          const blob = new Blob([response.data], { type: "application/csv" });

          // Create a URL for the Blob object
          const url = window.URL.createObjectURL(blob);

          // Create a link element to trigger the download
          const link = document.createElement("a");
          link.href = url;
          link.download = "bookings_report.csv"; // Specify the filename

          // Trigger a click event on the link to initiate the download
          link.click();

          // Clean up by revoking the URL
          window.URL.revokeObjectURL(url);
        })
        .catch((error) => {
          console.error("Error downloading bookings report:", error);
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
