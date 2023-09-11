import { ref } from "vue"

const error = ref(null)

const removeitem = async (tech_id) => {
    error.value = null
    const token = localStorage.getItem('token')
    console.log(tech_id)
    try {
        const response = await fetch('http://0.0.0.0:8000/api/v1/items/' + tech_id, {
            method: "DELETE",
            headers: {
                Authorization: 'Bearer ' + token,
            }
        })
        if (!response.ok) {
            const messageError = await response.json()
            error.value = messageError.detail
            throw Error(messageError.detail)
        }
        error.value = null

    } catch (err) {
        console.log(err.value)
        error.value = err.message

    }
}
const removeItem = () => {
    return { error, removeitem }
}

export default removeItem