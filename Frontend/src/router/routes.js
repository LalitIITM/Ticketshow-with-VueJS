/* eslint-disable */

import Vue from "vue";
import VueRouter from "vue-router";

import AllShows from "@/components/AllShows.vue";
import AllVenues from "@/views/AllVenues.vue";
import TestComponent from "@/components/TestComponent.vue";
import LogoutView from "@/views/LogoutView.vue";
import LoginView from "@/views/LoginView.vue";
import HomeView from "@/views/HomeView.vue";
import VenuesView from "@/views/VenuesView.vue";
import AddVenue from "@/views/AddVenue.vue";
import AddShow from "@/views/AddShow.vue";
import AddBooking from "@/views/AddBooking.vue";
import AboutView from "@/views/AboutView.vue";
import ShowsView from "@/views/ShowsView.vue";
import UsersView from "@/views/UsersView.vue";
import UserDashboard from "@/views/UserDashboard.vue";
import AdminBookings from "@/views/AdminBookings.vue";
import MyBookings from "@/views/MyBookings.vue";
import CreateVenue from "@/components/CreateVenue.vue";
import CreateShow from "@/components/CreateShow.vue";
import AdminDashboard1 from "@/views/AdminDashboard1.vue";
import SearchView from "@/views/SearchView.vue";

Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "Home",
      component: HomeView,
      meta: {
        requiresAuth: false,
      },
    },
    {
      path: "/venues",
      name: "Venues",
      component: VenuesView,
    },
    {
      path: "/addvenue",
      name: "AddVenue",
      component: AddVenue,
    },
    {
      path: "/addshow",
      name: "AddShow",
      component: AddShow,
    },
    {
      path: "/addbooking",
      name: "AddBooking",
      component: AddBooking,
    },
    {
      path: "/aboutus",
      name: "About",
      component: AboutView,
    },
    {
      path: "/search",
      name: "Search",
      component: SearchView,
    },

    {
      path: "/admindashboard1",
      name: "Admin1",
      component: AdminDashboard1,
      meta: { requiresAdmin: true },
    },
    {
      path: "/userdashboard",
      name: "UserDashboard",
      component: UserDashboard,
      meta: { requiresAuth: true },
    },
    {
      path: "/shows",
      name: "Shows",
      component: ShowsView,
    },
    {
      path: "/users",
      name: "Users",
      component: UsersView,
    },

    {
      path: "/login",
      name: "Login",
      component: LoginView,
    },
    {
      path: "/logout",
      name: "Logout",
      component: LogoutView,
    },

    {
      path: "/admin/bookings",
      name: "AdminBookings",
      component: AdminBookings,
    },

    {
      path: "/user/my_bookings",
      name: "MyBookings",
      component: MyBookings,
    },
    {
      path: "/create_venue",
      name: "CreateVenue",
      component: CreateVenue,
    },
    {
      path: "/create_show",
      name: "create-show",
      component: CreateShow,
    },
    {
      path: "/show",
      name: "AllShows",
      component: AllShows,
    },
    {
      path: "/venue",
      name: "AllVenues",
      component: AllVenues,
    },

    {
      path: "/test",
      name: "Test",
      component: TestComponent,
    },
  ],
});

router.beforeEach((to, from, next) => {
  // Check if the route requires authentication
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // Check if the user is authenticated (e.g., check for a token in localStorage)
    const token = localStorage.getItem("token");
    if (!token) {
      // If there's no token, redirect to the login page
      next({
        name: "Login",
      });
    } else {
      // If there's a token, proceed to the route
      next();
    }
  } else if (to.matched.some((record) => record.meta.requiresAdmin)) {
    // Check if the user is authenticated (e.g., check for a token in localStorage)
    const isAdmin = localStorage.getItem("isAdmin");
    if (!isAdmin || isAdmin == false) {
      // If there's no token, redirect to the login page
      next({
        name: "Login",
      });
    } else {
      // If there's a token, proceed to the route
      next();
    }
  } else {
    // If the route doesn't require authentication, proceed
    next();
  }
});

export default router;
/* eslint-enable */
