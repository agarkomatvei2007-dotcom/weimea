<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-100 sticky top-0 z-50">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <NuxtLink to="/" class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-white text-xl shadow-lg">
              🌍
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-800">{{ $t('app.name') }}</h1>
              <p class="text-xs text-gray-500">{{ $t('dashboard.title') }}</p>
            </div>
          </NuxtLink>

          <div class="flex items-center space-x-4">
            <div class="text-sm text-gray-500">
              {{ $t('dashboard.lastUpdate') }}: {{ lastUpdate }}
            </div>
            <LanguageSwitcher />
            <button
              @click="refreshData"
              class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-xl font-medium transition-colors flex items-center space-x-2"
            >
              <svg class="w-4 h-4" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>{{ $t('dashboard.refresh') }}</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-6">
      <!-- Loading -->
      <div v-if="loading && !currentAQI" class="flex justify-center items-center min-h-[60vh]">
        <div class="spinner"></div>
      </div>

      <div v-else>
        <!-- Current AQI Card -->
        <div class="bg-white rounded-3xl p-6 mb-6 shadow-lg shadow-gray-100/50 border border-gray-100">
          <div class="flex flex-col lg:flex-row items-center justify-between gap-6">
            <div class="flex items-center space-x-6">
              <div
                class="w-32 h-32 rounded-full flex flex-col items-center justify-center text-white shadow-2xl transition-transform hover:scale-105"
                :style="{ background: currentAQI?.color || '#gray' }"
              >
                <div class="text-5xl font-bold">{{ currentAQI?.aqi || '--' }}</div>
                <div class="text-sm opacity-80">AQI</div>
              </div>
              <div>
                <div class="text-sm text-gray-500">{{ $t('dashboard.aqi') }}</div>
                <div class="text-4xl font-bold text-gray-900 mb-1">{{ currentAQI?.category || $t('common.loading') }}</div>
                <div class="text-sm text-gray-500">{{ currentAQI?.dominant_pollutant || '' }}</div>
              </div>
            </div>
            <div class="bg-gray-50 rounded-2xl p-5 max-w-md">
              <div class="text-sm font-semibold text-gray-700 mb-2">{{ $t('dashboard.healthRecommendation') }}</div>
              <p class="text-sm text-gray-600">{{ currentAQI?.health_message || $t('common.loading') }}</p>
            </div>
          </div>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div class="bg-white rounded-2xl p-5 shadow-lg shadow-gray-100/50 border border-gray-100 hover:-translate-y-1 transition-transform">
            <div class="flex items-center justify-between mb-3">
              <span class="text-2xl">💨</span>
              <span class="text-xs text-gray-400">µg/m³</span>
            </div>
            <div class="text-sm text-gray-500 mb-1">{{ $t('pollutants.pm25') }}</div>
            <div class="text-3xl font-bold text-gray-900">{{ latestData?.pm25?.toFixed(1) || '--' }}</div>
          </div>

          <div class="bg-white rounded-2xl p-5 shadow-lg shadow-gray-100/50 border border-gray-100 hover:-translate-y-1 transition-transform">
            <div class="flex items-center justify-between mb-3">
              <span class="text-2xl">🌫️</span>
              <span class="text-xs text-gray-400">µg/m³</span>
            </div>
            <div class="text-sm text-gray-500 mb-1">{{ $t('pollutants.pm10') }}</div>
            <div class="text-3xl font-bold text-gray-900">{{ latestData?.pm10?.toFixed(1) || '--' }}</div>
          </div>

          <div class="bg-white rounded-2xl p-5 shadow-lg shadow-gray-100/50 border border-gray-100 hover:-translate-y-1 transition-transform">
            <div class="flex items-center justify-between mb-3">
              <span class="text-2xl">⚗️</span>
              <span class="text-xs text-gray-400">µg/m³</span>
            </div>
            <div class="text-sm text-gray-500 mb-1">{{ $t('pollutants.no2') }}</div>
            <div class="text-3xl font-bold text-gray-900">{{ latestData?.no2?.toFixed(1) || '--' }}</div>
          </div>

          <div class="bg-white rounded-2xl p-5 shadow-lg shadow-gray-100/50 border border-gray-100 hover:-translate-y-1 transition-transform">
            <div class="flex items-center justify-between mb-3">
              <span class="text-2xl">🌡️</span>
              <span class="text-xs text-gray-400">°C</span>
            </div>
            <div class="text-sm text-gray-500 mb-1">{{ $t('pollutants.temperature') }}</div>
            <div class="text-3xl font-bold text-gray-900">{{ latestData?.temperature?.toFixed(1) || '--' }}</div>
          </div>
        </div>

        <!-- Map and Chart Row -->
        <div class="grid lg:grid-cols-2 gap-6 mb-6">
          <!-- Interactive Map -->
          <div class="bg-white rounded-3xl p-6 shadow-lg shadow-gray-100/50 border border-gray-100">
            <h3 class="text-xl font-bold text-gray-900 mb-4">{{ $t('dashboard.sensorNetwork') }}</h3>
            <div class="h-[450px] rounded-2xl overflow-hidden">
              <PollutionMap
                :sensors="sensors"
                :readings="readings"
                :center="[52.2873, 76.9674]"
                :zoom="12"
              />
            </div>
          </div>

          <!-- Trends Chart -->
          <div class="bg-white rounded-3xl p-6 shadow-lg shadow-gray-100/50 border border-gray-100">
            <h3 class="text-xl font-bold text-gray-900 mb-4">{{ $t('dashboard.trends') }}</h3>
            <div class="h-[450px]">
              <canvas ref="chartCanvas"></canvas>
            </div>
          </div>
        </div>

        <!-- AI Insights -->
        <div v-if="insights" class="bg-white rounded-3xl p-6 mb-6 shadow-lg shadow-gray-100/50 border border-gray-100">
          <div class="flex items-center space-x-3 mb-4">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-xl">
              🤖
            </div>
            <h3 class="text-xl font-bold text-gray-900">{{ $t('dashboard.aiInsights') }}</h3>
          </div>
          <div class="bg-gray-50 rounded-2xl p-5">
            <p class="text-gray-700 leading-relaxed whitespace-pre-line">{{ insights }}</p>
          </div>
        </div>

        <!-- Active Alerts -->
        <div v-if="activeAlerts.length > 0" class="bg-white rounded-3xl p-6 shadow-lg shadow-gray-100/50 border border-gray-100">
          <div class="flex items-center space-x-3 mb-4">
            <span class="text-xl">🚨</span>
            <h3 class="text-xl font-bold text-gray-900">{{ $t('dashboard.activeAlerts') }}</h3>
            <span class="px-2 py-1 bg-red-100 text-red-600 text-xs font-semibold rounded-full">
              {{ activeAlerts.length }}
            </span>
          </div>
          <div class="space-y-3">
            <div
              v-for="alert in activeAlerts"
              :key="alert.id"
              class="bg-red-50 border border-red-100 rounded-2xl p-4 flex items-start space-x-3"
            >
              <div class="w-10 h-10 bg-red-100 rounded-xl flex items-center justify-center text-xl">
                ⚠️
              </div>
              <div class="flex-1">
                <div class="font-semibold text-red-700">{{ $t(`alerts.${alert.severity}`) }}</div>
                <p class="text-sm text-gray-700 mt-1">{{ alert.message }}</p>
                <div class="text-xs text-gray-500 mt-2">{{ formatTime(alert.timestamp) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- AI Chat -->
    <AiChat />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const { t, locale } = useI18n()
const config = useRuntimeConfig()

const loading = ref(true)
const lastUpdate = ref('')
const currentAQI = ref(null)
const latestData = ref(null)
const sensors = ref([])
const readings = ref([])
const activeAlerts = ref([])
const insights = ref('')
const chartCanvas = ref(null)

let chart = null
let refreshInterval = null

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleString(locale.value)
}

const fetchDashboardData = async () => {
  try {
    // Fetch all data in parallel
    const [aqiRes, readingsRes, sensorsRes, alertsRes] = await Promise.all([
      fetch(`${config.public.analyticsApiUrl}/aqi/current`).catch(() => null),
      fetch(`${config.public.iotApiUrl}/readings/recent?limit=50`).catch(() => null),
      fetch(`${config.public.iotApiUrl}/sensors`).catch(() => null),
      fetch(`${config.public.alertApiUrl}/alerts/active`).catch(() => null)
    ])

    if (aqiRes) {
      const aqiData = await aqiRes.json()
      currentAQI.value = aqiData
    }

    if (readingsRes) {
      const readingsData = await readingsRes.json()
      readings.value = readingsData.readings || []
      if (readings.value.length > 0) {
        latestData.value = readings.value[0]
      }
    }

    if (sensorsRes) {
      const sensorsData = await sensorsRes.json()
      sensors.value = sensorsData.sensors || []
    }

    if (alertsRes) {
      const alertsData = await alertsRes.json()
      activeAlerts.value = alertsData.alerts || []
    }

    // Fetch insights
    try {
      const insightsRes = await fetch(`${config.public.analyticsApiUrl}/insights`)
      const insightsData = await insightsRes.json()
      insights.value = insightsData.insights || ''
    } catch (e) {
      console.log('Insights not available')
    }

    lastUpdate.value = new Date().toLocaleTimeString(locale.value)
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
}

const initChart = async () => {
  if (!chartCanvas.value || typeof window === 'undefined') return

  try {
    const Chart = (await import('chart.js/auto')).default

    const statsRes = await fetch(`${config.public.analyticsApiUrl}/statistics/hourly?hours=24`)
    const statsData = await statsRes.json()

    if (chart) {
      chart.destroy()
    }

    chart = new Chart(chartCanvas.value, {
      type: 'line',
      data: {
        labels: statsData.statistics?.map(s => {
          const date = new Date(s.timestamp)
          return date.toLocaleTimeString(locale.value, { hour: '2-digit', minute: '2-digit' })
        }) || [],
        datasets: [
          {
            label: t('pollutants.pm25'),
            data: statsData.statistics?.map(s => s.pm25?.avg) || [],
            borderColor: 'rgb(99, 102, 241)',
            backgroundColor: 'rgba(99, 102, 241, 0.1)',
            fill: true,
            tension: 0.4,
            borderWidth: 2
          },
          {
            label: t('pollutants.pm10'),
            data: statsData.statistics?.map(s => s.pm10) || [],
            borderColor: 'rgb(168, 85, 247)',
            backgroundColor: 'rgba(168, 85, 247, 0.1)',
            fill: true,
            tension: 0.4,
            borderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              usePointStyle: true,
              padding: 20
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.05)'
            },
            title: {
              display: true,
              text: 'µg/m³'
            }
          },
          x: {
            grid: {
              display: false
            }
          }
        },
        interaction: {
          intersect: false,
          mode: 'index'
        }
      }
    })
  } catch (error) {
    console.error('Error initializing chart:', error)
  }
}

const refreshData = async () => {
  loading.value = true
  await fetchDashboardData()
  await initChart()
  loading.value = false
}

onMounted(async () => {
  loading.value = true
  await fetchDashboardData()
  await initChart()
  loading.value = false

  refreshInterval = setInterval(fetchDashboardData, 30000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  if (chart) {
    chart.destroy()
  }
})
</script>
