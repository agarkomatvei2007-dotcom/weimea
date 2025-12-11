<template>
  <div class="relative" ref="dropdownRef">
    <button
      @click="isOpen = !isOpen"
      class="flex items-center space-x-2 px-3 py-2 rounded-xl glass border border-white/20 hover:bg-white/30 transition-all duration-300"
    >
      <span class="text-lg">{{ currentFlag }}</span>
      <span class="text-sm font-medium text-gray-700">{{ currentLang }}</span>
      <svg
        class="w-4 h-4 text-gray-500 transition-transform duration-300"
        :class="{ 'rotate-180': isOpen }"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
      <div
        v-if="isOpen"
        class="absolute right-0 mt-2 w-48 py-2 glass-dark rounded-xl shadow-xl border border-white/20 z-50"
      >
        <button
          v-for="lang in languages"
          :key="lang.code"
          @click="selectLanguage(lang.code)"
          class="w-full px-4 py-2 flex items-center space-x-3 hover:bg-white/20 transition-colors duration-200"
          :class="{ 'bg-blue-50/50': locale === lang.code }"
        >
          <span class="text-lg">{{ lang.flag }}</span>
          <span class="text-sm font-medium text-gray-700">{{ lang.name }}</span>
          <svg
            v-if="locale === lang.code"
            class="w-4 h-4 ml-auto text-blue-500"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const { locale, setLocale } = useI18n()

const isOpen = ref(false)
const dropdownRef = ref(null)

const languages = [
  { code: 'en', name: 'English', flag: '🇬🇧' },
  { code: 'ru', name: 'Русский', flag: '🇷🇺' },
  { code: 'kk', name: 'Қазақша', flag: '🇰🇿' }
]

const currentLang = computed(() => {
  const lang = languages.find(l => l.code === locale.value)
  return lang ? lang.name : 'English'
})

const currentFlag = computed(() => {
  const lang = languages.find(l => l.code === locale.value)
  return lang ? lang.flag : '🇬🇧'
})

const selectLanguage = (code) => {
  setLocale(code)
  isOpen.value = false
  if (typeof window !== 'undefined') {
    localStorage.setItem('preferred_language', code)
  }
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  // Load saved language preference
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('preferred_language')
    if (saved && languages.some(l => l.code === saved)) {
      setLocale(saved)
    }
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
