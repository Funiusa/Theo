<template>
    <form @submit.prevent="handleSubmit">
        <div class="mb-3">
            <label for="inputEmail1" class="form-label">Email address</label>
            <input type="email" required class="form-control" id="inputEmail1" aria-describedby="emailHelp"
                v-model="displayEmail">
            <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
        </div>
        <div class="mb-3">
            <label for="inputUsername" class="form-label">Username</label>
            <input type="username" required class="form-control" id="inputUsername" aria-describedby="usernameHelp"
                v-model="newUsername">
            <div id="usernameHelp" class="form-text">Be smart</div>
        </div>

        <label for="inputPassword5" class="form-label">Password</label>
        <input type="password" id="inputPassword5" class="form-control" aria-describedby="passwordHelpBlock"
            v-model="newPwd">
        <div id="passwordHelpBlock" class="form-text">
            Must be 8-20 characters long.
        </div>
        <div class="error">{{ error }}</div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
</template>


<script>
import { ref } from 'vue';
import useSingup from '../composables/useSignup'


export default {
    setup(props, context) {
        const { error, signup } = useSingup()

        const displayEmail = ref('')
        const newUsername = ref('')
        const newPwd = ref('')

        const handleSubmit = async () => {
            await signup(displayEmail.value, newUsername.value, newPwd.value)
            if (!error.value) {
                context.emit('signup')
                console.log("Signup success")

            }

        }

        return { displayEmail, newUsername, newPwd, handleSubmit, error }
    }
}
</script>