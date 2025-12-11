<template>
  <div class="fixed bottom-6 right-6 z-50">
    <!-- Chat Toggle Button -->
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="transform scale-0 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-0 opacity-0"
    >
      <button
        v-if="!isOpen"
        @click="isOpen = true"
        class="w-16 h-16 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-2xl flex items-center justify-center hover:scale-110 transition-transform duration-300 glow"
      >
        <span class="text-2xl">🤖</span>
      </button>
    </Transition>

    <!-- Chat Window -->
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="transform translate-y-4 opacity-0"
      enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform translate-y-4 opacity-0"
    >
      <div
        v-if="isOpen"
        class="w-96 h-[32rem] glass-dark rounded-3xl shadow-2xl flex flex-col overflow-hidden border border-white/20"
      >
        <!-- Header -->
        <div class="px-4 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <span class="text-2xl">🤖</span>
            <div>
              <h3 class="font-bold">{{ $t('chat.title') }}</h3>
              <p class="text-xs opacity-80">EcoAssist</p>
            </div>
          </div>
          <button
            @click="isOpen = false"
            class="w-8 h-8 rounded-full hover:bg-white/20 flex items-center justify-center transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Messages -->
        <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-4">
          <!-- Welcome Message -->
          <div v-if="messages.length === 0" class="text-center py-8">
            <div class="text-4xl mb-4">🌍</div>
            <h4 class="font-semibold text-gray-700 mb-2">{{ $t('chat.title') }}</h4>
            <p class="text-sm text-gray-500 mb-4">{{ $t('chat.suggestions') }}</p>
            <div class="space-y-2">
              <button
                v-for="suggestion in suggestions"
                :key="suggestion"
                @click="sendMessage(suggestion)"
                class="w-full px-4 py-2 text-left text-sm glass rounded-xl hover:bg-white/50 transition-colors"
              >
                {{ suggestion }}
              </button>
            </div>
          </div>

          <!-- Message List -->
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="flex"
            :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
          >
            <div
              class="max-w-[80%] px-4 py-3 rounded-2xl"
              :class="message.role === 'user'
                ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-br-none'
                : 'glass border border-gray-100 rounded-bl-none'"
            >
              <p class="text-sm whitespace-pre-wrap">{{ message.content }}</p>
              <span class="text-[10px] opacity-60 mt-1 block">
                {{ formatTime(message.timestamp) }}
              </span>
            </div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="isTyping" class="flex justify-start">
            <div class="glass border border-gray-100 px-4 py-3 rounded-2xl rounded-bl-none">
              <div class="flex space-x-2">
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="p-4 border-t border-gray-100">
          <form @submit.prevent="handleSubmit" class="flex items-center space-x-2">
            <input
              v-model="input"
              :placeholder="$t('chat.placeholder')"
              class="flex-1 px-4 py-3 glass border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              :disabled="isTyping"
            />
            <button
              type="submit"
              :disabled="!input.trim() || isTyping"
              class="w-12 h-12 rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 text-white flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed hover:scale-105 transition-transform"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'

const { t, locale } = useI18n()
const config = useRuntimeConfig()

const isOpen = ref(false)
const input = ref('')
const messages = ref([])
const isTyping = ref(false)
const messagesContainer = ref(null)
const suggestions = ref([])

// Format timestamp
const formatTime = (date) => {
  return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Scroll to bottom of messages
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Load suggestions
const loadSuggestions = async () => {
  try {
    const response = await fetch(`${config.public.analyticsApiUrl}/chat/suggestions?language=${locale.value}`)
    const data = await response.json()
    suggestions.value = data.suggestions || []
  } catch (error) {
    console.error('Failed to load suggestions:', error)
    suggestions.value = [
      locale.value === 'ru' ? 'Какое качество воздуха сейчас?' :
      locale.value === 'kk' ? 'Ауа сапасы қандай?' :
      'What is the current air quality?'
    ]
  }
}

// Send message
const sendMessage = async (text) => {
  if (!text.trim()) return

  const userMessage = {
    role: 'user',
    content: text,
    timestamp: new Date()
  }

  messages.value.push(userMessage)
  input.value = ''
  isTyping.value = true
  await scrollToBottom()

  try {
    const response = await fetch(`${config.public.analyticsApiUrl}/chat?message=${encodeURIComponent(text)}&language=${locale.value}`, {
      method: 'POST'
    })

    const data = await response.json()

    const assistantMessage = {
      role: 'assistant',
      content: data.response || t('chat.error'),
      timestamp: new Date()
    }

    messages.value.push(assistantMessage)
  } catch (error) {
    console.error('Chat error:', error)
    messages.value.push({
      role: 'assistant',
      content: t('chat.error'),
      timestamp: new Date()
    })
  } finally {
    isTyping.value = false
    await scrollToBottom()
  }
}

const handleSubmit = () => {
  sendMessage(input.value)
}

onMounted(() => {
  loadSuggestions()
})

// Reload suggestions when language changes
watch(locale, () => {
  loadSuggestions()
})
</script>
