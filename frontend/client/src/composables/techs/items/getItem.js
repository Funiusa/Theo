import { ref } from 'vue';

const item = ref()
const error = ref(null)


const getitem = async (item_id) => {
    item.value = null
    const token = localStorage.getItem("token")
    try {
        let response = await fetch('http://0.0.0.0:8000/api/v1/items/' + item_id, {
            headers: { Authorization: 'Bearer ' + token },
        })
        if (!response.ok) {
            throw Error("no data available")
        }
        item.value = await response.json()
    }
    catch (err) {
        error.value = err.message
        console.log("Error", err.value)
    }
}


const getItem = () => {
    return { item, getitem }
}

export default getItem