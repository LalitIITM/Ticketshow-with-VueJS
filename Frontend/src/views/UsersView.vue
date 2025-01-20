/* eslint-disable */
<template>
  <div class="landing">
    <div class="center">
      <h3>All Users ( For Admin Only )</h3>

      <div class="mt-5">
        <b-container class="bv-example-row mb-3">
          <b-row cols="4">
            <b-col v-for="user in users" :key="user.user_id">
              <b-card
                :title="user.username"
                img-src="https://picsum.photos/600/300/?image=117"
                img-alt="Image"
                img-top
                tag="article"
                style="max-width: 20rem"
                class="mb-2"
              >
                <b-card-text>
                  <h6>ID: {{ user.user_id }}</h6>
                  <h6>Username: {{ user.username }}</h6>
                  <h6>Role: {{ user.role }}</h6>
                  <div v-if="user.approved === 0">
                    <input
                      type="checkbox"
                      v-model="selectedUsers"
                      :value="user.id"
                    />
                  </div>
                </b-card-text>
              </b-card>
            </b-col>
          </b-row>
        </b-container>
        <button @click="approveUsers">Approve Selected Users</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import store from "@/store"; // Import your Vuex store instance

export default {
  data() {
    return {
      users: [], // Your user data goes here
      selectedUsers: [], // Store the IDs of selected users
    };
  },
  methods: {
    approveUsers() {
      const token = this.$store.getters.getToken;

      // Loop through the selected users and make a request to approve each one
      this.selectedUsers.forEach((id) => {
        axios
          .put(
            `http://localhost:8080/api/approve_user/${id}`,
            {},
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          )
          .then(() => {
            console.log(`User ${id} approved successfully`);
            //  update the user list to reflect the changes
            this.fetchUsers();
          })
          .catch((error) => {
            console.error(`Error approving user ${id}:`, error);
          });
      });

      // Clear the selected users array after approval
      this.selectedUsers = [];
    },
    fetchUsers() {
      const token = store.getters.getToken; // Get the token from the store
      const config = {
        headers: {
          Authorization: `Bearer ${token}`, // Include the token in the request header
        },
      };
      //console.log("Token Sent to Backend:", token);

      axios
        .get("http://localhost:8080/api/user", config) // Update the URL to your backend route
        .then((response) => {
          this.users = response.data;
        })
        .catch((error) => {
          console.error("Error fetching users:", error);
        });
    },
  },
  mounted() {
    // Fetch users data and set this.users
    this.fetchUsers();
  },
};
</script>
<style scoped>
/* Add your styles here */
button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
