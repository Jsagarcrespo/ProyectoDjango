import type { Encuesta } from '../types'

const API_URL = 'http://127.0.0.1:8000/api/encuestas/'

export async function obtenerEncuestas(): Promise<Encuesta[]> {
  const respuesta = await fetch(API_URL)

  if (!respuesta.ok) {
    throw new Error('No se han podido cargar las encuestas desde Django')
  }

  return await respuesta.json()
}
