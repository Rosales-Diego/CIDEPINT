<template>
  <div class="container">
    <div class="graph-header">
      <h2>📈 Estados de las Solicitudes 📊</h2>
    </div>
    <div class="graph-box">
      <Pie v-if="loaded" :data="chartData" />
    </div>
  </div>
</template>

<script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'vue-chartjs';
import { listRequest } from '../common/user';

ChartJS.register(ArcElement, Tooltip, Legend);

import axios from 'axios';

export default {
  name: 'GraficoBar',
  components: { Pie },

  data() {
    return {
      loaded: false,
      chartData: null,
      userlist: [],
    };
  },
  async mounted() {
    this.loaded = false;

    try {
      const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` };
      const response = await listRequest.getList(headers);
      const userlist = response.data.data;

      this.chartData = {
        labels: ['Aceptada', 'Rechazada', 'En proceso', 'Finalizada', 'Cancelada'],
        datasets: [
          {
            label: 'Cantidad de Solicitudes',
            fontColor: 'black',
            backgroundColor: ['green', 'red', 'lightblue', 'blue', 'yellow'],
            borderColor: ['green', 'red', 'lightblue', 'blue', 'yellow'],
            borderWidth: 1,
            data: [
              userlist.filter((item) => item.status === 'aceptada').length,
              userlist.filter((item) => item.status === 'rechazada').length,
              userlist.filter((item) => item.status === 'en_proceso').length,
              userlist.filter((item) => item.status === 'finalizada').length,
              userlist.filter((item) => item.status === 'cancelada').length,
            ],
          },
        ],
      };

      this.loaded = true;
    } catch (e) {
      console.error(e);
    }
  },
};
</script>

<style scoped>
.container {
  text-align: center;
}

.graph-header {
  background-color: #f2f2f2;
  padding: 20px;
  border-radius: 10px;
}

h2 {
  color: black;
  margin: 0;
}

.graph-box{
    position: relative;
    width: 100%;
    padding: 5%; /* Añadir un espacio alrededor del gráfico */
    
  }

  .container {
  width: 60%;
  margin: 0 auto; /* Centrar el contenedor */
}
</style>
