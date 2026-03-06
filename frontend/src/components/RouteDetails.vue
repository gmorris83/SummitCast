<template>
  <div>
    <h2>Route</h2>

    <p><strong>{{ route.name }}</strong></p>
    <p><strong>Created By:</strong> {{ route.athlete.username }}</p>
    <p><strong>Distance:</strong> {{ route.distance }}</p>
    <p><strong>Elevation:</strong> {{ route.elevation_gain }}</p>
    <p><strong>Estimated Finish Time:</strong> {{ route.estimated_moving_time }}</p>

    <div v-if="route.waypoints">
      <h3>Waypoints</h3>
      <ul>
        <li v-for="(wp, index) in route.waypoints" :key="index">
          {{ wp.lat }}, {{ wp.lng }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
defineProps({
  route: Object
})
</script>
