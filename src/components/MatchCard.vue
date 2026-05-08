<template>
  <div class="card shadow-sm p-3 mb-4 match-card">

    <div class="row align-items-center">

      <!-- Profile Image -->
      <div class="col-md-2 text-center">
        <img
          :src="match.profile_picture
            ? '/uploads/' + match.profile_picture
            : defaultAvatar"
          class="img-fluid rounded-circle profile-img"
          alt="Profile photo"
        />
      </div>

      <!-- User Info -->
      <div class="col-md-7">
        <h4 class="match-name">
          {{ match.name }}<span v-if="match.age">, {{ match.age }}</span>
        </h4>
        <p class="match-bio">{{ match.bio }}</p>
        <small class="text-muted">{{ match.location }}</small>
        <div v-if="match.interests && match.interests.length" class="mt-1">
          <span
            v-for="interest in match.interests"
            :key="interest"
            class="badge bg-light text-dark me-1 border"
          >{{ interest }}</span>
        </div>
      </div>

      <!-- Buttons -->
      <div class="col-md-3 text-center">

        <!-- Dashboard Buttons -->
        <div
          v-if="type === 'dashboard'"
          class="d-flex flex-wrap justify-content-center gap-2"
        >
          <button class="btn btn-success action-btn" @click="$emit('like', match.user_id || match.id)">
            Like
          </button>
          <button class="btn btn-danger action-btn" @click="$emit('dislike', match.user_id || match.id)">
            Dislike
          </button>
          <button class="btn btn-secondary action-btn" @click="$emit('pass', match.user_id || match.id)">
            Pass
          </button>
          <button class="btn btn-warning action-btn" @click="$emit('favorite', match.user_id || match.id)">
            ★ Save
          </button>
        </div>

        <!-- Matches Buttons -->
        <div
          v-else-if="type === 'matches'"
          class="d-flex flex-wrap justify-content-center gap-2"
        >
          <button class="btn btn-primary action-btn" @click="$emit('message', match.id)">
            Message
          </button>
        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
defineProps({
  match: Object,
  type:  String
})

defineEmits(['like', 'dislike', 'pass', 'favorite', 'message'])

const defaultAvatar = `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' fill='%23ffd6de'/%3E%3Ccircle cx='50' cy='38' r='18' fill='%23ff85a1'/%3E%3Cellipse cx='50' cy='80' rx='28' ry='20' fill='%23ff85a1'/%3E%3C/svg%3E`
</script>

<style scoped>
.profile-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border: 4px solid #ffd6de;
}

.action-btn {
  min-width: 80px;
  border-radius: 14px;
  font-weight: bold;
  padding: 8px 12px;
}
</style>
