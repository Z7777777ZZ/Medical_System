import { defineStore } from 'pinia'
import axios from 'axios'

export const usePrescriptionStore = defineStore('prescription', {
  state: () => ({
    // 当前正在编辑的处方
    currentPrescription: null,
    // 患者的历史处方列表
    patientPrescriptions: [],
    // 可用药物列表
    availableMedicines: [],
    // 加载状态
    loading: false,
    // 错误信息
    error: null
  }),
  
  getters: {
    hasPrescription() {
      return this.currentPrescription !== null
    }
  },
  
  actions: {
    // 获取可用药物列表
    async fetchAvailableMedicines() {
      try {
        this.loading = true
        this.error = null
        const token = localStorage.getItem('token');
        
        // 调用实际 API 获取药物列表
        const response = await axios.get('/diagnosis/prescription/medicines', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        this.availableMedicines = response.data || []
        
        this.loading = false
      } catch (error) {
        this.error = '获取药物列表失败'
        this.loading = false
        console.error('获取药物列表失败:', error)
      }
    },
    
    // 创建新处方
    createNewPrescription(patientId, doctorId) {
      this.currentPrescription = {
        patientId,
        doctorId,
        date: new Date().toISOString(),
        medicines: [],
        instructions: '',
        status: 'draft' // 草稿状态
      }
    },
    
    // 向处方添加药物
    addMedicineToPrescription(medicine) {
      if (!this.currentPrescription) return
      
      // 检查药物是否已在处方中，如果存在则增加数量
      const existingMedicine = this.currentPrescription.medicines.find(m => m.id === medicine.id)
      if (existingMedicine) {
        existingMedicine.quantity += 1
      } else {
        this.currentPrescription.medicines.push({
          ...medicine,
          quantity: 1,
          usage: '' // 用药说明默认为空
        })
      }
    },
    
    // 从处方中移除药物
    removeMedicineFromPrescription(medicineId) {
      if (!this.currentPrescription) return
      
      this.currentPrescription.medicines = this.currentPrescription.medicines.filter(
        medicine => medicine.id !== medicineId
      )
    },
    
    // 更新药物数量
    updateMedicineQuantity(medicineId, quantity) {
      if (!this.currentPrescription) return
      
      const medicine = this.currentPrescription.medicines.find(m => m.id === medicineId)
      if (medicine) {
        medicine.quantity = quantity
      }
    },
    
    // 更新药物用法说明
    updateMedicineUsage(medicineId, usage) {
      if (!this.currentPrescription) return
      
      const medicine = this.currentPrescription.medicines.find(m => m.id === medicineId)
      if (medicine) {
        medicine.usage = usage
      }
    },
    
    // 更新处方整体说明
    updateInstructions(instructions) {
      if (!this.currentPrescription) return
      
      this.currentPrescription.instructions = instructions
    },
    
    // 保存处方
    async savePrescription() {
      if (!this.currentPrescription) return null
      
      try {
        this.loading = true
        this.error = null
        const token = localStorage.getItem('token');
        
        // 判断是创建新处方还是更新已有处方
        let response
        if (this.currentPrescription.id) {
          // 更新已有处方
          response = await axios.put(
            `/diagnosis/prescription/${this.currentPrescription.id}`, 
            {
              ...this.currentPrescription,
              status: 'completed'
            },
            {
              headers: {
                'Authorization': `Bearer ${token}`
              }
            }
          )
        } else {
          // 创建新处方
          response = await axios.post(
            '/diagnosis/prescription', 
            {
              ...this.currentPrescription,
              status: 'completed'
            },
            {
              headers: {
                'Authorization': `Bearer ${token}`
              }
            }
          )
        }
        
        if (response.data) {
          this.currentPrescription = response.data
        }
        
        this.loading = false
        return response.data
      } catch (error) {
        this.error = '保存处方失败'
        this.loading = false
        console.error('保存处方失败:', error)
        return null
      }
    },
    
    // 获取患者的处方列表
    async fetchPatientPrescriptions(patientId) {
      try {
        this.loading = true
        this.error = null
        const token = localStorage.getItem('token');
        
        // 调用实际 API 获取患者处方列表
        const response = await axios.get(`/diagnosis/prescription?patientId=${patientId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        this.patientPrescriptions = response.data || []
        
        this.loading = false
        return this.patientPrescriptions
      } catch (error) {
        this.error = '获取处方列表失败'
        this.loading = false
        console.error('获取处方列表失败:', error)
        return []
      }
    },
    
    // 获取处方详情
    async fetchPrescription(prescriptionId) {
      try {
        this.loading = true
        this.error = null
        const token = localStorage.getItem('token');
        
        // 调用实际 API 获取处方详情
        const response = await axios.get(`/diagnosis/prescription/${prescriptionId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        
        if (response.data) {
          this.currentPrescription = response.data
        } else {
          this.currentPrescription = null
        }
        
        this.loading = false
        return this.currentPrescription
      } catch (error) {
        this.error = '获取处方详情失败'
        this.loading = false
        console.error('获取处方详情失败:', error)
        return null
      }
    },
    
    // 清除当前处方
    clearCurrentPrescription() {
      this.currentPrescription = null
    }
  }
})