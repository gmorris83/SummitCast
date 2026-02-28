<template>
  <div>
    <h2>Route Info</h2>

    <p><strong>ID:</strong> {{ route.route_id }}</p>
    <p><strong>Distance:</strong> {{ route.distance }}</p>

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
