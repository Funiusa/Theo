import { ref } from 'vue';

const items = ref([])
const error = ref(null)


const getitems = async (tech_id) => {
    items.value = null
    const token = localStorage.getItem("token")
    try {
        let response = await fetch('http://0.0.0.0:8000/api/v1/technologies/' + tech_id + "/items", {
            headers: { Authorization: 'Bearer ' + token },
        })
        if (!response.ok) {
            throw Error("no data available")
        }
        items.value = await response.json()
    }
    catch (err) {
        error.value = err.message
        console.log("Error", err.value)
    }
}


const getItems = (tech_id) => {
    getitems(tech_id)
    return { items }
}

export default getItems