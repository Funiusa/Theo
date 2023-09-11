import { ref } from "vue"

const tech = ref(null)
const error = ref(null)

const create = async (title, description) => {
    error.value = null
    tech.value = null
    const token = localStorage.getItem('token')

    try {
        const response = await fetch('http://0.0.0.0:8000/api/v1/technologies/', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
            body: JSON.stringify({
                title: title,
                description: description,
            })
        })
        if (!response.ok) {
            const messageError = await response.json()
            error.value = messageError.detail
            throw Error(messageError.detail)
        }

        tech.value = await response.json()
        error.value = null
        return tech

    } catch (err) {
        console.log(err.value)
        error.value = err.message

    }
}
const createTech = () => {
    return { error, create }
}

export default createTech