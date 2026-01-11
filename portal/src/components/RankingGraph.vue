<template>
    <div class="container">
      <div class="graph-header">
      <h2>📈 Ranking de la Solicitudes 📊</h2>
      </div>
        <h2></h2>
      <Bar v-if="loaded" :data="chartData" />
    </div>
</template> 
  
  <script>
  import axios, { AxiosHeaders } from 'axios';
  
  
  import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'
import { listRequest } from '../common/user';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)
  export default {
    name: 'RankingBar',
    components: { Bar },
    data: () => ({
      loaded: false,
      chartData: null
    }),
    async mounted () {
      this.loaded = false
  
      try {

        const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` };
        
        const response = await listRequest.getList(headers);
  
        //const userlist = response.data.data;
        //const response = await axios.get(`http://127.0.0.1:5000/api/me/requests/list`);

        const userlist = response.data.data;

        // Crear un objeto para almacenar la cuenta de servicios por tipo
        const serviceCounts = {};

        // Contar la cantidad de cada tipo de servicio
        userlist.forEach(item => {
            const typeOfService = item.type_of_service;
            serviceCounts[typeOfService] = (serviceCounts[typeOfService] || 0) + 1;
        });

        // Obtener un array de nombres de servicio ordenado por la cantidad de solicitudes
        const serviceNames = Object.keys(serviceCounts).sort((a, b) => serviceCounts[b] - serviceCounts[a]);

        // Obtener un array de colores para los servicios (puedes personalizar los colores según tus preferencias)
        const serviceColors = ['blue', 'yellow', 'lightblue'];

        // Crear datasets para el gráfico
        this.chartData = {
                datasets : [
                    {
                    label: 'Ranking de Servicios',
                    fontColor: 'black',
                    backgroundColor: serviceColors,
                    borderColor: serviceColors,
                    borderWidth: 1,
                    data: serviceCounts,
                }
            ],
        }
        this.chartdata = userlist

  
        this.loaded = true
      } catch (e) {
        console.error(e)
      }
    }
  }  
  </script>

  <style>
h2{
    color:black;
  }
  .container {
  text-align: center;
}

  .graph-header {
  background-color: #f2f2f2;
  padding: 20px;
  border-radius: 10px;
}

.graph-box{
    position: relative;
    width: 100%;
    padding: 5%; /* Añadir un espacio alrededor del gráfico */
    
  }

  .container {
  width: 70%;
  margin: 0 auto; /* Centrar el contenedor */
}
  </style>