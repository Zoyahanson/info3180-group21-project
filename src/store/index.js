import { createStore } from 'vuex'

const savedUser = localStorage.getItem('user')

export default createStore({

  state: {
    darkMode: false,
    user: savedUser ? JSON.parse(savedUser) : null
  },

  mutations: {

    toggleDarkMode(state) {
      state.darkMode = !state.darkMode
    },

    setUser(state, user) {
      state.user = user
      localStorage.setItem('user', JSON.stringify(user))
    },

    logout(state) {
      state.user = null
      localStorage.removeItem('user')
    }

  }

})