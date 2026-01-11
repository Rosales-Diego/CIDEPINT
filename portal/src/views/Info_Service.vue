<template>
  <div>
    <MenuBar @ver-servicios="cambiarEstado" />

    <div class="main-container">
      <div class="article-container">
        <article>
          <h2>{{ servicioData ? servicioData.name : 'Cargando nombre del servicio...' }}</h2>
          <section id="details">
            <p class="details-description">{{ servicioData ? servicioData.description : 'Cargando detalles...' }}</p>
            <p v-if="servicioData && servicioData.authorized_centers">
              <strong>Centros autorizados:</strong> {{ servicioData.authorized_centers }}
            </p>
            <p v-if="servicioData && servicioData.search_keywords">
              <strong>Palabras clave:</strong> {{ servicioData.search_keywords }}
            </p>
          </section>
        </article>

        <article>
          <h2>Institución</h2>
          <section id="institution">
            <p class="institution-name">{{ intitucionesData ? intitucionesData.name : 'Cargando institución...' }}</p>
            <ul class="institution-details">
              <li v-if="intitucionesData && intitucionesData.address">
                <strong>Dirección:</strong> {{ intitucionesData.address }}
              </li>
              <li v-if="intitucionesData && intitucionesData.contact_info">
                <strong>Contacto:</strong> {{ intitucionesData.contact_info }}
              </li>
              <li v-if="intitucionesData && intitucionesData.key_words">
                <strong>Palabras clave:</strong> {{ intitucionesData.key_words }}
              </li>
              <li v-if="intitucionesData && intitucionesData.web">
                <strong>Sitio web:</strong> <a :href="intitucionesData.web" target="_blank">{{ intitucionesData.web }}</a>
              </li>
              <li v-if="intitucionesData && intitucionesData.work_schedule">
                <strong>Horario de trabajo:</strong> {{ intitucionesData.work_schedule }}
              </li>
            </ul>
          </section>
        </article>
      </div>

      <div class="aside-container">
        <aside class="full-width-aside">
          <button @click="solicitar" class="centered-button" style="background-color: #28a745; color: white; border-color: #28a745;">Solicitar</button>
          <SolicitudePopUp v-if="mostrarPopup" @solicitar="enviarSolicitud" @cerrar-popup="cerrarPopup" />
          <h2>¿Cómo llegar?</h2>
          <div class="map-container" ref="map"></div>
        </aside>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import L from 'leaflet';
import MenuBar from '../components/MenuBar.vue';
import SolicitudePopUp from '../components/SolicitudePopUp.vue';
import 'leaflet/dist/leaflet.css'; 
import { SolicitudePost } from '../common/solicitude';

export default {
  components: {
      MenuBar,
      SolicitudePopUp,
    },
  data() {
    return {
      servicioData: null,
      intitucionesData: null,
      mostrarPopup: false,
    };
  },
  props: ['id'],
  mounted() {
    // Realiza la solicitud HTTP cuando el componente se ha montado en el DOM
    axios.get(`/api/services?id=${this.id}`)
      .then(response => {
        // Actualiza la data del componente con la respuesta
        this.servicioData = response.data;
        console.log('id de la istitucion:', this.servicioData.institutions_id)
        return axios.get(`/api/institutions/info?id=${this.servicioData.institutions_id}`);
      })
      .then(response => {
        // Actualiza la data del componente con la respuesta
        // guado para despues
        this.intitucionesData = response.data;
        this.initMap();
      })
      .catch(error => {
        console.error('Error al realizar la solicitud:', error);
      });
  },
  methods: {
    solicitar() {
      if (!localStorage.getItem('token')) {
        alert(`Debe iniciar sesión para realizar una solicitud`);
      } else {
        this.mostrarPopup = true;
      };
      
    },
    cerrarPopup() {
      this.mostrarPopup = false;
    },

    enviarSolicitud(comentario) {
      // Aquí puedes realizar la lógica para enviar la solicitud con el comentario
      if (localStorage.getItem('token')) {
        const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` };
        const data = { comment: `${comentario}`,
                    type_of_service: `${this.servicioData.type_of_service.split('.').pop()}`,
                    service_id: `${this.id}`
                    };
        SolicitudePost.postSolicitude(data, headers);
        alert(`Solicitud realizada con comentario: ${comentario}`);
      } else {
        alert(`Debe iniciar sesión para realizar una solicitud`);
      };
      this.cerrarPopup();
    },
    initMap() {
      const institucionDeseada = this.intitucionesData;
      
      if (institucionDeseada && institucionDeseada.location) {
        // Obtén las coordenadas de la ubicación
        const [lat, lng] = institucionDeseada.location.split(',');
        
        // Crea un nuevo mapa centrado en las coordenadas proporcionadas
        const map = L.map(this.$refs.map).setView([parseFloat(lat), parseFloat(lng)], 15);

        // Agrega una capa de mosaico de OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors',
        }).addTo(map);

        // Agrega un marcador en la ubicación
        L.marker([parseFloat(lat), parseFloat(lng)]).addTo(map)
          .bindPopup(institucionDeseada.address)
          .openPopup();
      } else {
        console.error('La ubicación de la institución no está disponible.');
      }
    },
  }
}

</script>

<style scoped>

body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  color: black; /* Cambiar el color del texto a negro */
  background-color: white; /* Cambiar el color de fondo a blanco */
}

/* Otras reglas de estilo para los elementos restantes */


.main-container {
  display: flex;
}

.anticle-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  flex-grow: 2;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  color: white; /* Cambiado a blanco */
}

article {
  padding: 20px;
  margin: 10px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
  color: black; /* Cambiar el color del texto a negro */
}

h2 {
  color: #333;
}

section {
  margin-top: 10px;
}

aside {
  width: 250px;
  height: 513px;
  padding: 20px;
  margin: 10px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
  color: black; /* Cambiar el color del texto a negro */
}

button {
  margin-bottom: 10px;
  padding: 12px 20px; /* Ajusta el tamaño según sea necesario */
  width: 100%; /* Ocupa todo el ancho disponible */
  text-align: center;
  border: 1px solid #333; /* Borde del botón */
  background-color: #ddd; /* Color de fondo del botón */
  border-radius: 10px; /* Añadir esta línea para redondear los bordes */
}

.centered-button {
  margin: auto;
}

.map-container {
  /* Estilos para el contenedor del mapa o imagen */
  /* Puedes ajustar según sea necesario */
  height: 400px;
  border: 1px solid #ddd;
  margin-top: 10px;
}

.main-container {
  display: flex;
  justify-content: space-around;
  margin: 20px;
}

.article-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

article {
  padding: 20px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
}

h2 {
  color: #333;
}

.details-description {
  margin-bottom: 10px;
}

.institution-name {
  font-size: 1.5em;
  font-weight: bold;
  margin-bottom: 10px;
}

.institution-details {
  list-style-type: none;
  padding: 0;
}

.institution-details li {
  margin-bottom: 10px;
}

/* Estilos para el contenedor del mapa o imagen */
.map-container {
  height: 385px;
  border: 1px solid #ddd;
  margin-top: 10px;
}
</style>
