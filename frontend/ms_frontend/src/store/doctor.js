import { defineStore } from 'pinia'
import axios from 'axios'

export const useDoctorStore = defineStore('doctor', {
  state: () => ({
    doctorId: null,
    patients: [],
    currentPatient: null,
    currentMedicalRecord: null,
    loading: false,
    error: null
  }),
  
  actions: {
    // 设置当前医生ID
    setDoctorId(id) {
      this.doctorId = id
      // 保存到localStorage，以便页面刷新时保持状态
      localStorage.setItem('doctorId', id)
      console.log('Current doctor ID set to:', id)
    },
    
    // Get patients assigned to doctor
    async fetchMyPatients() {
      this.loading = true
      this.error = null
      
      try {
        // 使用保存的医生ID，如果没有，则从localStorage获取
        const doctorId = this.doctorId || localStorage.getItem('doctorId')
        const response = await axios.get(`/patient/doctor/patients?doctor_id=${doctorId}`)
        this.patients = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch patients'
        return []
      } finally {
        this.loading = false
      }
    },
    
    // Get patient details
    async getPatientDetails(patientId) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`/patient/doctor/patients/${patientId}`)
        this.currentPatient = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch patient details'
        return null
      } finally {
        this.loading = false
      }
    },
    
    // Get patient's medical record
    async getPatientMedicalRecord(patientId, recordId) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`/patient/doctor/patients/${patientId}/records/${recordId}`)
        this.currentMedicalRecord = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch medical record'
        return null
      } finally {
        this.loading = false
      }
    },
    
    // Update medical record
    async updateMedicalRecord(patientId, recordId, recordData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.put(
          `/patient/doctor/patients/${patientId}/records/${recordId}`, 
          recordData
        )
        this.currentMedicalRecord = response.data
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update medical record'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // Create new medical record
    async createMedicalRecord(patientId, recordData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post(
          `/patient/doctor/patients/${patientId}/records`, 
          recordData
        )
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to create medical record'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // Reset state
    resetState() {
      this.currentPatient = null
      this.currentMedicalRecord = null
      this.error = null
    }
  }
}) 