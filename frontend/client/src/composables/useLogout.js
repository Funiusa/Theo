import { ref } from "vue"

const error = ref(null)

const logout = async () => {
    error.value = null

    try {
        localStorage.removeItem("token")
        localStorage.removeItem("current")
    } catch (err) {
        console.log(err.value)
        error.value = err.message
    }
}
const useLogout = () => {
    return { error, logout }
}

export default useLogout