<template>
  <div class="container mt-5">

    <div class="d-flex align-items-center mb-4 gap-3">
      <router-link to="/messages" class="btn btn-outline-secondary btn-sm">← Back</router-link>
      <h1 class="mb-0">Chat</h1>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center mt-5">
      <h5>Loading messages...</h5>
    </div>

    <!-- Empty State -->
    <div v-else-if="messages.length === 0" class="text-center">
      <h5>No messages yet. Say hello!</h5>
    </div>

    <!-- Messages -->
    <div class="messages-container mb-4">
      <div
        v-for="message in messages"
        :key="message.id"
        class="mb-3"
      >
        <!-- Other User -->
        <div v-if="message.sender_id !== currentUserId" class="text-start">
          <span class="badge bg-secondary p-3 message-bubble">
            {{ message.content }}
          </span>
          <div>
            <small class="text-muted">{{ formatTime(message.timestamp) }}</small>
          </div>
        </div>

        <!-- Current User -->
        <div v-else class="text-end">
          <span class="badge bg-primary p-3 message-bubble">
            {{ message.content }}
          </span>
          <div>
            <small class="text-muted">{{ formatTime(message.timestamp) }}</small>
          </div>
        </div>

      </div>
    </div>

    <!-- Input -->
    <form @submit.prevent="sendMessage">
      <div class="input-group mt-4">
        <input
          type="text"
          class="form-control"
          placeholder="Type a message..."
          v-model="newMessage"
        />
        <button class="btn btn-primary" :disabled="sending">
          <span v-if="sending">Sending...</span>
          <span v-else>Send</span>
        </button>
      </div>
    </form>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import api from '../services/api'

const route   = useRoute()
const store   = useStore()

const matchId       = computed(() => route.params.matchId)
const currentUserId = computed(() => store.state.user?.id)

const messages   = ref([])
const newMessage = ref('')
const loading    = ref(false)
const sending    = ref(false)

let pollInterval = null

const formatTime = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })
}

const fetchMessages = async () => {
  if (!matchId.value) return
  try {
    const res = await api.get(`/messages/${matchId.value}`)
    messages.value = res.data
  } catch (err) {
    console.log(err)
  }
}

onMounted(async () => {
  loading.value = true
  await fetchMessages()
  loading.value = false
  // Poll for new messages every 5 seconds
  pollInterval = setInterval(fetchMessages, 5000)
})

onUnmounted(() => {
  clearInterval(pollInterval)
})

const sendMessage = async () => {
  if (!newMessage.value.trim() || !matchId.value || !currentUserId.value) return

  sending.value = true
  const text = newMessage.value
  newMessage.value = ''

  try {
    const res = await api.post('/messages', {
      match_id: matchId.value,
      content:  text
    })

    messages.value.push({
      id:          res.data.id || Date.now(),
      sender_id:   currentUserId.value,
      receiver_id: null,
      content:     text,
      timestamp:   new Date().toISOString()
    })

  } catch (err) {
    console.log(err)
    newMessage.value = text
  } finally {
    sending.value = false
  }
}
</script>

<style scoped>
.messages-container {
  max-height: 60vh;
  overflow-y: auto;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
}

.message-bubble {
  font-size: 1rem;
  white-space: normal;
  max-width: 70%;
  display: inline-block;
  text-align: left;
  border-radius: 12px;
}
</style>
