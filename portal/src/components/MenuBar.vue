<!-- MenuBar.vue -->
<!-- respaldo -->
<template>
  <nav class="navbar">
     <div class="logo-container"> 
        <img src ="../assets/public/logo_todo.jpg" alt="Logo" class="logo"  />
        
      </div>
    
      <div class="menu-bar">
        <!-- Logo -->   
      
        <!-- Botones de Registro y Login -->

        <button class="bar-button" @click="inicio">Inicio</button>


        <button class="bar-button" @click="listadeServicios"> Servicios</button>
        
        <div v-if="!token_user" class="auth-buttons">
          <button class="bar-button" @click="registrar">Registrar</button>
   
          <button class="bar-button" @click="iniciarSesion">Iniciar Sesión</button>
        </div>
    
        <!-- Menú desplegable -->
      
        <div>
          <div class="dropdown" v-if="token_user">
            <button class="bar-button" @click="toggleDropdown">Menú</button>
            <div v-if="showDropdown" class="dropdown-content">
              <ul style="list-style: none;">
                <li><button class="bar-button" @click="perfil">Perfil</button></li>
                <li><button class="bar-button" @click="cerrarSesion">Cerrar Sesión</button></li>
                <li><button class="bar-button" @click="mostrarGrafico">Ver Gráficos 📈  </button></li>
                <li> <div class="dropdown">
                    <button class="bar-button" @click="toggleDropdownService">Opciones de Servicios</button>
                    <div v-if="showDropdownService" class="dropdown-content">
                      <ul style="list-style: none;">
                        <li>
                          <button class="bar-button" @click="verPedidosServicios">Ver Mis Pedidos</button>     
                        </li>
                      </ul>
                    </div>
                  </div> 
                </li> 
              </ul>
            </div>
          </div> 
        </div>  
          
    </div>
  </nav> 
</template>

<script > 
  export default {
    components: {
    
  },
    data() {
      return {
        showDropdown: false,
        showDropdownService: false,
        mostrarListServices: false,
        showRequestService: false,
        token_user: false,
      };
    }, 
    mounted() {
      this.verificarToken();
    },
    methods: {
      inicio(){
        this.$router.push('/')
      },

    registrar() {
      // Lógica de registro
      window.location.href='http://127.0.0.1:5000/auth/register_google'
    },
    iniciarSesion() {
        // Lógica de inicio de sesión
        this.$router.push('/login'); 
      },
      toggleDropdown() {
        this.showDropdown = !this.showDropdown;
      },
      toggleDropdownService() {
        this.showDropdownService = !this.showDropdownService;
      },
      cerrarSesion() {
        localStorage.removeItem('token');
        if (this.$route.path === '/') {
         // Si la ruta actual es '/', recarga la página
          location.reload();
        } else {
          // Si la ruta actual no es '/', redirige a la página principal
        this.$router.push('/');
        }
      },
      perfil() {
        this.currentView = false
        this.$router.push('/profile'); 
      },
      mostrarGrafico(){
        // Redirigue a la Lisat de Servicios
        this.$router.push('/ShowStatics'); 
      },
      listadeServicios(){
        // Redirigue a la Lisat de Servicios
        this.$router.push('/ListaDeServicios');
      },
      verPedidosServicios() {
        // Cambia el estado para mostrar ListServices
        this.$router.push('/ListRequest');
      },
      verificarToken() {
        // Verifica si existe el token en el localStorage
        const token = localStorage.getItem('token');
        if (token) {
          // Token encontrado, el usuario está autenticado
          this.token_user = true;
        } else {
          // Token no encontrado, el usuario no está autenticado
          this.token_user = false;
        }
      },
    },
  };
</script>  
  
  
<style scoped>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background-color: white; /* Cambia esto al color que desees para tu barra de navegación */
  }

  .logo-container {
    margin-right: 10px; /* Puedes ajustar el margen según tus preferencias */
  }

  .logo {
    max-width: 100%;
    height: auto;
  }

  .menu-bar {
    display: flex;
    align-items: center;
  }

  .bar-button {
    margin-right: 10px; /* Ajusta el margen entre los botones según tus preferencias */
    background-color: white; /* Fondo blanco por defecto */
    color: black; /* Cambia el color de texto a negro por defecto */
    border: none;
    padding: 10px 15px;
    cursor: pointer;
    transition: background-color 0.3s ease; /* Agrega una transición suave para el cambio de color */
  }

.menu-button:hover {
  background-color: #3498db; /* Cambia el fondo al color azul al pasar el cursor sobre el botón */
  color: #fff;  /* Letras blancas */
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);  /* Sombra suave al pasar el ratón */
  list-style: none;
}

  
.dropdown {
    position: relative;
    display: inline-block;
    list-style: none;
}


.dropdown-content {
    display:block;
    position: center;
    min-width: 160px;
    box-shadow: 0 8px 16px 0 rgba(246, 244, 244, 0.2);
    z-index: 1;
    list-style: none;   
  }
  
  .dropdown-item {
    color: rgb(237, 232, 232);
    padding: 12px 16px;
    text-decoration: none;
    display: block;
  }
  
  .dropdown-item:hover {
    background-color: #f7efef;
  }

  .bar-button:hover {
  background-color: #3498db; /* Cambia el fondo al color azul al pasar el cursor sobre el botón */
  color: #fff;  /* Letras blancas */
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);  /* Sombra suave al pasar el ratón */
  list-style: none;
  }

    .auth-buttons {
    display: flex;
    align-items: center; /* Centra verticalmente los botones si son de diferentes alturas */
  }

  .auth-buttons .bar-button {
    margin-right: 10px; /* Ajusta el margen entre los botones según tus preferencias */
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
