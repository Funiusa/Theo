import { ref } from 'vue';


const user = ref(null)
const error = ref(null)


user.value = null

const getuser = async () => {

    try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://0.0.0.0:8000/api/v1/users/me/', {
            headers: { Authorization: 'Bearer ' + token },
        })

        if (!response.ok) {
            throw Error("no data available")
        }
        user.value = null
        user.value = await response.json()
    }
    catch (err) {
        error.value = err.message
        console.log(err.value)
    }
}
// export function getCurrentUser() {
//     const currentUser = localStorage.getItem("current")
//     return currentUser
// }
const getUser = () => {
    return { user, error, getuser }
}

// export const getCurrent = () => {
//     return { user }
// }

export default getUser