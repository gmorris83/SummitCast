<template>
<div class="max-w-md mx-auto bg-white shadow-lg rounded-2xl p-6 border border-gray-200">
<h2 class="text-2xl font-bold text-gray-900 mb-2">
{{ route.name }}
</h2>

<p class="text-sm text-gray-500 mb-4">
by {{ route.author }}
</p>

<div class="space-y-2 text-gray-700">
<div class="flex justify-between">
<span class="font-medium">Distance</span>
<span>{{ formattedDistance }}</span>
</div>

<div class="flex justify-between">
<span class="font-medium">Estimated Time</span>
<span>{{ formattedTime }}</span>
</div>
</div>
</div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    route: {
               type: Object,
               required: true,
           // expected:
// {
   //   name: String,
//   author: String,
//   distance: Number (in meters),
//   estimatedTime: Number (in seconds)
// }
}
})

const formattedDistance = computed(() => {
if (!props.route.distance) return '-'
const km = props.route.distance / 1000
return `${km.toFixed(1)} km`
})

const formattedTime = computed(() => {
if (!props.route.estimatedTime) return '-'

const totalMinutes = Math.floor(props.route.estimatedTime / 60)
const hours = Math.floor(totalMinutes / 60)
const minutes = totalMinutes % 60

if (hours > 0) {
return `${hours}h ${minutes}m`
}

return `${minutes} min`
})
</script>