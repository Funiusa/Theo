import { ref } from 'vue';


const technology = ref(null)
const error = ref(null)

export const gettech = async (tech_id) => {
    try {
        technology.value = null
        const token = localStorage.getItem("token")
        let response = await fetch('http://0.0.0.0:8000/api/v1/technologies/' + tech_id, {
            headers: { Authorization: 'Bearer ' + token },
        })
        if (!response.ok) {
            throw Error("Technology does not exists")
        }
        technology.value = await response.json()

    }
    catch (err) {
        error.value = err.message
        console.log(err.value)
    }
}

const getTech = () => {

    return { technology, error, gettech }
}

export default getTech