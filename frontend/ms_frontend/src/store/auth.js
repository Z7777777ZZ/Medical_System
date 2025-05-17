import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    userType: localStorage.getItem('userType') || null, // 'patient' or 'doctor'
    patientId: localStorage.getItem('patientId') || null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    isPatient: (state) => state.userType === 'patient',
    isDoctor: (state) => state.userType === 'doctor',
    currentUser: (state) => state.user
  },
  
  actions: {
    async login(credentials) {
      try {
        const response = await axios.post('/patient/auth/login', credentials)
        this.setUserData(response.data)
        return { success: true }
      } catch (error) {
        console.error('Login failed:', error)
        return { 
          success: false, 
          message: error.response?.data?.message || 'Login failed'
        }
      }
    },
    
    setUserData(data) {
      this.token = data.token
      this.user = data.user
      this.userType = data.userType
      
      // Store auth data in localStorage
      localStorage.setItem('token', data.token)
      localStorage.setItem('userType', data.userType)
      
      // 存储患者ID（如果适用）
      if (data.patientId) {
        localStorage.setItem('patientId', data.patientId)
      }
      
      // Set Authorization header for all future requests
      axios.defaults.headers.common['Authorization'] = `Bearer ${data.token}`
    },
    
    logout() {
      this.user = null
      this.token = null
      this.userType = null
      this.patientId = null
      
      // Clear local storage
      localStorage.removeItem('token')
      localStorage.removeItem('userType')
      localStorage.removeItem('patientId')
      
      // Remove Authorization header
      delete axios.defaults.headers.common['Authorization']
    }
  }
}) 