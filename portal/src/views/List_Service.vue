<template>
  <div>
    <MenuBar @ver-servicios="cambiarEstado" />
    <div>
      <h1>Lista de servicios</h1>

      <div class="separator"></div>

      <!-- Agregar campo de búsqueda -->
      <nav class="nav-container">
        <label for="searchInput" style="color: black;">Buscar servicio por nombre: </label>
        <input type="text" id="searchInput" v-model="filtroname" @keyup.enter="aplicarFiltros"  style="color: black;"/>
        <button @click="volverAtras">Volver al Listado</button>
      </nav>
      
      <div class="separator"></div>

      <!-- Verificar si hay servicios disponibles -->
      <div class="main-container">
        <aside style="background-color: #38a138; padding: 10px;">
            <h2>Filtros</h2>
            <div class="filtros-container" >
              <form @submit.prevent="aplicarFiltros">
                <div class="filter-item">
                  <label for="institucion">Institución:</label>
                  <select v-model="filtroInstitucion">
                    <option value="">Todas</option>
                    <option v-for="institucion in listInstitutions" :key="institucion.id" :value="institucion.id">{{ institucion.name }}</option>
                  </select>
                </div>

                <div class="filter-item">
                  <label for="palabrasClaves">Palabras Claves:</label>
                  <input type="text" v-model="filtroPalabrasClaves">
                </div>

                <div class="filter-item">
                  <label for="tipoServicio">Tipo de Servicio:</label>
                  <select v-model="filtroTipoServicio">
                    <option value="">Todos</option>
                    <option v-for="(value, key) in Tipo_de_Servicios" :key="key" :value="value">{{ key }}</option>
                  </select>
                </div>

                <button type="submit">Aplicar Filtros</button>
              </form>  
            </div>
        </aside>

        <div class="separator"></div>

        <div v-if="ListServices && ListServices.data && ListServices.data.length > 0">
          <!-- Contenedor general de servicios -->
          <div class="services-container">
            <!-- Iterar sobre la lista de servicios -->
            <article v-for="service in ListServices.data" :key="service.name" class="service-item">
              <div class="service-info">
                <div>
                  <h2>{{ service.name }}</h2>
                  <!-- Truncar la descripción a 100 caracteres -->
                  <p>{{ truncateDescription(service.description) }}</p>
                  <!-- Mostrar el nombre de la institución -->
                  <p>Instituciones: {{ service.institution_name }}</p>
                  <p>Keywords: {{ service.search_keywords }}</p>
                </div>

                <!-- Botón "Ver más" con estilo condicional y texto dinámico -->
                <button @click="verMas(service)" :style="{ background: service.enabled ? 'green' : 'red' }">
                  {{ service.enabled ? 'Ver más' : 'No disponible' }}
                </button>
              </div>
              <hr>
            </article>
          </div>

          <!-- Controles de paginación -->
          <div>
            <button @click="cargarPagina(ListServices.page - 1)" :disabled="ListServices.page === 1">Anterior</button>
            <span>Página {{ ListServices.page }} de {{ Math.ceil(ListServices.total / ListServices.per_page) }}</span>
            <button @click="cargarPagina(ListServices.page + 1)" :disabled="ListServices.page === Math.ceil(ListServices.total / ListServices.per_page)">Siguiente</button>
          </div>
        </div>

        <!-- Mostrar mensaje si no hay servicios -->
        <div v-else>
          <p style="color: black;">No hay servicios disponibles.</p>
        </div>
      </div>
    </div>
  </div>
</template>

  
<script>
  import axios from 'axios';
  import MenuBar from '../components/MenuBar.vue';
  import router from '@/router';  
  export default {
    components: {
      MenuBar
    },
    data() {
      return {
        ListServices: null,
        page: 1,
        per_page: 5,
        listInstitutions: null,
        filtroInstitucion: '',
        filtroPalabrasClaves: '',
        filtroTipoServicio: '',
        filtroname:'',
        Tipo_de_Servicios: '',

      };
    },
    mounted() {
      this.listInst();
      this.cargarTiposServicio(); 
      this.cargarPagina(this.page);
    },
    methods: {
      aplicarFiltros() {
        this.cargarPagina(this.page);
      },
      cargarTiposServicio(){
        /** Asignar la lista de tipos de servicio a la propiedad Tipo_de_Servicios */
        axios.get(`/api/services-types`)
        .then(response => {
          this.Tipo_de_Servicios = response.data.data.reduce((obj, item) => {
            obj[item] = item;
            return obj;
          }, {});
        })
        .catch(error => {
          console.error('Error al obtener tipos de servicio:', error);
        });      
      },
      cargarPagina(pagina) {
        /** Funcion que me permite mostra las cantidad de 
         * servios que cunmplen con los params enviados en la consulta a la API y 
         * permite manajar el tema de la paguinacion*/
        const params = {
          page: pagina,
          per_page: this.per_page,
          institution: this.filtroInstitucion,
          q: this.filtroPalabrasClaves,
          type: this.filtroTipoServicio,
          name:this.filtroname,
        };
        axios.get(`/api/services/search`,{params})
        /** Traigo una lista de los sercivios  */
          .then(response => {
            this.per_page =response.data.per_page;
            this.ListServices = response.data;
            console.log(this.ListServices.data)
          })
          .catch(error => {
            console.error('Error al obtener servicios:', error);
          });
      },
      listInst(){
        /** Traigo una lista de instittuciones */
        axios.get(`/api/institutions/List`)
          .then(response => {
            this.listInstitutions = response.data;
          })
          .catch(error => {
            console.error('Error al obtener servicios:', error);
          });
      },
      verMas(service) {
        /**  Lógica para manejar la acción "Ver más" de un servicio específico */
        if (service.enabled) {
          /**  Mostrar mensaje de confirmación si el servicio está habilitado */
          router.push({ name: 'servicio', params: {id: service.id} });
        } else {
          /**  Mostrar mensaje de servicio no disponible si el servicio no está habilitado */
          alert('Servicio no disponible');
        }
      },
      truncateDescription(description) {
        /** Función para truncar la descripción a 100 caracteres */
        return description.length > 100 ? description.slice(0, 100) + '...' : description;
      },
      volverAtras() {
        window.location.reload();
      },
    }
  }
  </script>
  
<style scoped>
  .service-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
    color: black; 
  }

  .service-info button {
    cursor: pointer;
    padding: 5px 10px;
    border: none;
    color: #fff;
    font-weight: bold;
  }

  .services-container {
    width: 30%;
    display: flex;
    flex-wrap: wrap;
    gap: 20px; 
  }

  .service-item {
    flex: 0 0 calc(33.33% - 20px); 
    box-sizing: border-box;
  }

  .main-container {
    display: flex;
    justify-content: space-between;
  }

  aside {
    width: 40%; 
  }

  .services-container {
    width: 100%; 
  }

  .filter-form {
  display: flex;
  flex-direction: column;
}

.filter-item {
  margin-bottom: 10px; 
}


.filtros-container {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

button {
  margin-top: 10px; 
}

.main-container {
  color: black;
}

.filtros-container {
  color: black;
}

.filter-item label {
  color: black;
}

.filter-item input,
.filter-item select {
  color: black;
}

button {
  color: black;
}

.separator {
  width: 1px;
  height: 100%;
  background-color: #ccc;
  margin: 0 20px; 
}

.nav-container {
    background-color: lightblue;
    padding: 10px; 
  }


  .nav-container {
    display: flex;
    align-items: center;
    background-color: #ffffff;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }

  .nav-container label {
    margin-right: 10px;
    color: black;
  }

  .nav-container input {
    flex: 1;
    padding: 5px;
    border: 1px solid #ddd;
    border-radius: 5px;
    color: black;
  }

  .nav-container button {
    padding: 5px 10px;
    border: none;
    background-color: #38a138;
    color: white;
    cursor: pointer;
  }
</style>
  
