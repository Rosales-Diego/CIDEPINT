<script>
import MenuBar from '../components/MenuBar.vue'
import AboutView from './AboutView.vue'
import ConfetiView from '../components/ConfetiView.vue';
import ListRequest from './ListRequest.vue';
import ListGraph from '../components/ListGraph.vue';
import Contacto from '../components/Contacto.vue';

export default{
    components : {
        MenuBar,
        AboutView,
        ConfetiView,
        ListRequest,
        ListGraph,
        Contacto,
    },
    methods :{
        handleVerPedidosServicios() {
            this.showRequestService = !this.showRequestService;
        },
        handleVerGraph(){
            this.showGraph = !this.showGraph;
        }
    },
    data() {
        return {
        showRequestService: false,
        showGraph: false,
        };
    },
}



</script>

<template>

    <div>

        <!--MenuBar esta esperando que el evento ver-servicios(se presiona un botón)
        Cuando llega el evento, MostrarListServices se pone en True-->
        <MenuBar @verGraficos="handleVerGraph" @ver-servicios="cambiarEstado" @verPedidosServicios="handleVerPedidosServicios" />
        <br>

        <ListRequest v-if="showRequestService" />

        <ListGraph v-if="showGraph" />

        <AboutView />
        <br>
            <ConfetiView />
        <br>
        <div>
            <Contacto />
        </div>

    </div>

  
</template>

<style scoped>
.titulo {
  color: black; /* Puedes ajustar el color según tus preferencias */
}
</style>
