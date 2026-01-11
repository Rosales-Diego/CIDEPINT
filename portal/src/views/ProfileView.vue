<template>
  <div>
    <MenuBar @ver-servicios="cambiarEstado" />
    <div v-if="user" class="profile-view">
      <h1 style="color: black;">Bienvenido a Cidepint</h1>
      <div class="user-info">
        <div class="info-item">
          <label>Nombre:</label>
          <p>{{ user.name }}</p>
        </div>
        <div class="info-item">
          <label>Apellido:</label>
          <p>{{ user.last_name }}</p>
        </div>
        <div class="info-item">
          <label>Correo electrónico:</label>
          <p>{{ user.email }}</p>
        </div>
        <div class="info-item">
          <label>Activo:</label>
          <p>{{ user.active }}</p>
        </div>
        <div class="info-item">
          <label>Fecha de registro:</label>
          <p>{{ user.inserted_at }}</p>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import MenuBar from '../components/MenuBar.vue';
import { UserServices } from '../common/user';
import { ref } from 'vue';
export default {
  components: {
    MenuBar
  },
  data() {
    return {
      user: ref(false),
    };
  },
  mounted() {
    try {
      const data = this.makeRequestWithJWT();
      this.user = data;
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  },
  methods: {
    updateUser(data) {
      this.user = data;
    },
    makeRequestWithJWT() {
      const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` };
      return UserServices.getProfile(this.updateUser, headers);
    },
  },
};
</script>

<style scoped>
.profile-view {
  background-color: #369f5c;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin: 20px auto;
  max-width: 600px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.info-item {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
}

p {
  margin: 0;
}
</style>

