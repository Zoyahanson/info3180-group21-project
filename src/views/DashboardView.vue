<template>
  <div class="container mt-5">

    <h1 class="mb-4">Potential Matches</h1>

    <!-- Filters -->
    <div class="card p-4 mb-4">
      <div class="row">

        <!-- Search -->
        <div class="col-md-3 mb-3">
          <input type="text" class="form-control" placeholder="Search by name..." v-model="search" />
        </div>

        <!-- Age Filter -->
        <div class="col-md-3 mb-3">
          <select class="form-select" v-model="selectedAge">
            <option value="">All Ages</option>
            <option value="18-22">18–22</option>
            <option value="23-27">23–27</option>
            <option value="28-35">28–35</option>
          </select>
        </div>

        <!-- Location Filter -->
        <div class="col-md-3 mb-3">
          <input type="text" class="form-control" placeholder="Filter by location..." v-model="location" />
        </div>

        <!-- Sort -->
        <div class="col-md-3 mb-3">
          <select class="form-select" v-model="sortBy">
            <option value="newest">Newest</option>
            <option value="oldest">Oldest</option>
          </select>
        </div>

      </div>

      <!-- Interest Filters toggle -->
      <button class="btn btn-primary w-100 mb-2" @click="showInterests = !showInterests">
        {{ showInterests ? 'Hide Interest Filters' : 'Show Interest Filters' }}
      </button>

      <div v-if="showInterests" class="d-flex flex-wrap gap-2 mb-3 mt-1">
        <span
          v-for="interest in allInterests"
          :key="interest.id"
          class="badge border"
          :class="selectedInterests.includes(interest.id) ? 'bg-primary text-white' : 'bg-light text-dark'"
          style="cursor:pointer; font-size:0.9rem; padding:8px 12px"
          @click="toggleInterest(interest.id)"
        >
          {{ interest.name }}
        </span>
      </div>

      <button class="btn btn-secondary w-100" @click="resetFilters">
        Reset Filters
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center mt-5">
      <h5>Loading profiles...</h5>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredMatches.length === 0" class="mt-5">
      <div class="empty-state">No profiles found.</div>
    </div>

    <!-- Match Cards -->
    <MatchCard
      v-for="profile in filteredMatches"
      :key="profile.id"
      :match="profile"
      type="dashboard"
      @like="likeUser"
      @dislike="dislikeUser"
      @pass="passUser"
      @favorite="favoriteUser"
    />

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import MatchCard from '../components/MatchCard.vue'
import api from '../services/api'

const store = useStore()

const search            = ref('')
const selectedAge       = ref('')
const location          = ref('')
const sortBy            = ref('newest')
const showInterests     = ref(false)
const selectedInterests = ref([])
const allInterests      = ref([])
const profiles          = ref([])
const loading           = ref(false)

const fetchInterests = async () => {
  try {
    const res = await api.get('/interests')
    allInterests.value = res.data
  } catch (err) {
    console.log(err)
  }
}

const fetchProfiles = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (sortBy.value) params.append('sort', sortBy.value)
    const response = await api.get('/search?' + params.toString())
    profiles.value = response.data
  } catch (err) {
    console.log(err)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchInterests()
  fetchProfiles()
})

const toggleInterest = (id) => {
  const idx = selectedInterests.value.indexOf(id)
  if (idx === -1) selectedInterests.value.push(id)
  else selectedInterests.value.splice(idx, 1)
}

const resetFilters = () => {
  search.value            = ''
  selectedAge.value       = ''
  location.value          = ''
  sortBy.value            = 'newest'
  selectedInterests.value = []
  showInterests.value     = false
}

/* Client-side filter on top of server results */
const filteredMatches = computed(() => {
  return profiles.value.filter((profile) => {
    const matchesSearch = (profile.name || '').toLowerCase().includes(search.value.toLowerCase())

    const matchesLocation = (profile.location || '').toLowerCase().includes(location.value.toLowerCase())

    let matchesAge = true
    if (selectedAge.value === '18-22')  matchesAge = profile.age >= 18 && profile.age <= 22
    else if (selectedAge.value === '23-27') matchesAge = profile.age >= 23 && profile.age <= 27
    else if (selectedAge.value === '28-35') matchesAge = profile.age >= 28 && profile.age <= 35

    const matchesInterests = selectedInterests.value.length === 0 ||
      selectedInterests.value.some(id => {
        const interest = allInterests.value.find(i => i.id === id)
        return interest && (profile.interests || []).includes(interest.name)
      })

    return matchesSearch && matchesLocation && matchesAge && matchesInterests
  })
})

const likeUser = async (profileId) => {
  const currentUserId = store.state.user?.id
  if (!currentUserId) { alert('Please log in again.'); return }
  try {
    const res = await api.post('/like', { user1_id: currentUserId, user2_id: profileId })
    alert(res.data.message)
  } catch (err) { console.log(err) }
}

const dislikeUser = async (profileId) => {
  const currentUserId = store.state.user?.id
  if (!currentUserId) return
  try {
    await api.post('/dislike', { user1_id: currentUserId, user2_id: profileId })
  } catch (err) { console.log(err) }
  profiles.value = profiles.value.filter(p => p.id !== profileId)
}

const passUser = (id) => {
  profiles.value = profiles.value.filter(p => p.id !== id)
}

const favoriteUser = async (profileId) => {
  try {
    await api.post('/favorites', { favorited_user_id: profileId })
    alert('Added to favorites!')
  } catch (err) { console.log(err) }
}
</script>