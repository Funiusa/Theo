<template>
    <div class="tech-remove">
        <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#removeModal">
            Remove
        </button>
    </div>

    <!-- Modal -->

    <div class="modal fade" id="removeModal" tabindex="-1" aria-labelledby="removeModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="item modal-title fs-5">Remove "{{ tech.title }}"</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    Are you shore, you want to remove {{ tech.title }}?
                </div>
                <div class="modal-footer">
                    <form class="itme-remove" @click="handleRemove(tech.id)">
                        <button type="submit" class="btn btn-danger" data-bs-dismiss="modal">
                            Remove</button>
                    </form>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>

                </div>
            </div>
        </div>
    </div>
</template>

<script>
import removeTech from '../../composables/techs/removeTech'
import { useRouter } from 'vue-router'

export default {
    props: ["tech"],
    setup(props, context) {
        const router = useRouter()
        const { error, removetech } = removeTech()


        const handleRemove = async (tech_id) => {
            await removetech(tech_id)
            if (!error.value) {
                router.push({ name: "Technologies" })
            }
        }
        return { handleRemove, error }
    }
}
</script>

<style></style>