<template>
  <div class="w-full h-[500px] rounded-xl overflow-hidden border">
    <LMap
      :zoom="13"
      :center="center"
      style="height:100%; width:100%"
    >
      <LTileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="© OpenStreetMap"
      />

      <LPolyline :lat-lngs="polyline" />
    </LMap>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { LMap, LTileLayer, LPolyline } from "@vue-leaflet/vue-leaflet"
import "leaflet/dist/leaflet.css"
import L from "leaflet"

import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png"
import markerIcon from "leaflet/dist/images/marker-icon.png"
import markerShadow from "leaflet/dist/images/marker-shadow.png"

delete L.Icon.Default.prototype._getIconUrl

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

const props = defineProps({
  polyline: {
    type: Array,
    required: true
  }
})

const center = computed(() => {
  return props.polyline?.[0] ?? [51.505, -0.09]
})

console.log(props.polyline);
</script>
