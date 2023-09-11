<template>
  <router-view></router-view>
</template>

<script>

export default {
  components: {

  },
  created() {

  },
  data() {
    return {
      activePage: 0,
      technologies: {},
      showModal: true,
    }
  },
  methods: {
    toggleModel() {
      this.showModal = !this.showModal
    }
  }
}
</script>
<style></style>