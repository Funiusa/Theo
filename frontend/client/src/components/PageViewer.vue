<template>
    <div class="container">
        <h1>{{ page.pageTitle }}</h1>
        <p>{{ page.content }}</p>

    </div>
    <div class="container">
        <tech-viewer></tech-viewer>
    </div>
</template>

<script>
import TechViewer from './TechViewer.vue';

export default {
    components: {
        TechViewer,
    },
    props: ['page'],
    


}
</script>

   