<script setup>
import { RouterView, useRoute } from 'vue-router'

import AppHeader from "@/components/AppHeader.vue"
import AppFooter from "@/components/AppFooter.vue"

const route = useRoute()

const hideNavbarRoutes = ['/login', '/register']
</script>

<template>

  <!-- Hide Navbar on Login/Register -->
  <AppHeader
    v-if="!hideNavbarRoutes.includes(route.path)"
  />

  <RouterView />

  <AppFooter />

</template>