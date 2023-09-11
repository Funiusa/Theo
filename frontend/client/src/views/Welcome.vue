<template>
    <div class="welcome container">
        <p>Welcome</p>
        <div v-if="showLogin">
            <h2>Login</h2>
            <SigninForm @login="enterProfile"/>
            <p>No account yet? <span @click="showLogin = false">Signup</span></p>
        </div>
        <div v-else>
            <h2>Sign up</h2>
            <SignupForm @signup="enterProfile"/>
            <p>Already registerd? <span @click="showLogin = true">Signin</span></p>
        </div>
    </div>
</template>



<script>
import SigninForm from '../components/SigninForm.vue'
import SignupForm from '../components/SignupForm.vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
    components: {
        SigninForm,
        SignupForm
    },
    setup() {
        const router = useRouter()
        const showLogin = ref(true)

        const enterProfile = () => {
            showLogin.value = true
            router.push({name: 'Profile'})
        }
        return { showLogin, enterProfile }
    }
}

</script>

<style>
.welcome {
    padding: 10rem;

}

.welcome p {
    text-align: center;
    font-size: 20px;
    padding-top: 20px;
}

.welcome h2 {
    text-align: center;
    font: 45px bold, Hack; 
    padding-top: 20px;
}

.welcome form {
    width: 300px;
    margin: 20px auto;
}

.welcome label {
    margin: 20px 0 10px;
}

.welcome span {
    font-weight: bold;
    text-decoration: underline;
    cursor: pointer;
}
</style>