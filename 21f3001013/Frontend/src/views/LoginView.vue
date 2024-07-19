<template>
  <div class="landing">
    <div class="center">
      <h1>Ticket Booking - Login / Register</h1>
      <h2>Login / Register</h2>
      <router-link to="/" tag="button" class="btn btn-primary"
        ><b-icon icon="arrow-left" aria-hidden="true"></b-icon> Back to
        Home</router-link
      >
    </div>
    <div class="mt-5">
      <b-container class="bv-example-row mb-3">
        <b-row class="justify-content-md-center">
          <b-col cols="4">
            <b-card no-body>
              <b-tabs pills card align="center">
                <b-tab title="Login" active
                  ><b-card-text>
                    <b-form>
                      <b-form-group
                        id="input-group-1"
                        label="Username:"
                        label-for="input-1"
                      >
                        <b-form-input
                          id="input-1"
                          type="text"
                          placeholder="Username"
                          required
                          v-model="username"
                        ></b-form-input>
                      </b-form-group>

                      <b-form-group
                        class="mt-5 mb-5"
                        id="input-group-2"
                        label="Password:"
                        label-for="input-2"
                      >
                        <b-form-input
                          id="input-2"
                          placeholder="Enter Password"
                          v-model="password"
                          type="password"
                          required
                        ></b-form-input>
                      </b-form-group>

                      <b-button variant="primary" @click="login"
                        >Login
                        {{ username != "" ? "as " + username : "" }}</b-button
                      >
                    </b-form>
                    <!-- Show login error message -->
                    <div v-if="loginErrorMessage" class="success-message">
                      {{ loginErrorMessage }}
                    </div>
                    <!-- Show login message -->
                    <div v-if="loginMessage" class="success-message">
                      {{ loginMessage }}
                    </div>
                  </b-card-text></b-tab
                >
                <b-tab title="Register"
                  ><b-card-text>
                    <b-form>
                      <b-form-group
                        id="input-group-1"
                        label="Username:"
                        label-for="input-3"
                      >
                        <b-form-input
                          id="input-3"
                          type="text"
                          placeholder="Username"
                          v-model="username"
                          required
                        ></b-form-input>
                      </b-form-group>

                      <b-form-group
                        class="mt-5 mb-5"
                        id="input-group-2"
                        label="Password:"
                        label-for="input-4"
                      >
                        <b-form-input
                          id="input-4"
                          placeholder="Enter Password"
                          v-model="password"
                          type="password"
                          required
                        ></b-form-input>
                      </b-form-group>

                      <b-button variant="primary" @click="register"
                        >Register</b-button
                      >
                    </b-form>
                    <div v-if="registrationSuccess" class="success-message">
                      Registration Successful! Please wait for approval.
                    </div>
                    <div v-if="registrationError" class="success-message">
                      {{ registrationError }}
                    </div>
                  </b-card-text></b-tab
                >
              </b-tabs>
            </b-card>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      registrationSuccess: false,
      loginErrorMessage: false,
      loginMessage: false,
      registrationError: false,
    };
  },
  methods: {
    register() {
      axios
        .post("http://localhost:8080/api/user/register", {
          username: this.username,
          password: this.password,
        })
        .then((response) => {
          if (response.data.message === "success") {
            // Registration successful
            this.registrationSuccess = true;

            // Show the flash message for a few seconds (e.g., 5 seconds)
            setTimeout(() => {
              this.registrationSuccess = false;
            }, 5000); // 5000 milliseconds = 5 seconds
          } else if (response.data.message === "Username already exists") {
            this.registrationError = "Username already exists"; //.message.trim();
            console.log(response.data.message);
            console.log(this.registrationError);
            setTimeout(() => {
              this.registrationError = false;
            }, 5000); // 5000 milliseconds = 5 seconds
          } else if (response.data.message === "Invalid username or password") {
            this.registrationError = "Invalid username or password"; //.message.trim();
            console.log(response.data.message);
            console.log(this.registrationError);
            setTimeout(() => {
              this.registrationError = false;
            }, 5000); // 5000 milliseconds = 5 seconds
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },

    login() {
      axios
        .post("http://localhost:8080/api/login", {
          username: this.username,
          password: this.password,
        })
        .then((response) => {
          console.log("Response:", response.data); // Log the entire response
          const { message } = response.data;
          //console.log("Message:", message); // Log the message

          if (message === "User login successful") {
            const { user_role, user_name, user_id } = response.data;
            const token = response.data.access_token;
            console.log("Successful Login");
            this.$store.commit("setToken", token);
            this.$store.commit("setUsername", user_name);
            this.$store.commit("setUserId", user_id);
            this.$store.commit("setRole", user_role);

            localStorage.setItem("username", this.username);

            if (user_role == "admin") {
              console.log("User is admin");
              localStorage.setItem("isAdmin", true);
              this.$router.push("/admindashboard1");
            } else {
              console.log("User is not admin");
              this.$router.push("/userdashboard");
            }
          } else if (message === "Invalid username or password") {
            console.log(
              "Unsuccessful Login due to Invalid username or password"
            );
            this.loginErrorMessage =
              "Invalid username or password. Please try again.";
            setTimeout(() => {
              this.loginErrorMessage = false;
            }, 5000); // 5000 milliseconds = 5 seconds
          } else if (
            message === "Your registration is not approved, please wait"
          ) {
            console.log("Unsuccessful Login due to user not approved");
            this.loginErrorMessage =
              "Your registration is not approved. Please wait for approval.";
            setTimeout(() => {
              this.loginErrorMessage = false;
            }, 5000); // 5000 milliseconds = 5 seconds
          }
        })
        .catch((error) => {
          console.log("Error caught:", error); // Log the caught error
          this.loginErrorMessage = "An error occurred. Please try again later.";
          setTimeout(() => {
            this.loginErrorMessage = false;
          }, 5000); // 5000 milliseconds = 5 seconds
        });
    },
  },
};
</script>
<style>
/* ... existing styles ... */

.registration-success {
  margin-top: 10px;
  padding: 10px;
  background-color: #4caf50; /* Green background color for success message */
  color: white;
  text-align: center;
  display: none; /* Hide the message by default */
}

.registration-success.show {
  display: block; /* Display the message when .show class is added */
}

.login-error {
  margin-top: 10px;
  padding: 10px;
  background-color: #f44336; /* Red background color for error message */
  color: white;
  text-align: center;
  display: none; /* Hide the message by default */
}

.login-error.show {
  display: block; /* Display the message when .show class is added */
}

.login-success {
  margin-top: 10px;
  padding: 10px;
  background-color: #4caf50; /* Green background color for success message */
  color: white;
  text-align: center;
  display: none; /* Hide the message by default */
}

.login-success.show {
  display: block; /* Display the message when .show class is added */
}
</style>
