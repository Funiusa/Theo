<template>
    <div class="row">
        <div class="col-sm-6"  v-for="card in 3" :key="card">
            <div class="card-tech" aria-hidden="true">
                <!-- <img src="..." class="card-img-top" alt="..."> -->
                <div class="card-body">
                    <h5 class="card-title placeholder-glow">
                        <span class="placeholder col-6"></span>
                    </h5>
                    <p class="card-text placeholder-glow" v-for="num in 4" :key="num">
                        <span :class="`placeholder col-${ num }`"></span>
                    </p>
                </div>
            </div>
        </div>  
    </div>
</template>

<script>

export default {
    components: {
    },
    setup() {
    },
}
</script>

<style></style>