import { ref } from 'vue';

const error = ref(null)

const removetech = async (tech_id) => {
    const token = localStorage.getItem("token")
    try {
        const response = await fetch('http://0.0.0.0:8000/api/v1/technologies/' + tech_id, {
            method: 'DELETE',
            headers: { Authorization: 'Bearer ' + token },
        })
        if (!response.ok) {
            error.message = await response.json();
            throw new Error(error.message)
        }
        error.value = null

    } catch (err) {
        console.log(err.value)
        error.value = err.message
    }
}

const removeTech = () => {
    return { error, removetech }
}

export default removeTech