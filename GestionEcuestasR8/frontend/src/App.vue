<script setup lang="ts">
import { onMounted, ref } from "vue";
import type { Encuesta } from "./types";
import { obtenerEncuestas } from "./services/encuestasService";

const encuestas = ref<Encuesta[]>([]);
const cargando = ref(true);
const error = ref("");

onMounted(async () => {
  try {
    encuestas.value = await obtenerEncuestas();
  } catch (e) {
    error.value = "Error al conectar con la API de Django";
  } finally {
    cargando.value = false;
  }
});
</script>

<template>
  <main class="contenedor">
    <section class="cabecera">
      <h1>Frontend Vue - Encuestas Reto 8</h1>
      <p>Esta pantalla está hecha con Vue y consume datos JSON desde Django.</p>
    </section>

    <section v-if="cargando" class="aviso">Cargando encuestas...</section>

    <section v-else-if="error" class="error">
      {{ error }}
    </section>

    <section v-else>
      <p class="contador">
        Total de encuestas recibidas desde Django: {{ encuestas.length }}
      </p>

      <article v-for="encuesta in encuestas" :key="encuesta.id" class="tarjeta">
        <div class="tarjeta-cabecera">
          <h2>{{ encuesta.titulo }}</h2>

          <span class="estado" :class="encuesta.estado">
            {{ encuesta.estado }}
          </span>
        </div>

        <p>{{ encuesta.descripcion }}</p>

        <p>
          <strong>Fecha cierre:</strong>
          {{ encuesta.fecha_cierre ?? "Sin fecha de cierre" }}
        </p>
      </article>
    </section>
  </main>
</template>

<style scoped>
.contenedor {
  max-width: 950px;
  margin: 0 auto;
  padding: 2rem;
  font-family: Arial, sans-serif;
}

.cabecera {
  background: #eef6ff;
  border: 1px solid #c9e2ff;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

h1 {
  margin: 0 0 0.5rem 0;
  color: #1f3b57;
}

.contador {
  margin-bottom: 1rem;
  font-weight: bold;
}

.tarjeta {
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1rem;
  background: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.tarjeta-cabecera {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
}

.tarjeta h2 {
  margin: 0;
  color: #243447;
}

.estado {
  padding: 0.3rem 0.7rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: bold;
  text-transform: uppercase;
}

.abierta {
  background: #d1f7d6;
  color: #166534;
}

.cerrada {
  background: #ffd6d6;
  color: #991b1b;
}

.borrador {
  background: #fff3c4;
  color: #92400e;
}

.aviso {
  padding: 1rem;
  background: #fff3c4;
  border-radius: 8px;
}

.error {
  padding: 1rem;
  background: #ffd6d6;
  color: #991b1b;
  border-radius: 8px;
}
</style>
