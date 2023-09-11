import { ref } from "vue"

const item = ref(null)
const error = ref(null)

const createnew = async (tech_id, itemName, body) => {
    error.value = null
    item.value = null
    const token = localStorage.getItem('token')

    try {
        const response = await fetch('http://0.0.0.0:8000/api/v1/technologies/' + tech_id + "/items/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
            body: JSON.stringify({
                technology_id: tech_id,
                name: itemName,
                body: body,
            })
        })
        if (!response.ok) {
            const messageError = await response.json()
            error.value = messageError.detail
            throw Error(messageError.detail)
        }

        item.value = await response.json()
        error.value = null

    } catch (err) {
        console.log(err.value)
        error.value = err.message

    }
}
const createNewItem = () => {
    return { error, item, createnew }
}

export default createNewItem