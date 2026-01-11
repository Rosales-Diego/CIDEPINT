<template>
    <div>
      <h2 class="title-notes">Responder Nota</h2>

      <!-- Muestra la nota que se está respondiendo -->
      <div>
        <strong class="title-notes">Nota: {{ nota }}</strong> 
      </div>

      <!-- Mostrar las notas -->
      <div v-for="notaItem in notas" :key="notaItem.id" :class="{ 'note-container-right': notaItem.user_id === usuarioActual, 'note-container-left': notaItem.user_id !== usuarioActual }">
        <div v-if="notaItem.user_id === usuarioActual" > 
          <p>Enviado por: Tú , a las {{  notaItem.insert_at }}</p>
        </div>
        <div v-else>
          <p>Enviado por: Proveedor, a las {{  notaItem.insert_at }}</p>
        </div> 
        <div> 
          <p>{{ notaItem.content }}</p>
        </div>
        
      </div>
  
      <!-- Casilla para insertar el mensaje de respuesta -->
      <textarea v-model="mensajeRespuesta" placeholder="Escribe tu respuesta aquí"></textarea>
  
      <!-- Botones "Volver" y "Enviar Respuesta" -->
      <div>
        <button class="note-button" @click="volver">Volver</button>
        <button class="note-button" @click="enviarRespuesta">Enviar Respuesta</button>
      </div>
    </div>
  </template>
  
  <script>

//AXIOS para consultar las API s
import { listNotesForService } from '../common/user';
import {commentNote} from '../common/user';
import {UserServices} from '../common/user';
import {UserNote} from '../common/user';

  export default {
    props: {
        idNota: {
            type: Number,
            required: true,
        },
        notaOriginal: {
            type: String,
            required: true,
        },
    },
    data() {
      return {
        mensajeRespuesta: '', // Almacena la respuesta del usuario
        solicitud_id: '', // Inicializa la propiedad notaOriginal
        id: '',
        notas:[],
        usuarioActual: '', // Simplemente como ejemplo, debes establecer el ID del usuario actual
      };
    },
    mounted() {
      // Aquí deberías hacer una solicitud para obtener la información de la nota según el ID
      // Por ahora, utilizo datos de ejemplo
      this.obtenerInformacionNota();
      this.obtenerIdUsuarioDesdeToken();
      
    },
    methods: {

      async obtenerIdUsuarioDesdeToken() {
        const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` };
        const response = await UserNote.getProfile(headers);
        this.usuarioActual = response.data.id
      },

      async obtenerInformacionNota() {
        try {

          const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` };
          const params = { id: this.$route.params.id, solicitud_id :this.$route.params.solicitud_id}
          this.id = this.$route.params.id
          this.solicitud_id =this.$route.params.solicitud_id

          const response = await listNotesForService.getList(params, headers);
          
          this.notas = response.data.data;
          
          console.log("Este es el listado actual", this.notas)

        } catch (error) {
          console.error('Error al obtener la lista de notas:', error);
        }


      },
      
      volver() {
        // Puedes redirigir al usuario de nuevo a la página anterior o a donde prefieras
        this.$router.go(-1);
      },

      enviarRespuesta() {
      // Verifica si el mensaje de respuesta no está vacío antes de enviarlo
      if (!this.mensajeRespuesta.trim()) {
        console.log('El mensaje de respuesta no puede estar vacío.');
        return;
      }
      else{
        const body = {
          comment: this.mensajeRespuesta,
        };
        const params = {
          id : this.id
        }
        const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` };
        console.log(body , params , headers);
        commentNote.send(body, params, headers);
        
        this.$router.push('/ListRequest');
      }

      
    },
    },
  };
  </script>
  
  <style>
  /* Agrega estilos según sea necesario */
  .title-notes{
    color:black;
  }

  .textarea {
    width: 100%;
    height: 100px;
    margin-bottom: 10px;
  }

    .note-button {
    margin-right: 10px; /* Ajusta el margen entre los botones según tus preferencias */
    background-color: black; /* Fondo blanco por defecto */
    color: white; /* Cambia el color de texto a negro por defecto */
    border: none;
    padding: 10px 15px;
    cursor: pointer;
    transition: background-color 0.3s ease; /* Agrega una transición suave para el cambio de color */
  }

  .note-button:hover {
    background-color: #3498db; /* Cambia el fondo al color azul al pasar el cursor sobre el botón */
    color: white; /* Cambia el color de texto a blanco al pasar el cursor sobre el botón */
  }

  .note-container-right {
  text-align: right;
  background-color: #e6e6e6; /* Color de fondo para el lado derecho */
}

.note-container-left {
  text-align: left;
  background-color: #f2f2f2; /* Color de fondo para el lado izquierdo */
}

  </style>
  