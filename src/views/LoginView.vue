<template>
  <div class="container auth-page">

  <div class="row justify-content-center w-100">

    <div class="col-md-6">

      <div class="card shadow p-4 auth-card">

          <h1 class="text-center mb-4">
            Login
          </h1>

          <!-- Error Message -->
          <div
            v-if="error"
            class="alert alert-danger"
          >

            {{ error }}

          </div>

          <form @submit.prevent="login">

            <!-- Email -->
            <div class="mb-4">

              <label class="form-label">
                Email
              </label>

              <input
                type="email"
                class="form-control"
                v-model="email"
                required
              />

            </div>

            <!-- Password -->
            <div class="mb-4">

              <label class="form-label">
                Password
              </label>

              <input
                type="password"
                class="form-control"
                v-model="password"
                required
              />

            </div>

            <!-- Login Button -->
            <button
              class="btn btn-primary w-100"
              :disabled="loading"
            >

              <span v-if="loading">
                Logging in...
              </span>

              <span v-else>
                Login
              </span>

            </button>

          </form>

          <!-- Register Link -->
          <router-link
            to="/register"
            class="text-center d-block mt-4"
          >

            Create Account

          </router-link>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'

import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

import api from '../services/api'

const router = useRouter()
const store = useStore()

const email = ref('')
const password = ref('')

const loading = ref(false)

const error = ref('')

const login = async () => {

  loading.value = true

  error.value = ''

  try {

    const res = await api.post('/login', {

      email: email.value,
      password: password.value

    })

    store.commit('setUser', { id: res.data.user_id })

    router.push('/dashboard')

  }

  catch (err) {

    error.value =
      'Invalid email or password'

    console.log(err)

  }

  finally {

    loading.value = false

  }
}
</script>
