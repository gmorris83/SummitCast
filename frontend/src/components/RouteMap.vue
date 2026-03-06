<template>
  <div ref="mapContainer" class="w-full h-[500px] rounded border"></div>
</template>

<script setup>
import { ref, onMounted } from "vue"
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

onMounted(() => {
  if (!props.polyline || props.polyline.length === 0) return

  const map = L.map(mapContainer.value)

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors"
  }).addTo(map)

  const route = L.polyline(props.polyline, {
    color: "blue",
    weight: 4
  }).addTo(map)

  map.fitBounds(route.getBounds())

  // Add waypoint markers
  props.waypoints.forEach((wp) => {
    if (wp.lat && wp.lon) {
      L.marker([wp.lat, wp.lon])
        .addTo(map)
        .bindPopup(wp.title ?? "Waypoint")
    }
  })
})
</script>
