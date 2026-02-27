<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-blue-200 flex flex-col items-center justify-center px-4">
    <!-- Hero -->
    <h1 class="text-4xl md:text-5xl font-bold text-blue-900 mb-6 text-center">
      SummitCast
    </h1>
    <p class="text-lg text-blue-800 mb-8 text-center max-w-xl">
      Forecast your run routes from Strava and see weather predictions for every waypoint.
    </p>

    <!-- Input form -->
    <div class="w-full max-w-md bg-white rounded-xl shadow-md p-6 flex flex-col gap-4">
      <input
        v-model="stravaLink"
        type="url"
        placeholder="Paste your Strava route link"
        class="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
      />

      <button
        @click="forecastRoute"
        class="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition-colors"
      >
        Forecast Route
      </button>

      <p v-if="error" class="text-red-600 text-sm mt-2">{{ error }}</p>
    </div>

    <!-- Result / status -->
    <div v-if="status" class="mt-6 p-4 bg-blue-100 rounded-lg text-blue-900 max-w-md text-center">
      {{ status }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const stravaLink = ref('')
const status = ref('')
const error = ref('')

const forecastRoute = async () => {
  status.value = ''
  error.value = ''

  if (!stravaLink.value) {
    error.value = 'Please enter a Strava route link.'
    return
  }

  try {
    // Call your backend API (replace with real endpoint later)
    const res = await fetch('/api/strava/forecast', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: stravaLink.value }),
    })

    if (!res.ok) throw new Error('Failed to forecast route')

    const data = await res.json()
    status.value = `Route forecast ready! ETA: ${data.eta ?? 'N/A'}`
  } catch (err: any) {
    error.value = err.message
  }
}
</script>
