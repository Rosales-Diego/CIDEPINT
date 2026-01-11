<template>
  <div>
    <div class="dropdown">
      <button class="bar-button" @click="toggleDropdown">Menú</button>

      <div v-if="showDropdown" class="dropdown-content">
        <ul style="list-style: none;">
          <li><button class="menu-button" @click="perfil">perfil</button></li>
          <li><button class="menu-button" @click="cerrarSesion">Cerrar Sesión</button></li>
        </ul>
      </div>
    </div>  
  </div>
</template>

<script>
export default {
  data() {
    return {
      showDropdown: false,
    };
  },
  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    perfil() {
      // Lógica de inicio de sesión
    },
    cerrarSesion() {
      localStorage.removeItem('token');
      this.$router.push('/');
    },
  },
};
</script>

<style scoped>
.bar-button {
  background-color: white;  /* Fondo blanco */
  color: #000;  /* Letras negras */
  padding: 5px 10px; /* Aumenta el padding para hacer el botón más grande */
  cursor: pointer;
  list-style: none;
  transition: background-color 0.3s, color 0.3s;  /* Transición suave al cambiar colores */
  font-size: 1.2em; /* Ajusta el tamaño de la fuente para que sea más grande */
}

.bar-button:hover {
  background-color: #3498db; /* Cambia el fondo al color azul al pasar el cursor sobre el botón */
  color: white; /* Cambia el color de texto a blanco al pasar el cursor sobre el botón */
}

.menu-button {
  background-color: white;  /* Fondo negro */
  color: #000;  /* Letras blancas */
  padding: 8px 12px;
  margin: 0 5px;
  cursor: pointer;
  list-style: none;
  transition: background-color 0.3s, color 0.3s;  /* Transición suave al cambiar colores */
}

.menu-button:hover {
  background-color: #3498db; /* Cambia el fondo al color azul al pasar el cursor sobre el botón */
  color: white; /* Cambia el color de texto a blanco al pasar el cursor sobre el botón */
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);  /* Sombra suave al pasar el ratón */
}
</style>
