<template>
  <div class="min-h-screen bg-white">
    <!-- Animated Background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-96 h-96 bg-blue-100 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob"></div>
      <div class="absolute top-40 right-10 w-96 h-96 bg-purple-100 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob animation-delay-2000"></div>
      <div class="absolute -bottom-8 left-1/2 w-96 h-96 bg-pink-100 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob animation-delay-4000"></div>
    </div>

    <!-- Header -->
    <header class="relative z-50 bg-white/80 backdrop-blur-lg border-b border-gray-100 sticky top-0">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <NuxtLink to="/" class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-white text-xl shadow-lg">
              🌍
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-800">{{ $t('app.name') }}</h1>
              <p class="text-xs text-gray-500">{{ $t('app.city') }}</p>
            </div>
          </NuxtLink>

          <div class="flex items-center space-x-4">
            <LanguageSwitcher />
            <NuxtLink to="/login" class="text-gray-600 hover:text-gray-900 transition font-medium">
              {{ $t('nav.signin') }}
            </NuxtLink>
            <NuxtLink
              to="/dashboard"
              class="px-6 py-2.5 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/30 hover:-translate-y-0.5 transition-all duration-300"
            >
              {{ $t('nav.getStarted') }} →
            </NuxtLink>
          </div>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="relative z-10 pt-20 pb-32">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto text-center">
          <div class="inline-flex items-center space-x-2 px-4 py-2 bg-blue-50 rounded-full text-blue-600 text-sm font-medium mb-8">
            <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            <span>{{ $t('stats.realtime') }}</span>
          </div>

          <h1 class="text-5xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">
            {{ $t('hero.title') }}
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600 block mt-2">
              {{ $t('hero.titleHighlight') }}
            </span>
          </h1>

          <p class="text-xl text-gray-600 mb-12 max-w-2xl mx-auto leading-relaxed">
            {{ $t('hero.subtitle') }}
          </p>

          <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
            <NuxtLink
              to="/dashboard"
              class="px-8 py-4 bg-gray-900 text-white rounded-2xl font-semibold text-lg hover:bg-gray-800 hover:-translate-y-1 transition-all duration-300 shadow-xl shadow-gray-900/20"
            >
              {{ $t('hero.startTrial') }} →
            </NuxtLink>
            <button
              @click="scrollToDemo"
              class="px-8 py-4 bg-white border-2 border-gray-200 rounded-2xl font-semibold text-lg hover:border-gray-300 hover:bg-gray-50 transition-all duration-300"
            >
              {{ $t('hero.viewDemo') }}
            </button>
          </div>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20 max-w-4xl mx-auto">
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-lg shadow-gray-100/50 hover:-translate-y-1 transition-transform duration-300">
            <div class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600 mb-2">24/7</div>
            <div class="text-sm text-gray-600">{{ $t('stats.realtime') }}</div>
          </div>
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-lg shadow-gray-100/50 hover:-translate-y-1 transition-transform duration-300">
            <div class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600 mb-2">{{ sensorsCount }}+</div>
            <div class="text-sm text-gray-600">{{ $t('stats.sensors') }}</div>
          </div>
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-lg shadow-gray-100/50 hover:-translate-y-1 transition-transform duration-300">
            <div class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600 mb-2">AI</div>
            <div class="text-sm text-gray-600">{{ $t('stats.aiPowered') }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="relative z-10 py-24 bg-gray-50">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">{{ $t('features.title') }}</h2>
          <p class="text-xl text-gray-600">{{ $t('features.subtitle') }}</p>
        </div>

        <div class="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div class="bg-white rounded-3xl p-8 border border-gray-100 shadow-lg hover:-translate-y-2 transition-all duration-500">
            <div class="w-14 h-14 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center text-2xl mb-6 shadow-lg">
              🎯
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">{{ $t('features.hyperlocal.title') }}</h3>
            <p class="text-gray-600 leading-relaxed">{{ $t('features.hyperlocal.description') }}</p>
          </div>

          <div class="bg-white rounded-3xl p-8 border border-gray-100 shadow-lg hover:-translate-y-2 transition-all duration-500">
            <div class="w-14 h-14 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-2xl flex items-center justify-center text-2xl mb-6 shadow-lg">
              🤖
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">{{ $t('features.ai.title') }}</h3>
            <p class="text-gray-600 leading-relaxed">{{ $t('features.ai.description') }}</p>
          </div>

          <div class="bg-white rounded-3xl p-8 border border-gray-100 shadow-lg hover:-translate-y-2 transition-all duration-500">
            <div class="w-14 h-14 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center text-2xl mb-6 shadow-lg">
              🚨
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">{{ $t('features.alerts.title') }}</h3>
            <p class="text-gray-600 leading-relaxed">{{ $t('features.alerts.description') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Live Dashboard Preview -->
    <section id="demo" class="relative z-10 py-24">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">{{ $t('dashboard.title') }}</h2>
          <p class="text-xl text-gray-600">Pavlodar, Kazakhstan</p>
        </div>

        <div class="bg-white rounded-3xl p-8 border border-gray-100 shadow-2xl shadow-gray-200/50 max-w-5xl mx-auto">
          <!-- Loading -->
          <div v-if="loading" class="flex justify-center py-16">
            <div class="spinner"></div>
          </div>

          <!-- AQI Display -->
          <div v-else-if="currentAQI" class="text-center mb-8">
            <div class="inline-flex items-center space-x-6">
              <div
                class="w-28 h-28 rounded-full flex flex-col items-center justify-center text-white shadow-2xl"
                :style="{ background: currentAQI.color }"
              >
                <div class="text-4xl font-bold">{{ currentAQI.aqi }}</div>
                <div class="text-xs opacity-80">AQI</div>
              </div>
              <div class="text-left">
                <div class="text-sm text-gray-500">{{ $t('dashboard.aqi') }}</div>
                <div class="text-3xl font-bold text-gray-900">{{ currentAQI.category }}</div>
                <div class="text-sm text-gray-500">{{ currentAQI.dominant_pollutant }}</div>
              </div>
            </div>
          </div>

          <!-- Pollutant Grid -->
          <div v-if="latestData" class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div class="bg-gray-50 rounded-2xl p-4 text-center hover:bg-gray-100 transition-colors">
              <div class="text-2xl mb-2">💨</div>
              <div class="text-xs text-gray-500">{{ $t('pollutants.pm25') }}</div>
              <div class="text-2xl font-bold text-gray-900">{{ latestData.pm25?.toFixed(1) || '--' }}</div>
              <div class="text-xs text-gray-400">µg/m³</div>
            </div>
            <div class="bg-gray-50 rounded-2xl p-4 text-center hover:bg-gray-100 transition-colors">
              <div class="text-2xl mb-2">🌫️</div>
              <div class="text-xs text-gray-500">{{ $t('pollutants.pm10') }}</div>
              <div class="text-2xl font-bold text-gray-900">{{ latestData.pm10?.toFixed(1) || '--' }}</div>
              <div class="text-xs text-gray-400">µg/m³</div>
            </div>
            <div class="bg-gray-50 rounded-2xl p-4 text-center hover:bg-gray-100 transition-colors">
              <div class="text-2xl mb-2">⚗️</div>
              <div class="text-xs text-gray-500">{{ $t('pollutants.no2') }}</div>
              <div class="text-2xl font-bold text-gray-900">{{ latestData.no2?.toFixed(1) || '--' }}</div>
              <div class="text-xs text-gray-400">µg/m³</div>
            </div>
            <div class="bg-gray-50 rounded-2xl p-4 text-center hover:bg-gray-100 transition-colors">
              <div class="text-2xl mb-2">🌡️</div>
              <div class="text-xs text-gray-500">{{ $t('pollutants.temperature') }}</div>
              <div class="text-2xl font-bold text-gray-900">{{ latestData.temperature?.toFixed(1) || '--' }}°</div>
              <div class="text-xs text-gray-400">Celsius</div>
            </div>
          </div>

          <NuxtLink
            to="/dashboard"
            class="block w-full py-4 bg-gray-900 text-white rounded-2xl font-semibold text-center hover:bg-gray-800 transition-colors"
          >
            {{ $t('common.viewMore') }} →
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="relative z-10 py-24 bg-gradient-to-r from-blue-600 to-purple-600">
      <div class="container mx-auto px-4 text-center text-white">
        <h2 class="text-4xl md:text-5xl font-bold mb-6">{{ $t('cta.title') }}</h2>
        <p class="text-xl mb-8 opacity-90">{{ $t('cta.subtitle') }}</p>
        <NuxtLink
          to="/register"
          class="inline-block px-12 py-4 bg-white text-purple-600 rounded-2xl font-bold text-lg shadow-2xl hover:shadow-3xl hover:-translate-y-1 transition-all duration-300"
        >
          {{ $t('cta.button') }}
        </NuxtLink>
      </div>
    </section>

    <!-- Footer -->
    <footer class="relative z-10 bg-gray-900 text-white py-16">
      <div class="container mx-auto px-4">
        <div class="grid md:grid-cols-4 gap-8 mb-12">
          <div>
            <div class="flex items-center space-x-2 mb-4">
              <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-xl">
                🌍
              </div>
              <div class="text-xl font-bold">{{ $t('app.name') }}</div>
            </div>
            <p class="text-gray-400 text-sm">{{ $t('footer.description') }}</p>
          </div>
          <div>
            <h4 class="font-semibold mb-4">{{ $t('footer.product') }}</h4>
            <div class="space-y-2 text-sm text-gray-400">
              <div class="hover:text-white cursor-pointer transition">{{ $t('footer.features') }}</div>
              <div class="hover:text-white cursor-pointer transition">{{ $t('footer.pricing') }}</div>
              <div class="hover:text-white cursor-pointer transition">{{ $t('footer.api') }}</div>
            </div>
          </div>
          <div>
            <h4 class="font-semibold mb-4">{{ $t('footer.company') }}</h4>
            <div class="space-y-2 text-sm text-gray-400">
              <div class="hover:text-white cursor-pointer transition">{{ $t('footer.about') }}</div>
              <div class="hover:text-white cursor-pointer transition">{{ $t('footer.blog') }}</div>
              <div class="hover:text-white cursor-pointer transition">{{ $t('footer.careers') }}</div>
            </div>
          </div>
          <div>
            <h4 class="font-semibold mb-4">{{ $t('footer.resources') }}</h4>
            <div class="space-y-2 text-sm text-gray-400">
              <div class="hover:text-white cursor-pointer transition">{{ $t('footer.documentation') }}</div>
              <div class="hover:text-white cursor-pointer transition">{{ $t('footer.support') }}</div>
              <div class="hover:text-white cursor-pointer transition">{{ $t('footer.status') }}</div>
            </div>
          </div>
        </div>
        <div class="border-t border-gray-800 pt-8 text-center text-sm text-gray-400">
          <p>© 2025 {{ $t('footer.copyright') }} • Made for GDG Fest Hackathon 2025</p>
        </div>
      </div>
    </footer>

    <!-- AI Chat -->
    <AiChat />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const { t } = useI18n()
const config = useRuntimeConfig()

const loading = ref(true)
const sensorsCount = ref(5)
const latestData = ref(null)
const currentAQI = ref(null)

const scrollToDemo = () => {
  document.getElementById('demo')?.scrollIntoView({ behavior: 'smooth' })
}

const fetchData = async () => {
  loading.value = true
  try {
    // Fetch sensors
    const sensorsRes = await fetch(`${config.public.iotApiUrl}/sensors`)
    const sensorsData = await sensorsRes.json()
    sensorsCount.value = sensorsData.sensors?.length || 5

    // Fetch latest reading
    const readingsRes = await fetch(`${config.public.iotApiUrl}/readings/recent?limit=1`)
    const readingsData = await readingsRes.json()
    if (readingsData.readings?.length > 0) {
      latestData.value = readingsData.readings[0]
    }

    // Fetch AQI
    const aqiRes = await fetch(`${config.public.analyticsApiUrl}/aqi/current`)
    const aqiData = await aqiRes.json()
    currentAQI.value = aqiData
  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
  setInterval(fetchData, 60000)
})
</script>

<style scoped>
@keyframes blob {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}

.animate-blob {
  animation: blob 10s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}
</style>
