<template>
    <div class="container-fluid">
        <div v-if="technologies.length">
            <div class="row">
                <div v-if="error">{{ error }}</div>
                <div class="col-sm-6 mb-3 mb-sm-0" v-for="tech in technologies" :key="tech.id">
                    <SingleTech :tech="tech" />
                </div>

            </div>
        </div>
        
        <div class="container-fluid" v-else>
            <div class="alert alert-danger" role="alert" >
                No technologies yet.
            </div>
        </div>
    </div>
</template>

<script>
import SingleTech from './SingleTech.vue';
import getTechnologies from '../../composables/techs/getTechnologies'


export default {


    props: ["tech"],
    components: {
        SingleTech,
    },
    setup() {
        const { technologies, error, load } = getTechnologies()
        load()
        return { technologies, error }
    },
}
</script>