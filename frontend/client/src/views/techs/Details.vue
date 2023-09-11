<template>
    <Navbar />
    <div class="container">
        <div v-if="error">{{ error }}</div>

        <div v-if="technology">
            <UpdateTech :tech="technology" />
            <div class="container">
                <div v-if="!technology.items && technology.items === 0">
                    <ItemPh />
                </div>
                <div v-else-if="technology.items.length > 0">
                    <Items :tech_id="technology.id" :items="technology.items"/>
                </div>
                <div v-else>
                    <div class="alert alert-danger" role="alert">No items yet...</div>
                    <CreateItem :tech_id="technology.id" />
                </div>
            </div>
            <div class="item">

                <RemoveTech :tech="technology" />
                <button type="return" class="btn btn-secondary" @click="handleBack">
                    Return
                </button>

            </div>
        </div>
    </div>
</template>


<script>
import getTech from '../../composables/techs/getTech'
import CreateItem from '../../components/techs/items/CreateItem.vue'
import { useRouter } from 'vue-router'
import RemoveTech from '../../components/techs/RemoveTech.vue'
import UpdateTech from '../../components/techs/UpdateTech.vue'
import Navbar from '../../components/Navbar.vue'
import ItemPh from '../../components/placeholders/ItemPh.vue'
import Items from '../../components/techs/items/Items.vue'


export default {

    components: {
        Navbar,
        ItemPh,
        CreateItem,
        RemoveTech,
        UpdateTech,
        Items,
    },
    props: ["tech_id"],
    setup(props) {
        const router = useRouter()
        const { technology, error, gettech } = getTech()

        gettech(props.tech_id)

        const handleBack = () => {
            router.push({ name: "Technologies" })
        }
        return { technology, error, handleBack }
    }


}
</script>

<style>
.head p {
    margin: 2rem 1rem 1rem 1rem;
    text-align: justify;
}

.list-group {
    margin: 1rem 1rem auto;
}

.list-group {
    margin: 1rem;
}

.item {
    display: flex;
    justify-content: space-between;
    margin: 1rem;
}
</style>