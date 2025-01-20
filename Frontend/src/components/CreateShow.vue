<template>
  <div>
    <h1>Create Show</h1>
    <form @submit.prevent="createShow">
      <label for="name">Show Name:</label>
      <input type="text" id="name" v-model="show.name" required />

      <label for="venue">Venue:</label>
      <select id="venue" v-model="show.venue" required>
        <option v-for="venue in venues" :key="venue.id" :value="venue.id">
          {{ venue.name }}
        </option>
      </select>

      <button type="submit">Create Show</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      show: {
        name: "",
        venue: null,
      },
      venues: [], // Populate this with venue data from API
    };
  },
  methods: {
    async createShow() {
      try {
        const response = await this.$axios.post("/api/show", this.show);
        console.log(response.data.message);
        // Redirect to show list or other page
        this.$router.push("/shows");
      } catch (error) {
        console.error("Error creating show:", error);
      }
    },
  },
};
</script>
