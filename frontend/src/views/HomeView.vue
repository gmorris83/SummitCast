<template>
  <div class="min-h-screen flex flex-col items-center justify-start px-4">
    <div class="w-full max-w-2xl bg-white shadow-lg rounded-2xl p-8 flex flex-col">


      <h1 class="text-2xl font-bold mb-4">
        <img :src="logo" alt="Logo" class="mx-auto h-50 mb-1"/>
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
          Fetch Route
        </button>
      </form>

      <div v-if="loading" class="text-gray-500 mb-4">Loading route...</div>
      <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded-lg mb-4">
        {{ error }}
      </div>

      <div v-if="routeData" class="flex flex-col gap-4">
        <h2 class="text-xl font-semibold">Route Info</h2>
        <p class="text-gray-700 flex items-center gap-2">
          <span class="font-medium">{{ routeData.name }}</span>
          <a
            :href="stravaRouteUrl"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img :src="strava_logo"
                 alt="Open in Strava"
                 class="w-10 hover:scale-105 transition"/>
          </a>

        </p>
        <p v-if="routeData.athlete.username">
          <span class="font-medium">Created By:</span> {{ routeData.athlete.username }}
        </p>
        <p v-if="routeData.distance">
          <span class="font-medium">Distance:</span> {{ distanceKm }} km
        </p>

        <p v-if="routeData.elevation_gain">
          <span class="font-medium">Elevation:</span> {{ elevationM }} m
        </p>

        <!-- Map container with fixed height -->
        <div class="w-full h-[500px] mt-4">
          <RouteMap v-if="routeData.polyline"
                    :polyline="routeData.polyline"
                    :waypoints="routeData.waypoints"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed} from "vue"
import RouteMap from "../components/RouteMap.vue"
import {fetchRoute} from "../services/api"
import logo from '../assets/logo.png'
import strava_logo from '../assets/strava_logo.png'

const distanceKm = computed(() => {
  if (!routeData.value) return "0.00"
  return (routeData.value.distance / 1000).toFixed(2)
})

const elevationM = computed(() => {
  if (!routeData.value) return "0"
  return Math.round(routeData.value.elevation_gain)
})

const stravaRouteUrl = ref("")
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
    error.value = err.response?.data?.detail || "Failed to load route"
  } finally {
    loading.value = false
  }
}
</script>
