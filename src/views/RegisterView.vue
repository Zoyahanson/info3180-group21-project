<template>
  <div class="container py-5">

    <div class="row justify-content-center">

      <div class="col-md-6">

        <div class="card shadow p-4 rounded-4">

          <h1 class="text-center mb-4 signup-title">
            Sign Up
          </h1>

          <!-- Error -->
          <div
            v-if="error"
            class="alert alert-danger"
          >

            {{ error }}

          </div>

          <!-- Success -->
          <div
            v-if="success"
            class="alert alert-success"
          >

            Registration successful!

          </div>

          <form @submit.prevent="register">

            <!-- Email -->
            <div class="mb-4">

              <label class="form-label">
                Email
              </label>

              <input
                type="email"
                class="form-control custom-input"
                placeholder="your@email.com"
                v-model="email"
                required
              />

            </div>

            <!-- Username -->
            <div class="mb-4">

              <label class="form-label">
                Username
              </label>

              <input
                type="text"
                class="form-control custom-input"
                placeholder="username"
                v-model="username"
                required
              />

            </div>

            <!-- First Name -->
            <div class="mb-4">

              <label class="form-label">
                First Name
              </label>

              <input
                type="text"
                class="form-control custom-input"
                placeholder="First Name"
                v-model="firstName"
                required
              />

            </div>

            <!-- Last Name -->
            <div class="mb-4">

              <label class="form-label">
                Last Name
              </label>

              <input
                type="text"
                class="form-control custom-input"
                placeholder="Last Name"
                v-model="lastName"
                required
              />

            </div>

            <!-- Date of Birth -->
            <div class="mb-4">

              <label class="form-label">
                Date of Birth
              </label>

              <input
                type="date"
                class="form-control custom-input"
                v-model="dob"
                required
              />

            </div>

            <!-- Gender -->
            <div class="mb-4">

              <label class="form-label">
                Gender
              </label>

              <select
                class="form-select custom-input"
                v-model="gender"
              >

                <option disabled value="">
                  Select gender
                </option>

                <option>
                  Male
                </option>

                <option>
                  Female
                </option>

                <option>
                  Other
                </option>

              </select>

            </div>

            <!-- Looking For -->
            <div class="mb-4">

              <label class="form-label">
                Looking For
              </label>

              <select
                class="form-select custom-input"
                v-model="lookingFor"
              >

                <option>
                  Any
                </option>

                <option>
                  Male
                </option>

                <option>
                  Female
                </option>

              </select>

            </div>

            <!-- Password -->
            <div class="mb-4">

              <label class="form-label">
                Password
              </label>

              <input
                type="password"
                class="form-control custom-input"
                placeholder="Password"
                v-model="password"
                required
              />

            </div>

            <!-- Button -->
            <button
              class="btn btn-primary w-100 signup-btn"
              :disabled="loading"
            >

              <span v-if="loading">
                Creating Account...
              </span>

              <span v-else>
                Sign Up
              </span>

            </button>

          </form>

          <p class="text-center mt-4">

            Already have an account?

            <router-link to="/login">
              Login
            </router-link>

          </p>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'

import { useRouter } from 'vue-router'

import api from '../services/api'

const router = useRouter()

const email = ref('')
const username = ref('')
const firstName = ref('')
const lastName = ref('')
const dob = ref('')
const gender = ref('')
const lookingFor = ref('Any')
const password = ref('')

const loading = ref(false)

const error = ref('')

const success = ref(false)

/* Register User */
const register = async () => {

  loading.value = true
  error.value = ''
  success.value = false

  try {

    await api.post('/register', {
      email:      email.value,
      username:   username.value,
      password:   password.value,
      firstName:  firstName.value,
      lastName:   lastName.value,
      dob:        dob.value,
      gender:     gender.value,
      lookingFor: lookingFor.value
    })

    success.value = true

    setTimeout(() => {
      router.push('/login')
    }, 1200)

  } catch (err) {

    error.value = err.response?.data?.error || 'Registration failed'
    console.log(err)

  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.signup-title {
  color: #5b5ff7;
  font-weight: bold;
}

.custom-input {
  height: 50px;
  border-radius: 10px;
}

.signup-btn {
  height: 50px;
  border-radius: 10px;
  font-weight: bold;
  font-size: 18px;
}
</style>