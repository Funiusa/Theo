<template>
    <form @submit.prevent="handleSubmit">
        <div class="mb-3">
            <label for="inputEmail1" class="form-label">Email address</label>
            <input type="email" required class="form-control" id="inputEmail1" aria-describedby="emailHelp"
                v-model="displayEmail">
            <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
        </div>
        <div class="mb-3">
            <label for="inputPassword" class="form-label">Password</label>
            <input type="password" required class="form-control" id="inputPassword" v-model="password">
        </div>
        <div class="error">{{ error }}</div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
</template>

<script>
import { ref } from 'vue';
import useSignin from '../composables/useSignin';


export default {
    setup(props, context) {
        const { error, signin, access_token } = useSignin()

        const displayEmail = ref('')
        const password = ref('')


        const handleSubmit = async () => {
            await signin(displayEmail.value, password.value)
            if (!error.value) {
                context.emit('login')
            }
        }
        return { displayEmail, password, handleSubmit, error, access_token }

    }

}
</script>