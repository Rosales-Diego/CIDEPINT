<template>
    <div>
      <MenuBar @ver-servicios="cambiarEstado" />
      <div class="login-container">
        
        <div class="login-form">
          <h2 style="color: black;">Login</h2>
          <form @submit.prevent="login">
            <label>Email:</label>
            <input type="email" v-model="email" required />

            <button type="submit">Login</button>
            <p v-if="error" class="error-message">{{ error }}</p>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import MenuBar from '../components/MenuBar.vue';
  
  export default {
    components: {
        MenuBar
    },
    data() {
      return {
        email: '',
        password: '123',
        error: '', // Nuevo estado para almacenar el mensaje de error
      };
    },
    methods: {
      async login() {
        try {
          const response = await axios.post('/api/auth/', {
            email: this.email,
            password: this.password,
          });
          const token = response.data.token;
          // Guardar el token en el almacenamiento local (localStorage)
          localStorage.setItem('token', token);
  
          // Redirigir al perfil del usuario /
          this.$router.push('/');
        } catch (error) {
          console.error('Error during login:', error);
  
          // Mostrar mensaje de error
          this.error = 'Email';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }
  
  .logo {
    width: 600px; /* Ajusta el tamaño según tus necesidades */
    margin-bottom: 20px;
    flex: auto;
  }
  
  .login-form {
    width: 300px;
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  h2 {
    font-size: 24px;
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 8px;
    color: darkcyan;
  }
  
  input {
    width: 100%;
    padding: 8px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background-color: #3498db;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #2980b9;
  }
  
  .error-message {
    color: red;
    margin-top: 10px;
  }
  
  .login-with-google {
    margin-top: 20px;
  }
  </style>
  
  
    