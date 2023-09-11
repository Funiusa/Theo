<template>
    <Navbar />
    <div class="container">
        <div class="container">
            <div class="jumbotron">
                <h1>{{ newTitle }}</h1>
            </div>
            <div class="mb-3">
                <label class="form-label">Title: </label>
                <input class="form-control" required placeholder="Insert a title..." v-model="newTitle">
            </div>
            <div class="mb-3">
                <label class="form-label">Description:</label>
                <textarea class="form-control" required rows="3" v-model="newDescription"></textarea>
            </div>
            <div class="d-grid gap-2 d-md-flex justify-content-md-between">
                <form class=create-tech @click="handleCreate">
                    <button type="button" class="btn btn-success">
                        Create
                    </button>
                </form>
                <button type="button" class="btn btn-secondary" @click="handleBack">
                    Return
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import createTech from '../../composables/techs/createTech'
import Navbar from '../Navbar.vue'

export default {
    components: {
        Navbar,
    },
    setup() {
        const router = useRouter()
        const newTitle = ref("")
        const newDescription = ref("")

        const handleBack = () => {
            router.push({ name: "Technologies" })
        }

        const { error, create } = createTech()

        const handleCreate = async () => {
            const tech = await create(newTitle.value, newDescription.value)
            if (!error.value) {
                console.log("Technology created")
                router.push({ name: "Details", params: {tech_id: tech.value.id} })
            }
        }

        return { handleBack, handleCreate, newTitle, newDescription }
    }

}
</script>

<style>
.container {
    padding: 5px;
}

.buttons {
    display: flex;
    justify-content: between;
}
</style>