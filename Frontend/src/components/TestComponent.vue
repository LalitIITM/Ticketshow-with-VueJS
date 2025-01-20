<template>
  <div>
    <h1>Test Backend Connection</h1>
    <button @click="testBackendConnection">Test Connection</button>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      message: "",
    };
  },
  methods: {
    async testBackendConnection() {
      try {
        const response = await axios.get("http://localhost:8080/api/test"); // Replace with your API endpoint
        this.message = response.data.message;
      } catch (error) {
        this.message = "Error connecting to the backend.";
        console.error(error);
      }
    },
  },
};
</script>
