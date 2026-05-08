<template>
  <div class="container mt-5">

    <h1 class="mb-4">My Profile</h1>

    <div class="card shadow-sm p-4">

      <div v-if="loading" class="text-center">
        <h5>Loading profile...</h5>
      </div>

      <div v-else-if="saveSuccess" class="alert alert-success">
        Profile updated successfully!
      </div>

      <form @submit.prevent="saveProfile">

        <!-- Name -->
        <div class="mb-3">
          <label class="form-label fw-bold">Name</label>
          <input type="text" class="form-control" v-model="profile.name" required />
        </div>

        <!-- Age -->
        <div class="mb-3">
          <label class="form-label fw-bold">Age</label>
          <input type="number" class="form-control" v-model="profile.age" min="18" max="120" />
        </div>

        <!-- Gender -->
        <div class="mb-3">
          <label class="form-label fw-bold">Gender</label>
          <select class="form-select" v-model="profile.gender">
            <option value="">Select gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <!-- Looking For -->
        <div class="mb-3">
          <label class="form-label fw-bold">Looking For</label>
          <select class="form-select" v-model="profile.looking_for">
            <option value="any">Any</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>

        <!-- Bio -->
        <div class="mb-3">
          <label class="form-label fw-bold">Bio</label>
          <textarea class="form-control" rows="4" v-model="profile.bio"></textarea>
        </div>

        <!-- Location -->
        <div class="mb-3">
          <label class="form-label fw-bold">Location</label>
          <input type="text" class="form-control" v-model="profile.location" placeholder="e.g. Kingston" />
        </div>

        <!-- Profile Visibility -->
        <div class="mb-3">
          <label class="form-label fw-bold">Profile Visibility</label>
          <select class="form-select" v-model="profile.visibility">
            <option value="public">Public</option>
            <option value="private">Private</option>
          </select>
        </div>

        <!-- Profile Photo -->
        <div class="mb-3">
          <label class="form-label fw-bold">Profile Photo</label>
          <div v-if="currentPhoto" class="mb-2">
            <img :src="'/uploads/' + currentPhoto" class="rounded-circle" width="80" height="80" style="object-fit:cover; border:3px solid #ffd6de" />
          </div>
          <input type="file" class="form-control" accept="image/*" @change="onPhotoChange" />
          <small v-if="photoUploading" class="text-muted">Uploading...</small>
          <small v-if="photoSuccess" class="text-success">Photo updated!</small>
        </div>

        <!-- Interests -->
        <div class="mb-4">
          <label class="form-label fw-bold">Interests (select at least 3)</label>
          <div class="d-flex flex-wrap gap-2 mt-2">
            <div
              v-for="interest in allInterests"
              :key="interest.id"
              class="form-check"
              style="min-width: 140px"
            >
              <input
                class="form-check-input"
                type="checkbox"
                :id="'interest-' + interest.id"
                :value="interest.id"
                v-model="profile.selectedInterests"
              />
              <label class="form-check-label" :for="'interest-' + interest.id">
                {{ interest.name }}
              </label>
            </div>
          </div>
          <small v-if="profile.selectedInterests.length < 3" class="text-danger">
            Please select at least 3 interests.
          </small>
        </div>

        <!-- Save Button -->
        <button class="btn btn-success" :disabled="saving || profile.selectedInterests.length < 3">
          <span v-if="saving">Saving...</span>
          <span v-else>Save Profile</span>
        </button>

      </form>

    </div>

  </div>
</template>

<script setup>
import { reactive, onMounted, ref } from 'vue'
import api from '../services/api'

const loading        = ref(false)
const saving         = ref(false)
const saveSuccess    = ref(false)
const allInterests   = ref([])
const currentPhoto   = ref('')
const photoUploading = ref(false)
const photoSuccess   = ref(false)

const profile = reactive({
  name:              '',
  age:               '',
  gender:            '',
  looking_for:       'any',
  bio:               '',
  location:          '',
  visibility:        'public',
  selectedInterests: []
})

const fetchInterests = async () => {
  try {
    const res = await api.get('/interests')
    allInterests.value = res.data
  } catch (err) {
    console.log(err)
  }
}

const fetchProfile = async () => {
  loading.value = true
  try {
    const res = await api.get('/profile')
    profile.name        = res.data.name        || ''
    profile.age         = res.data.age         || ''
    profile.gender      = res.data.gender      || ''
    profile.looking_for = res.data.looking_for || 'any'
    profile.bio         = res.data.bio         || ''
    profile.location    = res.data.location    || ''
    profile.visibility  = res.data.visibility  || 'public'
    profile.selectedInterests = res.data.interest_ids || []
    currentPhoto.value = res.data.profile_picture || ''
  } catch (err) {
    console.log(err)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchInterests()
  await fetchProfile()
})

const onPhotoChange = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  photoUploading.value = true
  photoSuccess.value = false
  const form = new FormData()
  form.append('photo', file)
  try {
    const res = await api.post('/profile/photo', form, { headers: { 'Content-Type': 'multipart/form-data' } })
    currentPhoto.value = res.data.profile_picture
    photoSuccess.value = true
    setTimeout(() => { photoSuccess.value = false }, 3000)
  } catch (err) {
    console.log(err)
  } finally {
    photoUploading.value = false
  }
}

const saveProfile = async () => {
  saving.value = true
  saveSuccess.value = false
  try {
    await api.put('/profile', {
      name:        profile.name,
      age:         profile.age,
      gender:      profile.gender,
      looking_for: profile.looking_for,
      bio:         profile.bio,
      location:    profile.location,
      visibility:  profile.visibility,
      interests:   profile.selectedInterests
    })
    saveSuccess.value = true
    setTimeout(() => { saveSuccess.value = false }, 3000)
  } catch (err) {
    console.log(err)
  } finally {
    saving.value = false
  }
}
</script>
