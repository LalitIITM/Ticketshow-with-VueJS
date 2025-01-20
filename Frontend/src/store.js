/* eslint-disable */

import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    token: localStorage.getItem("token") || null,
    username: localStorage.getItem("username") || "",
    role: localStorage.getItem("role") || "",
    user_id: localStorage.getItem("user_id") || "",
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      localStorage.setItem("token", token);
    },
    setUsername(state, username) {
      state.username = username;
      localStorage.setItem("username", username);
    },
    setRole(state, role) {
      state.role = role;
      localStorage.setItem("role", role);
    },
    setUserId(state, user_id) {
      state.user_id = user_id;
      localStorage.setItem("user_id", user_id);
    },
    clearToken(state) {
      state.token = null;
      state.username = "";
      state.role = "";
      state.user_id = "";
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      localStorage.removeItem("role");
      localStorage.removeItem("user_id");
    },
  },
  actions: {
    setToken({ commit }, access_token) {
      commit("setToken", access_token);
    },
    setUsername({ commit }, user_name) {
      commit("setUsername", user_name);
    },
    setRole({ commit }, user_role) {
      commit("setRole", user_role);
    },
    setUserId({ commit }, user_id) {
      commit("setUserId", user_id);
    },
    clearToken({ commit }) {
      commit("clearToken");
    },
  },
  getters: {
    getToken(state) {
      return state.token;
    },
    getUsername(state) {
      return state.username;
    },
    getRole(state) {
      return state.role;
    },
    getUserId(state) {
      return state.user_id;
    },
  },
});

export default store;
