import { createRouter, createWebHistory } from "vue-router";
import Home from '../views/Home.vue'
import Welcome from '../views/Welcome.vue'
import Details from '../views/techs/Details.vue'
import Profile from '../views/Profile.vue'
import CreateTech from '../components/techs/CreateTech.vue'
import Item from '../components/techs/items/Item.vue'
import Technologies from '../views/techs/Technologies.vue'


const requireAuth = (to, from, next) => {
    const user = localStorage.getItem("current")
    if (!user) {
        next({ name: "Welcome" })
    } else {
        next()
    }
}


const routes = [
    {
        path: '/',
        name: 'Welcome',
        component: Welcome
    },
    {
        path: '/profile/',
        name: 'Profile',
        component: Profile,
        beforeEnter: requireAuth,
    
    },
    {
        path: '/profile/technologies/',
        name: 'Technologies',
        component: Technologies,
        props: true
    },
    {
        path: '/profile/technologies/:tech_id',
        name: 'Details',
        component: Details,
        props: true
    },
    {
        path: '/profile/technologies/new/',
        name: 'CreateTech',
        component: CreateTech
    },
    {
        path: '/profile/technologies/:tech_id/items/:item_id',
        name: 'Item',
        component: Item,
        props: true
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router