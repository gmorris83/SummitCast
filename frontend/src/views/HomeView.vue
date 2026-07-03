<template>
  <main class="min-h-screen bg-slate-50 text-slate-900">
    <div class="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-6 sm:px-6 lg:px-8">
      <header class="flex flex-col gap-4 border-b border-slate-200 pb-5 sm:flex-row sm:items-center sm:justify-between">
        <div class="flex items-center gap-3">
          <img :src="logo" alt="SummitCast" class="h-14 w-14 rounded-lg bg-white object-contain p-2 shadow-sm ring-1 ring-slate-200"/>
          <div>
            <h1 class="text-2xl font-semibold text-slate-950">SummitCast</h1>
            <p class="text-sm text-slate-500">Route forecasting for exposed days out</p>
          </div>
        </div>
      </header>

      <section class="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <form @submit.prevent="handleSubmit" class="flex flex-col gap-3 md:flex-row">
          <label class="flex flex-1 flex-col gap-1 text-sm font-medium text-slate-700">
            Strava route
            <input
              v-model="stravaRouteUrl"
              type="text"
              placeholder="Paste Strava route URL or ID"
              class="h-11 rounded-lg border border-slate-300 bg-white px-3 text-slate-950 outline-none transition focus:border-sky-600 focus:ring-2 focus:ring-sky-100"
            />
          </label>
          <button
            type="submit"
            class="h-11 self-end rounded-lg bg-slate-950 px-5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
            :disabled="loading"
          >
            {{ loading ? "Fetching..." : "Fetch route" }}
          </button>
        </form>
      </section>

      <div v-if="loading" class="rounded-lg border border-slate-200 bg-white px-4 py-3 text-sm text-slate-600 shadow-sm">
        Loading route...
      </div>
      <div v-if="error" class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
        {{ error }}
      </div>

      <section v-if="routeData" class="flex flex-col gap-6">
        <div class="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div>
              <div class="flex items-center gap-3">
                <h2 class="text-xl font-semibold text-slate-950">{{ routeData.name }}</h2>
                <a
                  :href="stravaRouteUrl"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="rounded-lg border border-slate-200 bg-white p-1 transition hover:border-orange-300 hover:bg-orange-50"
                  aria-label="Open route in Strava"
                >
                  <img :src="strava_logo" alt="" class="h-7 w-7 object-contain"/>
                </a>
              </div>
              <p v-if="routeData.athlete.username" class="mt-1 text-sm text-slate-500">
                Created by {{ routeData.athlete.username }}
              </p>
            </div>

            <div class="grid grid-cols-2 gap-3 sm:grid-cols-3">
              <div class="rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
                <p class="text-xs font-medium uppercase text-slate-500">Distance</p>
                <p class="mt-1 text-lg font-semibold text-slate-950">{{ distanceKm }} km</p>
              </div>
              <div class="rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
                <p class="text-xs font-medium uppercase text-slate-500">Elevation</p>
                <p class="mt-1 text-lg font-semibold text-slate-950">{{ elevationM }} m</p>
              </div>
              <div class="rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
                <p class="text-xs font-medium uppercase text-slate-500">Waypoints</p>
                <p class="mt-1 text-lg font-semibold text-slate-950">{{ waypointCount }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
          <div class="border-b border-slate-200 px-5 py-4">
            <h3 class="text-base font-semibold text-slate-950">Route map</h3>
          </div>
          <div class="h-[560px] w-full">
            <RouteMap
              v-if="routeData.polyline"
              :polyline="routeData.polyline"
              :waypoints="routeData.waypoints"
            />
          </div>
        </div>

        <div class="rounded-lg border border-slate-200 bg-white shadow-sm">
          <div class="flex flex-col gap-4 border-b border-slate-200 px-5 py-4 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <h3 class="text-base font-semibold text-slate-950">Weather planning</h3>
              <p class="mt-1 text-sm text-slate-500">Choose a start date, hour, and average pace, then add forecast data to each waypoint.</p>
            </div>

            <div class="flex flex-wrap items-end gap-3">
              <label class="flex flex-col gap-1 text-sm font-medium text-slate-700">
                Date
                <input
                  v-model="weatherDate"
                  type="date"
                  class="h-10 rounded-lg border border-slate-300 bg-white px-3 text-slate-950 outline-none transition focus:border-sky-600 focus:ring-2 focus:ring-sky-100"
                />
              </label>

              <label class="flex flex-col gap-1 text-sm font-medium text-slate-700">
                Hour
                <select
                  v-model="weatherHour"
                  class="h-10 rounded-lg border border-slate-300 bg-white px-3 text-slate-950 outline-none transition focus:border-sky-600 focus:ring-2 focus:ring-sky-100"
                >
                  <option v-for="hour in hours" :key="hour" :value="hour">
                    {{ hour }}:00
                  </option>
                </select>
              </label>

              <label class="flex min-w-48 flex-col gap-1 text-sm font-medium text-slate-700">
                <span class="flex items-center justify-between gap-3">
                  Average pace
                  <span class="text-xs font-semibold text-slate-500">{{ formattedAveragePace }} /km</span>
                </span>
                <input
                  v-model.number="averagePaceMinPerKm"
                  type="range"
                  min="3"
                  max="20"
                  step="0.25"
                  class="h-10 accent-sky-700"
                />
              </label>

              <div class="h-10 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700">
                Finish <span class="font-semibold text-slate-950">{{ formattedEstimatedFinishTime }}</span>
              </div>

              <button
                type="button"
                :disabled="weatherLoading || isWeatherDateInPast"
                class="h-10 rounded-lg bg-sky-700 px-4 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:bg-slate-300"
                @click="handleAddWeather"
              >
                {{ weatherLoading ? "Adding..." : "Add weather" }}
              </button>
            </div>
          </div>

          <div class="px-5 py-4">
            <div v-if="isWeatherDateInPast" class="mb-4 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
              Choose a current or future date and hour to add weather.
            </div>

            <div v-if="weatherError" class="mb-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              {{ weatherError }}
            </div>

            <div v-if="hasWeather" class="overflow-x-auto rounded-lg border border-slate-200">
              <table class="min-w-full text-left text-sm">
                <thead class="bg-slate-50 text-xs uppercase text-slate-500">
                  <tr>
                    <th class="px-4 py-3 font-semibold">Waypoint</th>
                    <th class="px-4 py-3 font-semibold">ETA</th>
                    <th class="px-4 py-3 font-semibold">Weather</th>
                    <th class="px-4 py-3 font-semibold">Temp</th>
                    <th class="px-4 py-3 font-semibold">Feels like</th>
                    <th class="px-4 py-3 font-semibold">Wind</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 bg-white">
                  <tr
                    v-for="waypoint in routeData.waypoints"
                    :key="`${waypoint.title}-${waypoint.distance_into_route}`"
                    class="text-slate-700"
                  >
                    <td class="px-4 py-3 font-medium text-slate-950">{{ waypoint.title }}</td>
                    <td class="px-4 py-3">{{ formatEta(waypoint.eta) }}</td>
                    <td class="px-4 py-3">{{ waypoint.weather_summary || "-" }}</td>
                    <td class="px-4 py-3">{{ formatTemp(waypoint) }}</td>
                    <td class="px-4 py-3">{{ formatFeelsLike(waypoint.feels_like_c) }}</td>
                    <td class="px-4 py-3">{{ formatWind(waypoint.wind_speed_ms) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-else class="rounded-lg border border-dashed border-slate-300 bg-slate-50 px-4 py-8 text-center text-sm text-slate-500">
              Weather data will appear here after it is added to the route.
            </div>
          </div>
        </div>

        <ElevationProfile
          v-if="routeData.distance_profile?.length && routeData.elevation_profile?.length"
          :distance="routeData.distance_profile"
          :elevation="routeData.elevation_profile"
        />
      </section>
    </div>
  </main>
</template>

<script setup>
import {ref, computed} from "vue"
import RouteMap from "../components/RouteMap.vue"
import {addWeather, fetchRoute} from "../services/api"
import logo from '../assets/logo.png'
import strava_logo from '../assets/strava_logo.png'
import ElevationProfile from '../components/ElevationProfile.vue'

const distanceKm = computed(() => {
  if (!routeData.value) return "0.00"
  return (routeData.value.distance / 1000).toFixed(2)
})

const elevationM = computed(() => {
  if (!routeData.value) return "0"
  return Math.round(routeData.value.elevation_gain)
})

const waypointCount = computed(() => {
  return routeData.value?.waypoints?.length ?? 0
})

const stravaRouteUrl = ref("")
const routeData = ref(null)
const loading = ref(false)
const weatherLoading = ref(false)
const error = ref(null)
const weatherError = ref(null)
const dateInputValue = (date) => {
  const localDate = new Date(date.getTime() - date.getTimezoneOffset() * 60000)
  return localDate.toISOString().slice(0, 10)
}

const weatherDate = ref(dateInputValue(new Date()))
const weatherHour = ref(String(new Date().getHours()).padStart(2, "0"))
const averagePaceMinPerKm = ref(10)

const hours = Array.from({length: 24}, (_, hour) => String(hour).padStart(2, "0"))

const selectedStartTime = computed(() => {
  const localDate = new Date(`${weatherDate.value}T${weatherHour.value}:00:00`)
  return localDate.toISOString()
})

const selectedStartDate = computed(() => {
  return new Date(`${weatherDate.value}T${weatherHour.value}:00:00`)
})

const isWeatherDateInPast = computed(() => {
  const currentHour = new Date()
  currentHour.setMinutes(0, 0, 0)
  return selectedStartDate.value.getTime() < currentHour.getTime()
})

const hasWeather = computed(() => {
  return routeData.value?.waypoints?.some((waypoint) => waypoint.weather_source)
})

const estimatedFinishDate = computed(() => {
  if (!routeData.value?.distance) return null

  const distanceKm = routeData.value.distance / 1000
  return new Date(selectedStartDate.value.getTime() + distanceKm * averagePaceMinPerKm.value * 60000)
})

const formattedAveragePace = computed(() => {
  const minutes = Math.floor(averagePaceMinPerKm.value)
  const seconds = Math.round((averagePaceMinPerKm.value - minutes) * 60)
  return `${minutes}:${String(seconds).padStart(2, "0")}`
})

const formattedEstimatedFinishTime = computed(() => {
  if (!estimatedFinishDate.value) return "-"

  return estimatedFinishDate.value.toLocaleString([], {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false
  })
})

const handleSubmit = async () => {
  loading.value = true
  error.value = null
  routeData.value = null

  try {
    routeData.value = await fetchRoute(stravaRouteUrl.value)
    weatherError.value = null
  } catch (err) {
    error.value = err.response?.data?.detail || "Failed to load route"
  } finally {
    loading.value = false
  }
}

const handleAddWeather = async () => {
  if (!routeData.value) return

  weatherError.value = null
  if (isWeatherDateInPast.value) {
    weatherError.value = "Choose a current or future date and hour to add weather."
    return
  }

  weatherLoading.value = true

  try {
    routeData.value = await addWeather(routeData.value, selectedStartTime.value, averagePaceMinPerKm.value)
  } catch (err) {
    weatherError.value = err.response?.data?.detail || "Failed to add weather"
  } finally {
    weatherLoading.value = false
  }
}

const formatEta = (eta) => {
  if (!eta) return "-"
  return new Date(eta).toLocaleString([], {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false
  })
}

const formatTemp = (waypoint) => {
  if (waypoint.temperature_c !== null && waypoint.temperature_c !== undefined) {
    return `${Math.round(waypoint.temperature_c)} C`
  }

  if (waypoint.temp_min_c !== null && waypoint.temp_min_c !== undefined) {
    return `${Math.round(waypoint.temp_min_c)}-${Math.round(waypoint.temp_max_c)} C`
  }

  return "-"
}

const formatWind = (windSpeed) => {
  if (windSpeed === null || windSpeed === undefined) return "-"
  return `${Math.round(windSpeed)} m/s`
}

const formatFeelsLike = (feelsLike) => {
  if (feelsLike === null || feelsLike === undefined) return "-"
  return `${Math.round(feelsLike)} C`
}
</script>
