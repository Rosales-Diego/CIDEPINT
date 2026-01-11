  <!-- ListRequests.vue -->
  <template>
    
    <div>
    
      <MenuBar @ver-servicios="cambiarEstado" />
      <br>
      <div class="titulo-header">
        <h2> Listado de Solicitudes </h2>
      </div>
      <br>
      
      
      <table class="table table-bordered table-styled">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Nombre del Servicio</th>
            <th scope="col"> Estado:
              <div class="filtro-container">

                <select v-model="filtroEstado" @change="filtrarPedidos" class="filtro-select">
                  <option value="">Quitar Filtro</option>
                  <option value="en_proceso">En Proceso</option>
                  <option value="aceptada">Aceptada</option>
                  <option value="finalizada">Finalizada</option>
                  <option value="rechazada">Rechazada</option>
                  <option value="cancelada">Cancelada</option>
                </select>

              </div>
            </th>
              <th scope="col">Tipo de Servicio</th>
              <th scope="col">Fecha de Alta:
                <div class="filtro-container"> 
                  <select v-model="ordenFecha" @change="ordenarPedidos" class="filtro-select" id="ordenFecha">

                    <option value="asc">Ascendente</option>
                    <option value="desc">Descendente</option>

                  </select>
                </div>
              </th>
              <th scope="col">Notas</th>
          </tr>
        </thead>
        <tbody>
          
          <tr v-for="item in pedidos" :key="item">
          
            <th scope="row">{{ item.id }}</th>
            <td scope="row">{{item.service_name}}</td>
            <td scope="row">{{item.status}}</td>
            <td scope="row">{{item.type_of_service}}</td>
            <td>{{ formatearFecha(item.inserted_at) }}</td>
            <td><button class = "nota-button" @click="redirigirAFormulario(item) ">  Agregar Nota 📝  </button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>

  <script>

  //import axios from 'axios'; // Importa Axios
  //import moment from 'moment';
  import MenuBar from '../components/MenuBar.vue';
  import { listRequestWithNameService } from '../common/user';
  import moment from 'moment';


  export default {

    components: {
      MenuBar
    },
    
    data() {
      return {
        pedidos: [],
        originales:[], // Aquí almacenaremos la lista de pedidos obtenida de la API
        filtroEstado: '', 
      };
    },
    mounted() {
      // Llama a la función para obtener la lista de pedidos cuando se monta el componente
      this.obtenerPedidos();
    },

    methods: {

      redirigirAFormulario(item) {

        console.log("Redirigiendo con estos datos: ", item)
        this.$router.push({
          name: 'responder-nota',
          params: {
            id: item.id,
            solicitud_id: item.id,
          },
        });
      },


      ordenarPedidos() {
        if (this.ordenFecha === 'asc') {
          this.pedidos.sort((a, b) => new Date(a.inserted_at) - new Date(b.inserted_at));
        } else {
          this.pedidos.sort((a, b) => new Date(b.inserted_at) - new Date(a.inserted_at));
        }
      },

      capitalizarEstado(estado) {
          switch (estado) {
            case 'aceptada':
              return 'Aceptada';
            case 'en_proceso':
              return 'En Proceso';
            case 'finalizada':
              return 'Finalizada';
            case 'cancelada':
              return 'Cancelada';
            case 'rechazada':
              return 'Rechazada';
            default:
              return estado;
          }
        },


      /*Función para cambiar el formato fecha- hora- segundos a DD/MM/YYYY */
      formatearFecha(fecha) {
        return moment(fecha).format('DD/MM/YYYY');
      },

      cambiarEstados(listaDeObjetos) {
        for (let i = 0; i < listaDeObjetos.length; i++) {
          if (listaDeObjetos[i].status) {
            listaDeObjetos[i].status = this.capitalizarEstado(listaDeObjetos[i].status);
          }
        }
      },

      async obtenerPedidos() {
        try {

          const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` };
          const response = await listRequestWithNameService.getList(headers);
          this.pedidos = response.data.data;
          this.cambiarEstados(this.pedidos);
          this.originales = this.pedidos;
          console.log("Este es el listado actual", this.pedidos)

        } catch (error) {
          console.error('Error al obtener la lista de pedidos:', error);
        }


      },

      // Nuevo método para filtrar los pedidos según el estado seleccionado
      filtrarPedidos() {
        this.pedidos = this.originales;
        if (this.filtroEstado) {
          // Filtra los pedidos directamente, sin volver a obtener la lista completa
          this.filtroEstado = this.capitalizarEstado(this.filtroEstado);
          console.log(this.filtroEstado)
          this.pedidos = this.pedidos.filter((pedido) => pedido.status === this.filtroEstado);
          console.log("filtrados: ", this.pedidos);
        }
      },


    },

  };
  </script>

<style scoped>
.container {
  text-align: center;
}

.titulo-header {
  text-align: center;
  background-color: #f2f2f2;
  padding: 20px;
  border-radius: 10px;
}

.title {
  color: black;
}

.nota-button {
  background-color: #555;
  border: 1px solid #555;
  color: white;
  padding: 5px 10px;
  cursor: pointer;
  position:relative;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.nota-button:hover {
  background-color: #777;
  /* Cambia el color al pasar el mouse */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  /* Añade un efecto de resaltado */
}

.nota-button::after {
  content: '\2192';
  /* Código de la flecha hacia la derecha */
  margin-left: 5px;
  opacity: 0;
  /* Inicialmente invisible */
  transition: opacity 0.3s ease;
}

.filtro-container {
  margin-bottom: 20px;
}

.filtro-select {
  background-color: #555;
  /* Fondo oscuro con luminosidad */
  color: white;
  height: 50px;
  border: 1px solid #886363;
}

.table-styled {
  width: 75%;
  margin: auto;
  border-collapse: collapse;
  margin-top: 20px; /* Add margin-top for separation from the title */
}

.table-styled th,
.table-styled td {
  border: 2px solid #333;
  /* Bordes oscuros */
  padding: 8px;
  color: black;
}

.table-styled th {
  background-color: #555;
  /* Fondo oscuro con luminosidad */
  color: white;
  font-weight: bold; /* Make the header text bold */
}
</style>

