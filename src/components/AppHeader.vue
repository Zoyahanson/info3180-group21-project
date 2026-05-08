<template>
  <nav class="navbar navbar-expand-lg navbar-dark px-4">

    <router-link
      class="navbar-brand"
      to="/dashboard"
    >
      DriftDater
    </router-link>

    <div class="navbar-nav ms-auto align-items-center">

      <router-link
        class="nav-link"
        to="/dashboard"
      >
        Dashboard
      </router-link>

      <router-link
        class="nav-link"
        to="/matches"
      >
        Matches
      </router-link>

      <router-link
        class="nav-link"
        to="/messages"
      >
        Messages
      </router-link>

      <router-link
        class="nav-link"
        to="/profile"
      >
        Profile
      </router-link>

      <!-- Dark Mode Button -->
      <button
        class="btn btn-outline-light ms-3"
        @click="toggleDarkMode"
      >
        Dark Mode
      </button>

      <!-- Logout Button -->
      <button
        class="btn btn-light ms-2"
        @click="logout"
      >
        Logout
      </button>

    </div>

  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

import api from '../services/api'

const router = useRouter()
const store = useStore()

const logout = async () => {

  try {
    await api.post('/logout')
  } catch (err) {
    console.log(err)
  }

  store.commit('logout')
  router.push('/login')
}

/* Dark Mode Toggle */
const toggleDarkMode = () => {

  document.body.classList.toggle('dark-mode')

}
</script>