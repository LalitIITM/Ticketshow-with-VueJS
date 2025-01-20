import Vue from "vue";
import App from "./App.vue";
import router from "./router/routes.js";
import store from "./store";
import {
  BootstrapVue,
  IconsPlugin,
  CardPlugin,
  LayoutPlugin,
  ModalPlugin,
} from "bootstrap-vue";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
Vue.config.productionTip = false;

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue);
Vue.use(LayoutPlugin);
Vue.use(CardPlugin);
Vue.use(ModalPlugin);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);

new Vue({
  router, // Use the router configuration
  render: (h) => h(App),
  store,
}).$mount("#app");
