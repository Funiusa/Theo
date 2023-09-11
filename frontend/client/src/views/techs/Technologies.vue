<template>
    <Navbar/>
    <div class="tech container">
        <div class="jumbotron">
            <h1>Your technologies</h1>
        </div>
        <div class="container" v-if="!technologies">
            <TechnologyPh />
        </div>
        <div class="row" v-else-if="technologies && technologies.length > 0">
            <div class="col-sm-6" v-for="tech in technologies" :key="tech.id">
                <SingleTech :tech="tech" />
            </div>
            <NewTechPh @click="handleAddNew" />
        </div>

        <div class="row justify-content-center" v-else>
            <div class="alert alert-info" role="alert">
                You haven't any posts yet...
            </div>
            <NewTechPh @click="handleAddNew" />

        </div>

    </div>
</template>

<script>
import getTechs from '../../composables/techs/getTechs'
import SingleTech from '../../components/techs/SingleTech.vue'
import TechnologyPh from '../../components/placeholders/TechnologyPh.vue'
import NewTechPh from '../../components/placeholders/NewTechPh.vue'
import SceletonPage from '../../components/placeholders/SceletonPage.vue'
import Navbar from '../../components/Navbar.vue'

import { useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'

export default {
    components: {
        Navbar,
        SingleTech,
        TechnologyPh,
        NewTechPh,
        SceletonPage,
    },
    setup() {
        const router = useRouter()
        const { technologies, gettechs } = getTechs()
        onMounted(async () => {
            await gettechs()
        })


        const handleAddNew = () => {
            router.push({ name: 'CreateTech' })
        }

        return { technologies, handleAddNew }
    }
}
</script>

<style>


.content {
    font-size: 40px;
}


div.jumbotron {
    margin-top: 1rem;
    text-align: center;
}

div.alert {
    margin: 1rem;
}</style>
