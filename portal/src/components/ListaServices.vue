<script>
import axios from "axios";
export default {
  data: () => ({
    result: null,
  }),
  created() {
    axios.get("http://127.0.0.1:5000/api/services/list").then((result) => {
      this.result = result.data.data;
    });
    axios.get("http://127.0.0.1:5000/api/services/list").then((result) => {
      console.log(result.data.data);
    });
  },
};
</script>

<template>
  <div>
    <div>
      <label for="">Buscar por: </label>
      <input type="text" name="" id="">
      <router-link class="btn btn-success" v-bind:to="'/services/'">Buscar</router-link>
    </div>
     <ul> 
       <li v-for="item in result">
         <h2>Servicio: {{ item.name }}</h2> 
         <p>Descripcion: {{ item.description }}</p>
        <router-link class="btn btn-success" v-bind:to="'/services/'+item.id">Detalle</router-link>
       </li>
     </ul> 
  </div> 
</template>