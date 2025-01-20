/* eslint-disable */
<template>
  <div class="landing"></div>
</template>

<script>
export default {
  data() {
    return {};
  },
  created: function () {
    localStorage.clear();
    this.$router.push("/");
  },
};
</script>
