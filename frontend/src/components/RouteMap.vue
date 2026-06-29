<template>
  <div ref="mapContainer" class="h-full w-full"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from "vue"
import L from "leaflet"
import "leaflet/dist/leaflet.css"

// const props = defineProps({
//   polyline: {
//     type: Array,
//     required: true
//   }
// })

const props = defineProps({
  polyline: {
    type: Array,
    required: true
  },
  waypoints: {
    type: Array,
    default: () => []
  }
})

const mapContainer = ref(null)
let map = null
let routeLayer = null
let markerLayer = null

const formatWaypointPopup = (wp) => {
  const lines = [`<strong>${wp.title ?? "Waypoint"}</strong>`]

  if (wp.eta) {
    lines.push(`ETA: ${new Date(wp.eta).toLocaleString([], {
      day: "2-digit",
      month: "short",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false
    })}`)
  }

  if (wp.weather_summary) {
    lines.push(`Weather: ${wp.weather_summary}`)
  }

  if (wp.temperature_c !== null && wp.temperature_c !== undefined) {
    lines.push(`Temp: ${Math.round(wp.temperature_c)} C`)
  } else if (wp.temp_min_c !== null && wp.temp_min_c !== undefined) {
    lines.push(`Temp: ${Math.round(wp.temp_min_c)}-${Math.round(wp.temp_max_c)} C`)
  }

  if (wp.wind_speed_ms !== null && wp.wind_speed_ms !== undefined) {
    lines.push(`Wind: ${Math.round(wp.wind_speed_ms)} m/s`)
  }

  return lines.join("<br>")
}

const renderMap = () => {
  if (!props.polyline || props.polyline.length === 0) return

  if (!map) {
    map = L.map(mapContainer.value)

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map)
  }

  if (routeLayer) routeLayer.remove()
  if (markerLayer) markerLayer.remove()

  routeLayer = L.polyline(props.polyline, {
    color: "#0369a1",
    weight: 5,
    opacity: 0.9
  }).addTo(map)

  map.fitBounds(routeLayer.getBounds())

  markerLayer = L.layerGroup().addTo(map)
  props.waypoints.forEach((wp) => {
    if (wp.lat && wp.lon) {
      L.marker([wp.lat, wp.lon])
        .addTo(markerLayer)
        .bindPopup(formatWaypointPopup(wp))
    }
  })
}

onMounted(() => {
  renderMap()
})

watch(
  () => [props.polyline, props.waypoints],
  () => renderMap(),
  { deep: true }
)

onBeforeUnmount(() => {
  if (map) map.remove()
})
</script>
