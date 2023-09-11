<template>
    <Navbar/>
    <div v-if="error">{{ error }}</div>
    <div v-if="item">
        <div class="container">
            <div class="card text-center">
                <div class="card-header">
                    <h1 v-markdown="item.name"></h1>
                </div>
                <div class="card-body">
                    <UpdateItem :item="item" />
                </div>
                <div class="item">
                    <RemoveItem :item="item" />
                    <button type="button" class="btn btn-secondary me-md-2" @click="handleBack">Back</button>
                </div>
                <div class="card-footer text-muted">
                    2 days ago
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import getItem from '../../../composables/techs/items/getItem'
import RemoveItem from './RemoveItem.vue'
import UpdateItem from './UpdateItem.vue'

export default {
    components: {
        Navbar,
        RemoveItem,
        UpdateItem
    },
    props: ["item_id", "item"],
    setup(props) {
        const router = useRouter()
        const { error, item, getitem } = getItem()
        getitem(props.item_id)

        const handleBack = () => {
            router.push({ name: "Details" })
        }

        return { handleBack, item }
    }

}
</script>

<style>
.container {
    padding: 5px;
}

.card-header h1 {
    display: flex;
    justify-content: center;
    align-items: center;
}


.btn-toolbar {
    display: flex;
    justify-content: center;
}
</style>