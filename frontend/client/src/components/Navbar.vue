<template>
  <div class="container" v-if="user">
    <nav>
      <!-- <div>
        <p>Hay there {{ user.username }}</p>
        <p class="email">Your current email is {{ user.email }}</p>
  
      </div> -->
      <NavbarLink/>
      <button class="btn btn-primary" @click.prevent="handleClick">Logout</button>

    </nav>

  </div>

</template>

<script>
import NavbarLink from './NavbarLink.vue';
import useLogout from '../composables/useLogout'
import getUser  from '../composables/getUser'
import { useRouter } from 'vue-router'
import { onMounted } from 'vue';

export default {
  props: [],
  components: {
    NavbarLink,
  },
  setup() {

    const router = useRouter()
    const { logout, error } = useLogout()
    const { user, getuser } = getUser()

    onMounted(async () => {
      await getuser()
    })

    const handleClick = async () => {
      await logout()

      if (!error.value) {
        console.log("User logged out")
      }
      router.push({name: 'Welcome'})
    }


    return { handleClick, user }
  }

}
</script>

<style></style>