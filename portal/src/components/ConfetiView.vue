<script setup>
import JSConfetti from 'js-confetti'

const confetti = new JSConfetti()

function showConfetti() {
  confetti.addConfetti()
}

showConfetti()
</script>

<template>
<div>
   <h1 @click="showConfetti">🎉 Bienvenido!</h1>
   
</div>
</template>

<style>
h1 {
  text-align: center;
  cursor: pointer;
  margin-top: 3em;
  color: #4CAF50;
}
</style>