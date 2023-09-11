<template>
    <Navbar />
</template>

<script>

import Navbar from '../components/Navbar.vue'


export default {
    components: {
        Navbar,
    },
    setup() {

    },
}
</script>

<style>
nav {
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;

}

nav p {
    margin: 2px auto;
    font-size: 16px;
    color: #6d6875;
}

nav p.email {
    font-size: 14px;
    color: #b5838d;
}

</style>