import { defineStore } from 'pinia'
// 移除 axios 导入
// import axios from 'axios'

// 静态药物数据
const staticMedicines = [
  { id: 1, name: '阿莫西林胶囊', specification: '0.25g*24粒', price: 24.5, stock: 100 },
  { id: 2, name: '布洛芬缓释胶囊', specification: '0.3g*10粒', price: 16.8, stock: 150 },
  { id: 3, name: '头孢克肟胶囊', specification: '100mg*6片', price: 38.5, stock: 80 },
  { id: 4, name: '感冒灵颗粒', specification: '10g*9袋', price: 12.5, stock: 200 },
  { id: 5, name: '维生素C片', specification: '100mg*60片', price: 8.5, stock: 300 }
]

// 静态处方数据
const staticPrescriptions = [
  {
    id: 1,
    patientId: 101,
    doctorId: 201,
    date: '2025-04-20T08:30:00',
    medicines: [
      { id: 1, name: '阿莫西林胶囊', specification: '0.25g*24粒', price: 24.5, quantity: 2, usage: '一日三次，饭后服用' },
      { id: 4, name: '感冒灵颗粒', specification: '10g*9袋', price: 12.5, quantity: 1, usage: '一日三次，温水冲服' }
    ],
    instructions: '多喝水，注意休息',
    status: 'completed'
  },
  {
    id: 2,
    patientId: 102,
    doctorId: 201,
    date: '2025-04-21T10:15:00',
    medicines: [
      { id: 2, name: '布洛芬缓释胶囊', specification: '0.3g*10粒', price: 16.8, quantity: 1, usage: '发热时服用，一次一粒，间隔6小时' },
      { id: 5, name: '维生素C片', specification: '100mg*60片', price: 8.5, quantity: 1, usage: '一日一次，饭后服用' }
    ],
    instructions: '避免剧烈运动，多休息',
    status: 'completed'
  }
]

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
        // 使用静态数据替代 API 调用
        setTimeout(() => {
          this.availableMedicines = staticMedicines
          this.loading = false
        }, 300) // 添加小延迟模拟网络请求
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
      if (!this.currentPrescription) return
      
      try {
        this.loading = true
        // 使用静态数据模拟 API 响应
        return new Promise((resolve) => {
          setTimeout(() => {
            const savedPrescription = {
              ...this.currentPrescription,
              id: Math.floor(Math.random() * 1000) + 10, // 随机生成 ID
              status: 'completed'
            }
            // 添加到静态处方列表中
            staticPrescriptions.push(savedPrescription)
            this.currentPrescription = savedPrescription
            this.loading = false
            resolve(savedPrescription)
          }, 500)
        })
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
        // 使用静态数据模拟 API 响应
        return new Promise((resolve) => {
          setTimeout(() => {
            this.patientPrescriptions = staticPrescriptions.filter(p => p.patientId === patientId)
            this.loading = false
            resolve(this.patientPrescriptions)
          }, 300)
        })
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
        // 使用静态数据模拟 API 响应
        return new Promise((resolve) => {
          setTimeout(() => {
            const prescription = staticPrescriptions.find(p => p.id === prescriptionId)
            this.currentPrescription = prescription || null
            this.loading = false
            resolve(prescription)
          }, 300)
        })
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