import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Servicio from '../views/Info_Service.vue'
import RespondNote from '../components/RespondNote.vue'
import List_Service from '../views/List_Service.vue'
import ListRequest from '../views/ListRequest.vue';
import LoguiGoogle from '../views/LoginGoogle.vue';
import ShowStatics from '../components/ListGraph.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/about',
            name: 'about',
            component: () => import('../views/AboutView.vue')
        },
        {
            path: '/servicio/:id',
            name: 'servicio',
            component :Servicio,
            props: true
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/LoginView.vue')
        },
        {
            path: '/ListaDeServicios',
            name: 'ListaDeServicios',
            component :List_Service
        },
        {
            path: '/profile',
            name: 'profile',
            component :() => import('../views/ProfileView.vue')
        },
        {
            path: '/responder-nota/:id/:solicitud_id',  // Ruta dinámica para pasar el ID del pedido
            name: 'responder-nota',
            component: RespondNote,
            props: true,  // Permite pasar props desde la ruta
        },
        {
            path:'/ListRequest',
            name:'ListRequest',
            component:ListRequest
        },
        {
            path:'/LoginGoogle',
            name:'LoginGoogle',
            component:LoguiGoogle
        },
        {
            path:'/ShowStatics',
            name:'ShowStatics',
            component:ShowStatics
        },
        ]
})

export default router
