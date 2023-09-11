<template>
    <div class="list-group">
        <a class="list-group-item list-group-item-action" aria-current="true" href="" v-for="item in items">
            <div class="d-flex w-100 justify-content-between" @click.prevent="handleItem(item.id, item)">
                <h5 class="mb-1" v-markdown="item.name"></h5>
                <p v-markdown="item.body.slice(0, 20)"></p>
            </div>
        </a>
    </div>

    <CreateItem :tech_id="tech_id" />
</template>

<script>
import SingleTech from '../SingleTech.vue'
import CreateItem from './CreateItem.vue'

import { useRouter } from 'vue-router'

export default {
    components: {
        SingleTech,
        CreateItem,
    },
    props: ["tech_id", "items"],
    setup() {
        const router = useRouter()
        const handleItem = (item_id, item) => {
            router.push({ name: "Item", params: { item_id: item_id, item: item } })
        }

        return { handleItem }
    }
}
</script>

<style></style>
