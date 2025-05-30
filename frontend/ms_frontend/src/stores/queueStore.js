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
    async initData(userType, userId) {
      console.log('初始化队列数据:', userType, userId)
      this.loading = true
      try {
        // 先获取队列数据
        await this.fetchQueueData(userType, userId)
        // 再获取当前患者信息
        // await this.fetchCurrentPatient(userType, userId)
        console.log('队列数据已初始化完成')
      } catch (error) {
        console.error('初始化队列数据失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 获取队列数据
    async fetchQueueData(userType, userId) {
      console.log('开始获取队列数据...' + userType + ' ' + userId)
      this.loading = true
      try {
        if (!userType || !userId) {
          console.error('获取队列数据缺少必要参数:', { userType, userId })
          throw new Error('缺少必要参数')
        }

        const response = await fetch(`${BASE_API_URL}/api/call-number/queue/list?type=${userType}&id=${userId}`)
        if (!response.ok) {
          console.error('队列数据获取失败:', response.status, response.statusText)
          throw new Error(`获取队列数据失败: ${response.status}`)
        }
        
        const queueData0 = await response.json()
        console.log('获取队列数据原始数据:', queueData0)
        const queueData = Array.isArray(queueData0) ? queueData0.filter(p => p.status === 'waiting') : []
        console.log('过滤后的队列数据:', queueData)

        this.normalQueue = queueData.filter(p => !p.priority) // 注意：API 可能返回的是 priority 而不是 isPriority
        this.priorityQueue = queueData.filter(p => p.priority) // 使用 priority 字段进行过滤
        
        console.log('普通队列:', this.normalQueue)
        console.log('优先队列:', this.priorityQueue)
      } catch (error) {
        console.error('获取队列数据出错:', error)
        this.error = error.message
        // 清空队列，避免显示旧数据
        this.normalQueue = []
        this.priorityQueue = []
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

    async fetchCurrentPatient(userType, userId) {
      try {
        const response = await fetch(`${BASE_API_URL}/api/call-number/queue/current?type=${userType}&id=${userId}`)
        if (!response.ok) {
          throw new Error('获取当前患者失败')
        }
        const patient = await response.json()
        console.log('当前患者:', patient)
        if (patient && patient.status === 'waiting') {
          this.currentPatient = patient
        } else {
          this.currentPatient = null
        }
      } catch (error) {
        this.error = error.message
      }
    },
    
    // 患者检查完毕，重新加入队列
    // 由患者使用
    async returnToQueueAfterExam(patientId, doctorId) {
      this.loading = true
      
      try {
        if (!patientId || !doctorId) {
          throw new Error('患者ID和医生ID不能为空');
        }
        
        // 调用API更新患者优先级
        const response = await fetch(`${BASE_API_URL}/api/call-number/queue/update-priority`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            patientId: patientId,
            doctorId: doctorId,
            priority: true,
            examResult: '检查已完成'
          })
        });
        
        if (!response.ok) {
          throw new Error('更新患者优先级失败');
        }
        
        const updatedPatient = await response.json();
        console.log('患者优先级更新成功:', updatedPatient);
        
        await this.fetchQueueData('doctor', doctorId);
      } catch (error) {
        console.error('患者返回队列失败:', error);
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },
    
    // 结束当前患者诊断
    async finishDiagnosis() {
      this.loading = true
      // 清空当前患者
      this.currentPatient = null
      
      this.loading = false
    },
    
    // 调用特定患者
    async callSpecificPatient(doctorId, patientId) {
      if (!doctorId || !patientId) {
        throw new Error('医生ID和患者ID都是必需的');
      }
      
      this.loading = true;
      try {
        // 调用叫号API，指定医生ID和患者ID
        const response = await fetch(`${BASE_API_URL}/api/call-number/queue/call`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            doctorId: doctorId,
            patientId: patientId
          })
        });
        
        if (!response.ok) {
          throw new Error('叫号失败');
        }
        
        // 获取API返回的患者信息
        const patient = await response.json();
        console.log('叫特定患者:', patient);
        
        // 更新当前患者
        if (patient) {
          this.currentPatient = patient;
          
          // 重新获取最新的队列数据
          await this.fetchQueueData('doctor', doctorId);
        }
        
        return patient;
      } catch (error) {
        console.error('叫特定患者失败:', error);
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },
  }
})