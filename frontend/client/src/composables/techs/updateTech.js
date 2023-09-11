import { ref } from "vue"

const tech = ref(null)
const error = ref(null)

const updatetech = async (tech_id, newTitle, newDescription) => {
    error.value = null
    tech.value = null
    const token = localStorage.getItem('token')

    try {
        
        const response = await fetch('http://0.0.0.0:8000/api/v1/technologies/' + tech_id, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
            body: JSON.stringify({
                title: newTitle,
                description: newDescription,
            })
        })
        if (!response.ok) {
            const messageError = await response.json()
            error.value = messageError.detail
            throw Error(messageError.detail)
        }

        tech.value = await response.json()
        error.value = null

    } catch (err) {
        console.log(err.value)
        error.value = err.message

    }
}
const updateTech = () => {
    return { error, tech, updatetech }
}

export default updateTech