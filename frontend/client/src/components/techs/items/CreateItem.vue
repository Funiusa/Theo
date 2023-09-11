<template>

    <div class="list-group">
        <a class="list-group-item list-group-item-action" data-bs-toggle="modal" data-bs-target="#createItemModal"
            aria-current="true" href="">
            <div class="item-content">+</div>
        </a>
    </div>

    <!-- Modal -->

    <div class="modal fade" id="createItemModal" tabindex="-1" aria-labelledby="createItemModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="item modal-title fs-5">Create item</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div v-if="error">{{ error }}</div>
                    <div class="mb-3">
                        <label class="form-label">Item name</label>
                        <input type="name" required class="form-control" placeholder="Insert the name" v-model="newName">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Content</label>
                        <textarea class="form-control" required rows="3" v-model="newBody"></textarea>
                    </div>

                </div>

                <div class="footer">
                    <form class=create-item @click="handleCreate">
                        <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Create
                            item</button>
                    </form>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
import { computed, ref } from 'vue'
import createNewItem from '../../../composables/techs/items/createNewItem'


export default {
    props: ["item", "tech_id"],
    setup(props) {
        const newName = ref("")
        const newBody = ref("")


        const { error, item, createnew } = createNewItem()

        const handleCreate = () => {
            createnew(props.tech_id, newName.value, newBody.value)
        }
        const snippet = computed(() => {
            return props.item.body.substring(0, 100) + '...'
        })
        return { snippet, newName, newBody, handleCreate, error }
    }

}
</script>

<style>
.item-content {
    display: flex;
    justify-content: center;

}

.footer {
    display: flex;
    justify-content: space-between;
    margin: 1rem;
}
</style>