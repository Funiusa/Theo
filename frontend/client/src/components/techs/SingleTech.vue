<template>
    <div class="card">
        <div class="card-body" @click="handleDetails(tech.id)">
            <h5 class="card-title">{{ tech.title }}</h5>
            <p class="card-text">{{ snippet }}</p>
        </div>
    </div>
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
    components: {
    },
    props: ['tech'],
    setup(props) {
        const router = useRouter()
        const snippet = computed(() => {
            return props.tech.description.substring(0, 80) + '...'
        })

        const handleDetails = (tech_id) => {
            router.push({ name: "Details", params: { tech_id: tech_id } })
        }
        return { snippet, handleDetails }
    },

}
</script>

<style>
.card {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 200px;
    min-height: 200px;
    margin: 0.5rem;
    cursor: pointer;

}

.card-text {
    margin-top: 2rem;
}

</style>