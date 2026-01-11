<script setup>

</script>

<template>
  <div>
    <footer class="welcome-section">
      <div class="extra-decoration">
        <h3 class="extra-text">Información de contacto</h3>
        <p class="unique-experience">{{info_contacto}}</p>
        <hr>
      </div>
      <div class="container">
        <p class="copyright-text">Copyright &copy; 2023 All Rights Reserved by Grupo 24 </p>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from '../common/services';

export default {
  data() {
    return {
      info_contacto: {}
    };
  },
  mounted() {
    // Hacer la solicitud a la API de configuración de Flask al cargar el componente
    axios.get('/api/contact')
      .then(response => {
        this.info_contacto = response.data;
      })
      .catch(error => {
        this.info_contacto = "Llamenos 221-2211222 o al email cidepint@hotmail.com";
        console.error('Error al obtener datos de configuración desde Flask:', error);
      });
  }
};
</script>

<style>
  .welcome-section {
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    width: 100% ;
    justify-items: center   ;
    align-items: end;
  }

.extra-decoration {
  margin-top: 20px;
}

.extra-text {
  font-size: 1.5em;
  color: #4CAF50;
  text-decoration: underline;
  /* Subrayado */
}

.unique-experience {
  font-size: 1.2em;
  color: #4CAF50;
}

.copyright-text {
  color: darkgrey;
}
</style>