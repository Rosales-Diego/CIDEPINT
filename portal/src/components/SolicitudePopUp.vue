<template>
  <div class="popup-container">
    <div class="popup">
      <form @submit.prevent="solicitar">
        <label for="comentario">Agregue un comentario:</label>
        <textarea v-model="comentario" id="comentario" required></textarea>
        <div class="buttons-container">
          <button type="submit" class="submit-button">Solicitar</button>
          <button @click="cancelar" class="cancel-button">Cancelar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      comentario: '',
    };
  },
  methods: {
    solicitar() {
      this.$emit('solicitar', this.comentario);
    },
    cancelar() {
      this.$emit('cerrar-popup');
    },
  },
};
</script>

<style scoped>
.popup-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup {
  background-color: #45723b57;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  border: 1px solid #cccccc00;
  border-radius: 5px;
}

form {
  width: 300px;
  max-width: 100%;
}

label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
}

textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.buttons-container {
  display: flex;
  justify-content: space-between;
}

.submit-button,
.cancel-button {
  padding: 10px 15px;
  cursor: pointer;
  border: none;
  border-radius: 3px;
}

.submit-button {
  background-color: #4caf50;
  color: #fff;
}

.cancel-button {
  background-color: #ccc;
  color: #000;
}
</style>
