<template>
    <div class="head jumbotron" type="button" data-bs-toggle="modal" data-bs-target="#updateModal">
        <p class="card-text" v-markdown="item.body"></p>
    </div>
    <!-- Modal -->
    <div class="modal fade" id="updateModal" tabindex="-1" aria-labelledby="updateModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="item modal-title fs-5">Update "{{ item.name }}"</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="updateFormControlInput1" class="form-label">Name</label>
                        <input type="text" class="form-control" id="updateFormControlInput1" :placeholder="item.name"
                            v-model="newName">
                    </div>
                    <div class="mb-3">
                        <label for="updateFormControlTextarea1" class="form-label">Content</label>
                        <textarea class="form-control" id="updateFormControlTextarea1" rows="3"
                            v-model="newBody">{{ newBody }}</textarea>
                    </div>
                </div>

                <div class="modal-footer">
                    <form class="update-item" @submit="handleUpdate">
                        <button type="submit" class="btn btn-warning" data-bs-dismiss="modal">Update</button>
                    </form>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import updateItem from '../../../composables/techs/items/updateItem'
import VueMarkdown from 'vue-markdown'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

export default {
    components: {
        VueMarkdown
    },
    props: ["item"],
    setup(props, context) {
        const router = useRouter()
        const { error, updateitem } = updateItem()

        const newName = ref(props.item.name)
        const newBody = ref(props.item.body)

        const handleUpdate = () => {
            updateitem(props.item.id, newName.value, newBody.value)
            if (!error.value) {
                console.log("Item updated")
            }
        }

        return { handleUpdate, error, newName, newBody }
    }

}
</script>

<style>

</style>