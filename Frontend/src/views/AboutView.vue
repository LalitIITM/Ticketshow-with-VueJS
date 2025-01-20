<template>
  <div class="landing">
    <div class="center">
      <h1>Ticket Booking - About</h1>
      <h2>About us</h2>
      <p>
        The TicketShow web application is a comprehensive platform designed to
        streamline the process of booking movie tickets. Built using Flask for
        the backend and Vue.js for the frontend, TicketShow provides a seamless
        and user-friendly experience for both administrators and users. The app
        offers a range of features and functionalities that enhance the
        movie-ticket booking experience.
      </p>
      <p>
        <strong>Key Features:</strong>
      </p>
      <ul>
        <li>User Registration and Authentication</li>
        <li>Movie Ticket Booking</li>
        <li>Booking Management</li>
        <li>My Bookings</li>
        <li>Admin Management</li>
        <li>Search Functionality</li>
        <li>User-Friendly Interface</li>
      </ul>
      <p>
        The TicketShow project involves developing a web application that caters
        to the needs of movie enthusiasts and administrators. The backend is
        built using Flask, a versatile and powerful Python framework. Flask
        handles the core functionality, including user authentication, booking
        management, and CRUD operations.
      </p>
      <p>
        The frontend of TicketShow is developed using Vue.js, a progressive
        JavaScript framework that allows for dynamic and responsive user
        interfaces. Vue.js enables seamless interactions between users and the
        platform, offering a smooth and engaging experience.
      </p>
      <p>
        Administrators can log in to the app and access the Admin Dashboard.
        This dashboard serves as a central hub for managing venues and shows.
        CRUD operations on these entities ensure that the app's content remains
        accurate and up-to-date.
      </p>
      <p>
        Users can register and log in to the platform. They can browse shows,
        view venue details, and book tickets for their desired movie
        experiences. The "My Bookings" section keeps track of all their
        reservations.
      </p>
    </div>
    <router-link to="/" tag="button" class="btn btn-primary">
      <b-icon icon="arrow-left" aria-hidden="true"></b-icon> Back to Home
    </router-link>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {},
};
</script>

<style scoped>
/* Apply styles to the body element to control the background color */
body {
  background-color: #1a237e; /* Dark blue background color */
  color: #1a237e; /* Dark blue text color */
}

.center {
  text-align: center;
  margin: 30px;
}

.title {
  color: #1a237e; /* Dark blue text color for titles */
  font-size: 2em; /* Increase font size for titles */
}

.subtitle {
  color: #bbdefb; /* Light blue color for subtitles */
  font-size: 1.5em; /* Increase font size for subtitles */
}

.btn {
  margin-top: 20px;
}
</style>
