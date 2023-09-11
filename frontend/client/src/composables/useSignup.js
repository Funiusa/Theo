import { ref } from "vue"

const user = ref(null)
const error = ref(null)
const responseData = ref(null)

const signup = async (displayEmail, username, password) => {
    error.value = null
    user.value = null

    try {
        const response = await fetch('http://0.0.0.0:8000/api/v1/users/', {
            method: "POST",
            headers: { 
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: displayEmail,
                password: password,
            })
        })
        responseData.value = await response.json()
        console.log("response", responseData.value.detail)
        if (!response.ok) {
            error.value = responseData.value.detail
            throw Error(error.value)
        }
        error.value = null

    } catch (err) {
        error.value = err.message
    }
}
const useSignup = () => {
    return { error, user, signup }
}

export default useSignup