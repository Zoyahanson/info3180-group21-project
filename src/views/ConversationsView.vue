<template>
  <div class="container mt-5">

    <h1 class="mb-4">Messages</h1>

    <div v-if="loading" class="text-center mt-5">
      <h5>Loading conversations...</h5>
    </div>

    <div v-else-if="matches.length === 0" class="text-center mt-5">
      <h5>No conversations yet. Match with someone to start chatting!</h5>
      <router-link to="/dashboard" class="btn btn-primary mt-3">Find Matches</router-link>
    </div>

    <div v-else>
      <div
        v-for="match in matches"
        :key="match.id"
        class="card mb-3 conversation-card"
        @click="openChat(match.id)"
        style="cursor: pointer"
      >
        <div class="card-body d-flex align-items-center gap-3">

          <img
            :src="match.other_user?.profile_picture
              ? '/uploads/' + match.other_user.profile_picture
              : 'https://via.placeholder.com/60'"
            class="rounded-circle"
            width="60"
            height="60"
            style="object-fit: cover"
          />

          <div>
            <h5 class="mb-0">{{ match.other_user?.name || 'Unknown' }}</h5>
            <small class="text-muted">{{ match.other_user?.location || '' }}</small>
          </div>

          <div class="ms-auto">
            <span class="badge bg-primary">Chat</span>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import api from '../services/api'

const router  = useRouter()
const store   = useStore()
const matches = ref([])
const loading = ref(false)

const fetchMatches = async () => {
  const userId = store.state.user?.id
  if (!userId) return

  loading.value = true
  try {
    const res = await api.get(`/matches/${userId}`)
    matches.value = res.data
  } catch (err) {
    console.log(err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchMatches)

const openChat = (matchId) => {
  router.push(`/messages/${matchId}`)
}
</script>

<style scoped>
.conversation-card:hover {
  background-color: #f8f9fa;
  transition: background-color 0.2s;
}
</style>
