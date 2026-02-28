<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center px-4">
    <div class="w-full max-w-2xl bg-white shadow-lg rounded-2xl p-8">

      <h1 class="text-3xl font-bold text-gray-800 mb-6">
        SummitCast
      </h1>

      <form @submit.prevent="handleSubmit" class="flex gap-3 mb-6">
        <input
          v-model="stravaRouteUrl"
          type="text"
          placeholder="Paste Strava route URL or ID"
          class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          class="px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          Fetch
        </button>
      </form>

      <div v-if="loading" class="text-gray-500 mb-4">
        Loading route...
      </div>

      <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded-lg mb-4">
        {{ error }}
      </div>

      <div v-if="routeData" class="bg-gray-50 p-4 rounded-xl border">
        <h2 class="text-xl font-semibold mb-3">Route Info</h2>

        <p class="text-gray-700">
          <span class="font-medium">Route ID:</span>
          {{ routeData.route_id }}
        </p>

        <p v-if="routeData.distance" class="text-gray-700">
          <span class="font-medium">Distance:</span>
          {{ routeData.distance }}
        </p>

        <div v-if="routeData.waypoints" class="mt-4">
          <h3 class="font-semibold mb-2">Waypoints</h3>
          <ul class="space-y-1 text-sm text-gray-600">
            <li
              v-for="(wp, index) in routeData.waypoints"
              :key="index"
              class="bg-white px-3 py-1 rounded border"
            >
              {{ wp.lat }}, {{ wp.lng }}
            </li>
          </ul>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { fetchRoute } from '../services/api'
import RouteDetails from '../components/RouteDetails.vue'

const stravaRouteUrl = ref('')
const routeData = ref(null)
const loading = ref(false)
const error = ref(null)

const handleSubmit = async () => {
  loading.value = true
  error.value = null
  routeData.value = null

  try {
    routeData.value = await fetchRoute(stravaRouteUrl.value)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to fetch route'
  } finally {
    loading.value = false
  }
}
</script>
