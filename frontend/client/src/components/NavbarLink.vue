<template>
    <a 
        class="nav-link" 
        :class="activeClasses"
        href="Technologies"
        :title="`This page technologies`"
        >Tech
    </a>
</template>

<script>
    export default {
        props: ["page", "isActive"],
        computed: {
            activeClasses() {
                return {
                    active: this.isActive,
                    emphasize: this.isActive,
                };
            }
        }
    }
</script>

<style scoped>
.emphasize {
    text-decoration: underline !important;
    }
</style>