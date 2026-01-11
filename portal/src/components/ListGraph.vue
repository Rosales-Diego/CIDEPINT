<template>
  <div>
    <MenuBar @ver-servicios="cambiarEstado" />
    <br>
    <div class="titulo-header">
      <h2> Listado de Solicitudes </h2>
    </div>
    <br>

    <div class="headGraph">
      <h2>📊 Graficos 📈</h2>
    </div>
    <div>
      <div>
        <button class="graph-button" @click="mostrar(0)">Ver grafico 1</button>
        <div v-if="flagg_graph[0]">
          <GraficoBar />
        </div>
      </div>

      <div>
        <button class="graph-button" @click="mostrar(1)">Ver grafico 2</button>
        <div v-if="flagg_graph[1]">
          <RankingGraph />
        </div>
      </div>

      <div>
        <button class="graph-button" @click="mostrar(2)">Ver grafico 3</button>
        <div v-if="flagg_graph[2]">
          <TopFinished />
        </div>
      </div>
    </div>

  </div>
</template>

  
<script>
import axios from 'axios';

import GraficoBar from './GraficoBar.vue';
import RankingGraph from './RankingGraph.vue';
import TopFinished from './TopFinised.vue';
import MenuBar from './MenuBar.vue';
export default {
  components: {
    GraficoBar,
    RankingGraph,
    TopFinished,
    MenuBar,
  },
  data() {
    return {
      chartData: null,
      flagg_graph: [false, false, false],
      loaded_graph: [false, false, false],
    };
  },

  methods: {
    mostrar(numero_grafico) {
      this.flagg_graph[numero_grafico] = !this.flagg_graph[numero_grafico];
    },
  },
}
</script>
  
<style scoped>
.headGraph {
  background-color: #f2f2f2;
  padding: 20px;
  text-align: center;
  border-radius: 10px;
}

.graph-button {
  width: 100%;
  height: 50px;
  background-color: #e0e0e0;
  color: black;
  border: none;
  border-radius: 10px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.graph-button:hover {
  background-color: #d0d0d0;
}

</style>
