import { ref } from 'vue';

const technologies = ref([])
const error = ref(null)

const gettechs = async () => {
        technologies.value = null
        const token = localStorage.getItem("token")
        try {
            let response = await fetch('http://0.0.0.0:8000/api/v1/technologies/', {
                headers: { Authorization: 'Bearer ' + token },
            })
            if (!response.ok) {
                throw Error("no data available")
            }
            technologies.value = await response.json()
        }
        catch (err) {
            error.value = err.message
            console.log(err.value)
        }
    }


const getTechs = () => {
    return { technologies, gettechs }
}

export default getTechs