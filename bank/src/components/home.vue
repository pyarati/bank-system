<template>
  <div>
    <headers />
    <h1>Welcome {{ name }}</h1>
  </div>
</template>

<script>
import headers from "./headers.vue";
export default {
  name: "home",
  data() {
    return {
      user: "",
      name: localStorage.getItem("name"),
      item: undefined,
    };
  },
  components: {
    headers,
  },
  async mounted() {

    let user = localStorage.getItem("id");
    this.user = user;
    if (!user) {
      this.$router.push({ name: "signup" });
    }
  },
};
</script>

<style>
</style>
