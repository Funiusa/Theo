import { ref } from "vue"

const item = ref(null)
const error = ref(null)

const updateitem = async (item_id, newName, newBody) => {
    error.value = null
    item.value = null
    const token = localStorage.getItem('token')

    try {
        
        const response = await fetch('http://0.0.0.0:8000/api/v1/items/' + item_id, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
            body: JSON.stringify({
                name: newName,
                body: newBody,
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
const updateItem = () => {
    return { error, item, updateitem }
}

export default updateItem