<template>
    <div class="container">
      <div class="graph-header">
      <h2>📈 Mejores tiempos de resolución 📊</h2>
      </div>
      <div class="graph-box">
        <Line v-if="loaded" :data="chartData" />
      </div>   
    </div>
  </template>
  
  <script>
  import { finishedRequest } from '../common/user';
  import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)


  export default {
    name: 'TopFinished',
    components: { Line },
    data: () => ({
      loaded: false,
      chartData: null
    }),
    async mounted() {
      this.loaded = false
  
      try {
        const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` };
        
        const response = await finishedRequest.getFinished(headers);
  
        const userlist = response.data.data;
        console.log(userlist);
  
        // Utilizar un objeto para realizar un seguimiento de los mejores tiempos por institución
        const bestTimesByInstitution = {};

        userlist.forEach(item => {
          const institutionName = item.institution_name;
          const time = new Date(item.updated_at) - new Date(item.inserted_at);

          if (!(institutionName in bestTimesByInstitution) || time < bestTimesByInstitution[institutionName]) {
              bestTimesByInstitution[institutionName] = time;
            }
        });

            // Convertir el objeto a un array de objetos
          const sortedData = Object.keys(bestTimesByInstitution).map(institutionName => ({
            institution_name: institutionName,
            best_time: bestTimesByInstitution[institutionName],
          }));

          // Ordenar por el mejor tiempo
          sortedData.sort((a, b) => a.best_time - b.best_time);

          // Obtener las 10 instituciones con el mejor tiempo de resolución
          const top10Institutions = sortedData.slice(0, 10);
          
          // Convertir el tiempo a días
          const top10TimesInDays = top10Institutions.map(item => ({
            institution_name: item.institution_name,
            best_time: item.best_time / (1000 * 60 * 60 * 24), // Convertir de milisegundos a días
          }));
            
        console.log("Este es el ARRAy", top10Institutions);
  



        this.chartData = {
          labels: sortedData.map(item => item.institution_name),
          datasets: [
            {
              label: 'Tiempo de Resolución (días)',
              backgroundColor: 'blue',
              borderColor: 'blue',
              borderWidth: 1,
              data: top10TimesInDays.map(item => item.best_time),
            },
          ],
        };
  
        console.log(this.chartData.data)
        this.loaded = true;
      } catch (e) {
        console.error(e);
      }
    },
  };
  </script>
  
  <style>
  h2 {
    color: black;
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
  