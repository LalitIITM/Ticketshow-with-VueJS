<template>
  <div>
    <h2>Delete Show ( For Admin Only )</h2>
    <p>Are you sure you want to delete this Show?</p>
    <button @click="deleteshow">Confirm Delete</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    show: Object, // The venue data to delete
  },
  methods: {
    deleteShow() {
      // Send DELETE request to delete venue
      axios
        .delete(`/api/show/${this.show.id}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        })
        .then((response) => {
          console.log(response.data.message);
          // Emit an event to notify the parent component of the deletion
          this.$emit("Show-deleted");
        })
        .catch((error) => {
          // Handle error
          console.error("Error deleting Show:", error);
        });
    },
  },
};
</script>
