import { ref } from "vue"

const error = ref(null)


const signin = async (displayEmail, password) => {
    error.value = null
    const formData = new URLSearchParams();
    formData.append('username', displayEmail);
    formData.append('password', password);

    try {

        const response = await fetch('http://0.0.0.0:8000/api/v1/login/', {
            method: "POST",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        })
        if (!response.ok) {
            const errorMessage = await response.json();
            error.message = errorMessage.detail
            throw new Error(errorMessage.detail)
        }
        const responseData = await response.json()
        localStorage.setItem("token", responseData.access_token)
        localStorage.setItem("current", displayEmail)
        error.value = null

    } catch (err) {
        console.log(err.value)
        error.value = err.message
    }
}
const useSignin = () => {
    return { error, signin }
}

export default useSignin