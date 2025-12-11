<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <!-- Background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-96 h-96 bg-blue-100 rounded-full mix-blend-multiply filter blur-3xl opacity-40 animate-blob"></div>
      <div class="absolute bottom-20 right-10 w-96 h-96 bg-purple-100 rounded-full mix-blend-multiply filter blur-3xl opacity-40 animate-blob animation-delay-2000"></div>
    </div>

    <div class="relative z-10 w-full max-w-md">
      <!-- Logo -->
      <NuxtLink to="/" class="flex items-center justify-center space-x-3 mb-8">
        <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-2xl shadow-lg">
          🌍
        </div>
        <div>
          <h1 class="text-2xl font-bold text-gray-800">{{ $t('app.name') }}</h1>
          <p class="text-sm text-gray-500">{{ $t('app.tagline') }}</p>
        </div>
      </NuxtLink>

      <!-- Login Card -->
      <div class="bg-white rounded-3xl p-8 shadow-xl shadow-gray-200/50 border border-gray-100">
        <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ $t('auth.welcomeBack') }}</h2>
        <p class="text-gray-500 mb-6">{{ $t('auth.signInSubtitle') }}</p>

        <!-- Error Message -->
        <Transition
          enter-active-class="transition duration-300 ease-out"
          enter-from-class="transform -translate-y-2 opacity-0"
          enter-to-class="transform translate-y-0 opacity-100"
        >
          <div v-if="errorMessage" class="bg-red-50 border border-red-100 rounded-xl p-4 mb-6">
            <div class="flex items-center space-x-2 text-red-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="text-sm">{{ errorMessage }}</span>
            </div>
          </div>
        </Transition>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('auth.email') }}</label>
            <input
              v-model="email"
              type="email"
              required
              placeholder="your@email.com"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('auth.password') }}</label>
            <input
              v-model="password"
              type="password"
              required
              placeholder="••••••••"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            />
          </div>

          <div class="flex items-center justify-between">
            <label class="flex items-center space-x-2 cursor-pointer">
              <input
                v-model="rememberMe"
                type="checkbox"
                class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span class="text-sm text-gray-600">{{ $t('auth.rememberMe') }}</span>
            </label>
            <a href="#" class="text-sm text-blue-600 hover:text-blue-700 font-medium">
              {{ $t('auth.forgotPassword') }}
            </a>
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/30 disabled:opacity-50 transition-all"
          >
            <span v-if="!isLoading">{{ $t('auth.signIn') }} →</span>
            <span v-else class="flex items-center justify-center space-x-2">
              <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>{{ $t('auth.signingIn') }}</span>
            </span>
          </button>
        </form>

        <!-- Divider -->
        <div class="relative my-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-200"></div>
          </div>
          <div class="relative flex justify-center">
            <span class="px-4 bg-white text-sm text-gray-500">{{ $t('auth.orContinueWith') }}</span>
          </div>
        </div>

        <!-- Social Login -->
        <div class="grid grid-cols-2 gap-4 mb-6">
          <button
            @click="handleGoogleLogin"
            class="py-3 bg-gray-50 border border-gray-200 rounded-xl font-medium flex items-center justify-center space-x-2 hover:bg-gray-100 transition-colors"
          >
            <svg class="w-5 h-5" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            <span>{{ $t('auth.googleSignIn') }}</span>
          </button>
          <button
            @click="handleGithubLogin"
            class="py-3 bg-gray-900 text-white rounded-xl font-medium flex items-center justify-center space-x-2 hover:bg-gray-800 transition-colors"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            <span>{{ $t('auth.githubSignIn') }}</span>
          </button>
        </div>

        <!-- Sign Up Link -->
        <div class="text-center text-sm text-gray-600">
          {{ $t('auth.noAccount') }}
          <NuxtLink to="/register" class="text-blue-600 hover:text-blue-700 font-semibold ml-1">
            {{ $t('auth.signUp') }}
          </NuxtLink>
        </div>
      </div>

      <!-- Language Switcher & Back -->
      <div class="flex items-center justify-between mt-6">
        <NuxtLink to="/" class="text-sm text-gray-500 hover:text-gray-700 transition">
          ← {{ $t('auth.backToHome') }}
        </NuxtLink>
        <LanguageSwitcher />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const router = useRouter()
const config = useRuntimeConfig()

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

let auth = null

const initFirebase = async () => {
  try {
    const { getAuth } = await import('firebase/auth')
    const { initializeApp, getApps } = await import('firebase/app')

    if (getApps().length === 0) {
      initializeApp({
        apiKey: config.public.firebaseApiKey,
        authDomain: config.public.firebaseAuthDomain,
        projectId: config.public.firebaseProjectId,
        storageBucket: config.public.firebaseStorageBucket,
        messagingSenderId: config.public.firebaseMessagingSenderId,
        appId: config.public.firebaseAppId
      })
    }

    auth = getAuth()
    return true
  } catch (error) {
    console.error('Firebase not available:', error)
    return false
  }
}

const handleLogin = async () => {
  errorMessage.value = ''
  isLoading.value = true

  try {
    const firebaseAvailable = await initFirebase()

    if (!firebaseAvailable) {
      router.push('/dashboard')
      return
    }

    const { signInWithEmailAndPassword } = await import('firebase/auth')
    const userCredential = await signInWithEmailAndPassword(auth, email.value, password.value)
    const idToken = await userCredential.user.getIdToken()

    if (typeof window !== 'undefined') {
      localStorage.setItem('authToken', idToken)
      if (rememberMe.value) {
        localStorage.setItem('userEmail', email.value)
      }
    }

    router.push('/dashboard')
  } catch (error) {
    console.error('Login error:', error)
    errorMessage.value = error.message || t('common.error')
  } finally {
    isLoading.value = false
  }
}

const handleGoogleLogin = async () => {
  errorMessage.value = ''
  isLoading.value = true

  try {
    const firebaseAvailable = await initFirebase()
    if (!firebaseAvailable) {
      errorMessage.value = 'Google Sign-In requires Firebase configuration'
      isLoading.value = false
      return
    }

    const { signInWithPopup, GoogleAuthProvider } = await import('firebase/auth')
    const provider = new GoogleAuthProvider()
    const result = await signInWithPopup(auth, provider)
    const idToken = await result.user.getIdToken()

    if (typeof window !== 'undefined') {
      localStorage.setItem('authToken', idToken)
    }

    router.push('/dashboard')
  } catch (error) {
    console.error('Google login error:', error)
    errorMessage.value = error.message || t('common.error')
  } finally {
    isLoading.value = false
  }
}

const handleGithubLogin = async () => {
  errorMessage.value = ''
  isLoading.value = true

  try {
    const firebaseAvailable = await initFirebase()
    if (!firebaseAvailable) {
      errorMessage.value = 'GitHub Sign-In requires Firebase configuration'
      isLoading.value = false
      return
    }

    const { signInWithPopup, GithubAuthProvider } = await import('firebase/auth')
    const provider = new GithubAuthProvider()
    const result = await signInWithPopup(auth, provider)
    const idToken = await result.user.getIdToken()

    if (typeof window !== 'undefined') {
      localStorage.setItem('authToken', idToken)
    }

    router.push('/dashboard')
  } catch (error) {
    console.error('GitHub login error:', error)
    errorMessage.value = error.message || t('common.error')
  } finally {
    isLoading.value = false
  }
}

// Load remembered email
if (typeof window !== 'undefined') {
  const rememberedEmail = localStorage.getItem('userEmail')
  if (rememberedEmail) {
    email.value = rememberedEmail
    rememberMe.value = true
  }
}
</script>

<style scoped>
@keyframes blob {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(30px, -30px) scale(1.1); }
}

.animate-blob {
  animation: blob 8s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}
</style>
