<template>
  <div>
    <h3>Search</h3>

    <div class="input-container">
      <input
        v-model="show"
        placeholder="Enter Show Name"
        class="search-input"
      />
      <input
        v-model="place"
        placeholder="Enter Location"
        class="search-input"
      />
      <button @click="search" class="search-button">Search</button>
    </div>

    <div>
      <h3>Results:</h3>
      <table class="table">
        <thead>
          <tr>
            <th>Show Name</th>
            <th>Rating</th>
            <th>Tags</th>
            <th>Venue</th>
            <th>Place</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in paginatedResults" :key="result.id">
            <td>{{ result.name }}</td>
            <td>{{ result.rating }}</td>
            <td>{{ result.tags }}</td>
            <td>{{ result.venue }}</td>
            <td>{{ result.place }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination-container">
      <b-pagination
        v-model="currentPage"
        :total-rows="totalRows"
        :per-page="perPage"
        :align="'center'"
        size="md"
        class="mt-3"
      ></b-pagination>
    </div>

    <div v-if="results.length === 0">
      <p>No results found.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      show: "",
      place: "",
      results: [],
      currentPage: 1,
      perPage: 5, // Number of items per page
      totalRows: 0, // Total number of rows in the table
    };
  },
  computed: {
    paginatedResults() {
      // Calculate start and end indexes for the current page
      const startIndex = (this.currentPage - 1) * this.perPage;
      const endIndex = startIndex + this.perPage;

      // Return the slice of results for the current page
      return this.results.slice(startIndex, endIndex);
    },
  },
  methods: {
    search() {
      const requestData = {
        show: this.show,
        location: this.place,
      };

      axios
        .post("http://localhost:8080/api/search", requestData)
        .then((response) => {
          this.results = response.data;
          this.totalRows = this.results.length; // Update totalRows
        })
        .catch((error) => {
          console.error("Error fetching search results:", error);
        });
    },
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
