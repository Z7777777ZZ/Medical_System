import { defineStore } from 'pinia'

export const useQueueStore = defineStore('queue', {
  state: () => ({
    // 普通患者等待队列
    normalQueue: [
      { id: 101, name: '张三', age: 45, gender: '男', symptom: '头痛、发热', waitingTime: 30 },
      { id: 102, name: '李四', age: 28, gender: '女', symptom: '咳嗽、喉咙疼', waitingTime: 25 },
      { id: 103, name: '王五', age: 62, gender: '男', symptom: '腹痛、恶心', waitingTime: 15 },
      { id: 104, name: '赵六', age: 35, gender: '女', symptom: '过敏、皮疹', waitingTime: 10 }
    ],
    // 检查后优先队列
    priorityQueue: [
      { id: 201, name: '陈七', age: 72, gender: '男', symptom: '心悸、胸闷', waitingTime: 40, examResult: 'ECG显示轻度心率不齐' },
      { id: 202, name: '刘八', age: 8, gender: '男', symptom: '发热、全身酸痛', waitingTime: 35, examResult: '血检显示白细胞升高' }
    ],
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
    initData() {
      console.log('队列数据已初始化')
    },
    
    // 获取队列数据
    async fetchQueueData() {
      // 模拟加载过程
      this.loading = true
      setTimeout(() => {
        this.loading = false
      }, 500)
    },
    
    // 医生叫号接诊
    async callNextPatient() {
      if (!this.nextPatient) {
        return null
      }
      
      this.loading = true
      // 模拟API调用延迟
      await new Promise(resolve => setTimeout(resolve, 500))
      
      let patient = null
      
      // 从优先队列或普通队列中取出第一个患者
      if (this.priorityQueue.length > 0) {
        patient = { ...this.priorityQueue[0] }
        this.priorityQueue = this.priorityQueue.slice(1)
      } else if (this.normalQueue.length > 0) {
        patient = { ...this.normalQueue[0] }
        this.normalQueue = this.normalQueue.slice(1)
      }
      
      if (patient) {
        this.currentPatient = patient
      }
      
      this.loading = false
      return patient
    },
    
    // 患者检查完毕，重新加入队列
    async returnToQueueAfterExam(patient) {
      this.loading = true
      // 模拟API调用延迟
      await new Promise(resolve => setTimeout(resolve, 500))
      
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
      // 模拟API调用延迟
      await new Promise(resolve => setTimeout(resolve, 500))
      
      // 清空当前患者
      this.currentPatient = null
      
      this.loading = false
    }
  }
})