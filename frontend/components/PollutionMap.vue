<template>
  <div class="relative h-full w-full">
    <!-- Map Container -->
    <div ref="mapContainer" class="h-full w-full rounded-2xl overflow-hidden"></div>

    <!-- Map Controls -->
    <div class="absolute top-4 right-4 z-[1000] flex flex-col space-y-2">
      <!-- Layer Toggle -->
      <div class="glass-dark rounded-xl p-2 shadow-lg">
        <button
          @click="toggleHeatmap"
          class="w-10 h-10 rounded-lg flex items-center justify-center transition-colors"
          :class="showHeatmap ? 'bg-blue-500 text-white' : 'hover:bg-gray-100'"
          :title="$t('map.showHeatmap')"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
          </svg>
        </button>
        <button
          @click="toggleMarkers"
          class="w-10 h-10 rounded-lg flex items-center justify-center transition-colors mt-1"
          :class="showMarkers ? 'bg-blue-500 text-white' : 'hover:bg-gray-100'"
          :title="$t('map.showMarkers')"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Legend -->
    <div class="absolute bottom-4 left-4 z-[1000] glass-dark rounded-xl p-4 shadow-lg">
      <h4 class="text-sm font-semibold mb-3 text-gray-700">{{ $t('map.legend') }}</h4>
      <div class="space-y-2">
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 rounded-full" style="background: #00e400"></div>
          <span class="text-xs text-gray-600">0-50 {{ $t('aqi.good') }}</span>
        </div>
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 rounded-full" style="background: #ffff00"></div>
          <span class="text-xs text-gray-600">51-100 {{ $t('aqi.moderate') }}</span>
        </div>
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 rounded-full" style="background: #ff7e00"></div>
          <span class="text-xs text-gray-600">101-150 {{ $t('aqi.unhealthySensitive') }}</span>
        </div>
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 rounded-full" style="background: #ff0000"></div>
          <span class="text-xs text-gray-600">151-200 {{ $t('aqi.unhealthy') }}</span>
        </div>
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 rounded-full" style="background: #8f3f97"></div>
          <span class="text-xs text-gray-600">201-300 {{ $t('aqi.veryUnhealthy') }}</span>
        </div>
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 rounded-full" style="background: #7e0023"></div>
          <span class="text-xs text-gray-600">300+ {{ $t('aqi.hazardous') }}</span>
        </div>
      </div>
    </div>

    <!-- Selected Sensor Info -->
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="transform translate-y-4 opacity-0"
      enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform translate-y-4 opacity-0"
    >
      <div
        v-if="selectedSensor"
        class="absolute bottom-4 right-4 z-[1000] glass-dark rounded-xl p-4 shadow-lg w-72"
      >
        <div class="flex items-start justify-between mb-3">
          <div>
            <h4 class="font-semibold text-gray-800">{{ selectedSensor.name }}</h4>
            <p class="text-xs text-gray-500">{{ selectedSensor.location_description }}</p>
          </div>
          <button @click="selectedSensor = null" class="text-gray-400 hover:text-gray-600">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div v-if="selectedSensorReading" class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-600">AQI</span>
            <span
              class="px-2 py-1 rounded-lg text-white text-sm font-bold"
              :style="{ background: getAqiColor(selectedSensorReading.aqi) }"
            >
              {{ selectedSensorReading.aqi }}
            </span>
          </div>
          <div class="grid grid-cols-2 gap-2 pt-2 border-t border-gray-100">
            <div class="text-center p-2 bg-gray-50 rounded-lg">
              <div class="text-xs text-gray-500">PM2.5</div>
              <div class="font-semibold">{{ selectedSensorReading.pm25?.toFixed(1) || '--' }}</div>
            </div>
            <div class="text-center p-2 bg-gray-50 rounded-lg">
              <div class="text-xs text-gray-500">PM10</div>
              <div class="font-semibold">{{ selectedSensorReading.pm10?.toFixed(1) || '--' }}</div>
            </div>
            <div class="text-center p-2 bg-gray-50 rounded-lg">
              <div class="text-xs text-gray-500">NO₂</div>
              <div class="font-semibold">{{ selectedSensorReading.no2?.toFixed(1) || '--' }}</div>
            </div>
            <div class="text-center p-2 bg-gray-50 rounded-lg">
              <div class="text-xs text-gray-500">{{ $t('pollutants.temperature') }}</div>
              <div class="font-semibold">{{ selectedSensorReading.temperature?.toFixed(1) || '--' }}°</div>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-4">
          <div class="spinner-small mx-auto"></div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  sensors: {
    type: Array,
    default: () => []
  },
  readings: {
    type: Array,
    default: () => []
  },
  center: {
    type: Array,
    default: () => [52.2873, 76.9674]
  },
  zoom: {
    type: Number,
    default: 12
  }
})

const emit = defineEmits(['sensorClick'])

const mapContainer = ref(null)
const showHeatmap = ref(true)
const showMarkers = ref(true)
const selectedSensor = ref(null)
const selectedSensorReading = ref(null)

let map = null
let markersLayer = null
let heatmapLayer = null
let L = null

// Get AQI color
const getAqiColor = (aqi) => {
  if (!aqi) return '#gray'
  if (aqi <= 50) return '#00e400'
  if (aqi <= 100) return '#ffff00'
  if (aqi <= 150) return '#ff7e00'
  if (aqi <= 200) return '#ff0000'
  if (aqi <= 300) return '#8f3f97'
  return '#7e0023'
}

// Calculate AQI from PM2.5
const calculateAqi = (pm25) => {
  if (!pm25) return 0
  if (pm25 <= 12.0) return Math.round((50 / 12.0) * pm25)
  if (pm25 <= 35.4) return Math.round(50 + ((100 - 50) / (35.4 - 12.1)) * (pm25 - 12.1))
  if (pm25 <= 55.4) return Math.round(100 + ((150 - 100) / (55.4 - 35.5)) * (pm25 - 35.5))
  if (pm25 <= 150.4) return Math.round(150 + ((200 - 150) / (150.4 - 55.5)) * (pm25 - 55.5))
  if (pm25 <= 250.4) return Math.round(200 + ((300 - 200) / (250.4 - 150.5)) * (pm25 - 150.5))
  return Math.round(300 + ((500 - 300) / (500.4 - 250.5)) * (pm25 - 250.5))
}

// Create custom marker
const createCustomMarker = (sensor, reading) => {
  const aqi = reading ? calculateAqi(reading.pm25) : 0
  const color = getAqiColor(aqi)

  const markerHtml = `
    <div class="custom-marker" style="
      width: 48px;
      height: 48px;
      background: ${color};
      border-radius: 50%;
      border: 3px solid white;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      color: ${aqi > 100 ? 'white' : '#333'};
      font-size: 14px;
      cursor: pointer;
      transition: transform 0.3s ease;
    ">
      ${aqi || '--'}
    </div>
  `

  return L.divIcon({
    html: markerHtml,
    className: 'custom-marker-container',
    iconSize: [48, 48],
    iconAnchor: [24, 24]
  })
}

// Initialize map
const initMap = async () => {
  if (typeof window === 'undefined' || !mapContainer.value) return

  try {
    L = (await import('leaflet')).default

    // Create map
    map = L.map(mapContainer.value, {
      zoomControl: false
    }).setView(props.center, props.zoom)

    // Add custom zoom control
    L.control.zoom({ position: 'topright' }).addTo(map)

    // Add light-style tile layer (CartoDB Positron)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(map)

    // Initialize layers
    markersLayer = L.layerGroup().addTo(map)

    // Update markers
    updateMarkers()

    // Initialize heatmap
    await initHeatmap()

  } catch (error) {
    console.error('Error initializing map:', error)
  }
}

// Initialize heatmap layer
const initHeatmap = async () => {
  if (!map || !L) return

  try {
    // Simple gradient overlay using circles instead of heat plugin
    updateHeatmap()
  } catch (error) {
    console.error('Error initializing heatmap:', error)
  }
}

// Update markers
const updateMarkers = () => {
  if (!markersLayer || !L) return

  markersLayer.clearLayers()

  if (!showMarkers.value) return

  props.sensors.forEach(sensor => {
    const reading = props.readings.find(r => r.sensor_id === sensor.sensor_id)
    const icon = createCustomMarker(sensor, reading)

    const marker = L.marker([sensor.latitude, sensor.longitude], { icon })
      .on('click', () => {
        selectedSensor.value = sensor
        selectedSensorReading.value = reading ? {
          ...reading,
          aqi: calculateAqi(reading.pm25)
        } : null
        emit('sensorClick', sensor)
      })

    markersLayer.addLayer(marker)
  })
}

// Update heatmap
const updateHeatmap = () => {
  if (!map || !L) return

  // Remove existing heatmap circles
  map.eachLayer(layer => {
    if (layer.options && layer.options.isHeatmapCircle) {
      map.removeLayer(layer)
    }
  })

  if (!showHeatmap.value) return

  // Create gradient circles for each sensor
  props.sensors.forEach(sensor => {
    const reading = props.readings.find(r => r.sensor_id === sensor.sensor_id)
    const aqi = reading ? calculateAqi(reading.pm25) : 0
    const color = getAqiColor(aqi)

    // Create gradient circle
    const circle = L.circle([sensor.latitude, sensor.longitude], {
      radius: 1500,
      fillColor: color,
      fillOpacity: 0.3,
      stroke: false,
      isHeatmapCircle: true
    }).addTo(map)
  })
}

// Toggle heatmap
const toggleHeatmap = () => {
  showHeatmap.value = !showHeatmap.value
  updateHeatmap()
}

// Toggle markers
const toggleMarkers = () => {
  showMarkers.value = !showMarkers.value
  updateMarkers()
}

// Watch for data changes
watch(() => props.sensors, updateMarkers, { deep: true })
watch(() => props.readings, () => {
  updateMarkers()
  updateHeatmap()
}, { deep: true })

onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<style>
.custom-marker-container {
  background: transparent !important;
  border: none !important;
}

.custom-marker:hover {
  transform: scale(1.1);
}

.spinner-small {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(99, 102, 241, 0.2);
  border-left-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
