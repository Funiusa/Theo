<template>
    <div class="home container">
        <div class="jumbotron">
            <h1>Theory Bot</h1>
            <p>Bootstrap is the most popular HTML, CSS, and JS framework for developing
                responsive, mobile-first projects on the web.</p>
        </div>
    </div>
</template>

<script>
// import getTechnologies from '../composables/getTechnologies'
// import SignupForm from '../components/SignupForm.vue'


export default {


    props: ["tech"],
    components: {

    },
    setup() {
    },
}
</script>

<style>
.home {
    padding: 10rem
}
</style>