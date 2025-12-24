<script setup lang="ts">
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line } from 'vue-chartjs'
import { computed } from 'vue'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps<{
  orders: any[]
}>()

const chartData = computed(() => {
  // Group orders by date (last 7 days)
  const last7Days: string[] = [...Array(7)].map((_, i) => {
    const d = new Date()
    d.setDate(d.getDate() - (6 - i))
    return d.toISOString().split('T')[0] as string
  })

  // Initialize data map
  const salesByDate: Record<string, number> = {}
  last7Days.forEach(date => salesByDate[date] = 0)

  // Aggregate
  if (props.orders) {
    props.orders.forEach((order: any) => {
        const d = new Date(order.created_at || Date.now())
        const dateStr = d.toISOString().split('T')[0] as string
        // Ensure dateStr is a valid key in our range or just accumulate
        if (Object.prototype.hasOwnProperty.call(salesByDate, dateStr)) {
            salesByDate[dateStr] += order.total_amount || 0
        }
    })
  }

  return {
    labels: last7Days.map(d => new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
    datasets: [
      {
        label: 'Sales (AED)',
        backgroundColor: 'rgba(79, 70, 229, 0.2)',
        borderColor: '#4f46e5',
        borderWidth: 2,
        pointBackgroundColor: '#4f46e5',
        fill: true,
        data: last7Days.map(d => salesByDate[d] || 0),
        tension: 0.4
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: (context: any) => ` ${context.parsed.y.toLocaleString()} AED`
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(0, 0, 0, 0.05)'
      }
    },
    x: {
      grid: {
        display: false
      }
    }
  }
}
</script>

<template>
  <div class="chart-wrapper">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<style scoped>
.chart-wrapper {
  height: 300px;
  width: 100%;
}
</style>
