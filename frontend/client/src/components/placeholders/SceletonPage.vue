<template>
  <div class="loading-spinner">
    <!-- Use CSS to style the spinner -->
    <div class="spinner"></div>
    <div>Loading...</div>
  </div>
  <div>
    <button @click="toggle">Toggle</button>
    <transition name="fade">
      <div v-if="show" class="box"></div>
    </transition>
  </div>
</template>
<script>
import { ref } from 'vue';

export default {


  setup() {
    const show = ref(false);

    const toggle = () => {
      show.value = !show.value;
    }

    return { toggle, show } 
  }
}
</script>
  
<style>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.3);
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
.box {
  width: 100px;
  height: 100px;
  background-color: #3498db;
}
</style>