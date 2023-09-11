<template>
    <div class="item-remove">
        <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#removeModal">
            Remove
        </button>
    </div>

    <!-- Modal -->
    <form class="itme-remove" @click="handleRemove">
        <div class="modal fade" id="removeModal" tabindex="-1" aria-labelledby="removeModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="item modal-title fs-5">Remove "{{ item.name }}"</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        Are you shore, you want to remove {{ item.name }}?
                    </div>
                    <div class="modal-footer">

                        <button type="submit" class="btn btn-danger" data-bs-dismiss="modal">Remove</button>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>

                    </div>
                </div>
            </div>
        </div>
    </form>
</template>

<script>
import removeItem from '../../../composables/techs/items/removeItem'
import { useRouter } from 'vue-router'

export default {
    props: ["item"],
    setup(props, context) {
        const router = useRouter()
        const { error, removeitem } = removeItem()


        const handleRemove = (item_id) => {
            removeitem(item_id)
            if (!error.value) {
                context.emit('details')
            }

            router.push({ name: "Details" })
            window.location.reload()

        }

        return { handleRemove, error }
    }

}
</script>

<style></style>