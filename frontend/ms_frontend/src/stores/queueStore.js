import { defineStore } from 'pinia'
const BASE_API_URL = 'http://127.0.0.1:5000'
export const useQueueStore = defineStore('queue', {
  state: () => ({
    // 普通患者等待队列
    normalQueue: [],
    // 检查后优先队列
    priorityQueue: [],
    // 当前接诊的患者
    currentPatient: null,
    // 加载状态
    loading: false,
    // 错误信息
    error: null
  }),
  
  getters: {
    // 所有等待患者
    allPatients() {
      return [...this.priorityQueue, ...this.normalQueue]
    },
    
    // 队列长度
    queueLength() {
      return this.normalQueue.length + this.priorityQueue.length
    },
    
    // 下一个患者
    nextPatient() {
      return this.priorityQueue.length > 0 ? this.priorityQueue[0] : 
             (this.normalQueue.length > 0 ? this.normalQueue[0] : null)
    }
  },
  
  actions: {
    // 初始化数据 - 用于组件挂载时调用
    async initData() {
      await this.fetchQueueData()
      await this.fetchCurrentPatient()
      console.log('队列数据已初始化')
    },
    
    // 获取队列数据
    async fetchQueueData() {
      this.loading = true
      try {
        const response = await fetch(`${BASE_API_URL}/api/call-number/queue/list`)
        const queueData0 = await response.json()
        // console.log('获取队列数据0:', queueData0)
        const queueData = queueData0.filter(p => p.status === 'waiting')

        // console.log('获取队列数据:', queueData)

        this.normalQueue = queueData.filter(p => !p.isPriority)
        this.priorityQueue = queueData.filter(p => p.isPriority)
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    
    // 医生叫号接诊
    async callNextPatient(doctorId) {
      if (!this.nextPatient) {
        return null
      }
      
      this.loading = true
      let patient = null
      
      try {
        // 调用叫号API
        console.log('开始叫号...')
        const response = await fetch(`${BASE_API_URL}/api/call-number/queue/call`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            doctorId: doctorId,
          })
        })
        
        if (!response.ok) {
          throw new Error('叫号失败')
        }
        
        // 获取API返回的下一个患者
        patient = await response.json()
        
        // 将该患者设为当前患者
        if (patient) {
          this.currentPatient = patient
          
          // 更新队列数据，从队列中移除该患者
          await this.fetchQueueData() // 重新获取最新的队列数据
        }
      } catch (error) {
        console.error('叫号失败:', error)
        this.error = error.message
      } finally {
        this.loading = false
      }
      return patient
    },

    async fetchCurrentPatient() {
      try {
        const response = await fetch(`${BASE_API_URL}/api/call-number/queue/current`)
        this.currentPatient = await response.json()
      } catch (error) {
        this.error = error.message
      }
    },
    
    // 患者检查完毕，重新加入队列
    async returnToQueueAfterExam(patient) {
      this.loading = true
      
      if (patient) {
        // 添加检查结果
        const patientWithExam = { 
          ...patient, 
          examResult: '检查已完成',
          waitingTime: Math.floor(Math.random() * 10) + 5 
        }
        
        // 加入优先队列
        this.priorityQueue = [...this.priorityQueue, patientWithExam]
      }
      
      this.loading = false
    },
    
    // 结束当前患者诊断
    async finishDiagnosis() {
      this.loading = true
      // 清空当前患者
      this.currentPatient = null
      
      this.loading = false
    }
  }
})