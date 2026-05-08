<template>
  <div class="container mt-5">

    <h1 class="mb-4">
      Your Matches
    </h1>

    <!-- Loading -->
    <div
      v-if="loading"
      class="text-center mt-5"
    >

      <h5>
        Loading matches...
      </h5>

    </div>

    <!-- Empty State -->
    <div
      v-else-if="matches.length === 0"
      class="text-center mt-5"
    >

      <h4>
        No matches yet.
      </h4>

    </div>

    <!-- Match Cards -->
    <MatchCard
      v-for="match in matches"
      :key="match.id"
      :match="match.other_user || match"
      type="matches"
      @message="messageUser(match.id)"
    />

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

import MatchCard from '../components/MatchCard.vue'

import api from '../services/api'

const router = useRouter()
const store = useStore()

const matches = ref([])

const loading = ref(false)

/* Fetch confirmed mutual matches */
const fetchMatches = async () => {

  const userId = store.state.user?.id

  if (!userId) return

  loading.value = true

  try {

    const response =
      await api.get(`/matches/${userId}`)

    matches.value = response.data

  }

  catch (err) {

    console.log(err)

  }

  finally {

    loading.value = false

  }
}


onMounted(() => {

  fetchMatches()

})

/* Open Messages for this match */
const messageUser = (matchId) => {

  router.push(`/messages/${matchId}`)

}
</script>