<template>
    <div class="head container" type="button" data-bs-toggle="modal" data-bs-target="#updateModal" @click="openModal">
        <div class="jumbotron">
            <h1 v-markdown="tech.title"></h1>
            <p v-markdown="tech.description"></p>
        </div>
    </div>

    <!-- Modal -->
    <div class="modal fade" id="updateModal" tabindex="-1" aria-labelledby="updateModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="item modal-title fs-5">Update "{{ tech.title }}"</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="updateFormControlInput1" class="form-label">Title</label>
                        <input type="text" class="form-control" id="updateFormControlInput1" :placeholder="tech.name"
                            v-model="newTitle">
                    </div>
                    <div class="mb-3">
                        <label for="updateFormControlTextarea1" class="form-label">Description</label>
                        <textarea class="form-control" id="updateFormControlTextarea1" rows="3"
                            v-model="newDescription">{{ newDescription }}</textarea>
                    </div>
                </div>

                <div class="modal-footer">
                    <form class=create-item @click.prevent="handleUpdate">
                        <button type="submit" class="btn btn-warning" data-bs-dismiss="modal"
                            >Update</button>
                    </form>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal"
                        @click="closeModal">Close</button>

                </div>
            </div>
        </div>
    </div>
</template>

<script>
import updateTech from '../../composables/techs/updateTech'
import { useRouter } from 'vue-router'
import { ref, computed } from 'vue'

export default {
    props: ["tech"],
    setup(props, context) {
        const router = useRouter()
        const { error, updatetech } = updateTech()
        const newTitle = ref(props.tech.title)
        const newDescription = ref(props.tech.description)

        const handleUpdate = async () => {
            await updatetech(props.tech.id, newTitle.value, newDescription.value)
            if (!error.value) {
                console.log("Tech updated")
                window.location.reload()
            }

        }

        return { handleUpdate, error, newTitle, newDescription }
    }

}
</script>

<style></style>