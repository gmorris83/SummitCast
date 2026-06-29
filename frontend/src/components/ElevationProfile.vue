<script setup>
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale
)

const props = defineProps({
  elevation: Array,
  distance: Array
})

const data = {
  labels: props.distance,
  datasets: [
    {
      label: 'Elevation (m)',
      data: props.elevation,
      tension: 0.3,
      pointRadius: 0
    }
  ]
}

const options = {
  responsive: true,
  plugins: {
    legend: { display: false }
  },
  scales: {
    x: {
      title: { display: true, text: 'Distance (km)' }
    },
    y: {
      title: { display: true, text: 'Elevation (m)' }
    }
  }
}
</script>

<template>
  <div class="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
    <h2 class="mb-4 text-base font-semibold text-slate-950">
      Elevation Profile
    </h2>

    <Line :data="data" :options="options"/>
  </div>
</template>
