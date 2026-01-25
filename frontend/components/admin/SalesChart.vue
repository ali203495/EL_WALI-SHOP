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
const { translateLanguage, locale } = useLanguage()

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
    labels: last7Days.map(d => new Date(d).toLocaleDateString(locale.value === 'ar' ? 'ar-EG' : (locale.value === 'fr' ? 'fr-FR' : 'en-US'), { month: 'short', day: 'numeric' })),
    datasets: [
      {
        label: `${translateLanguage('admin.sales')} (${translateLanguage('common.currency')})`,
        backgroundColor: (context: any) => {
          const chart = context.chart;
          const {ctx, chartArea} = chart;
          if (!chartArea) return 'rgba(16, 185, 129, 0.1)';
          const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
          gradient.addColorStop(0, 'rgba(16, 185, 129, 0.01)');
          gradient.addColorStop(1, 'rgba(16, 185, 129, 0.15)');
          return gradient;
        },
        borderColor: '#10b981',
        borderWidth: 3,
        pointBackgroundColor: '#10b981',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        fill: true,
        data: last7Days.map(d => salesByDate[d] || 0),
        tension: 0.45
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
        label: (context: any) => ` ${(context.parsed.y || 0).toLocaleString()} ${translateLanguage('common.currency')}`
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
