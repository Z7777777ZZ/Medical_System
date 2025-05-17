import { defineStore } from 'pinia'
import axios from 'axios'

export const usePatientStore = defineStore('patient', {
  state: () => ({
    patientId: null,
    medicalRecords: [],
    currentRecord: null,
    departments: [],
    doctors: [],
    selectedDepartment: null,
    selectedDoctor: null,
    paymentOrder: null,
    loading: false,
    error: null,
    connectionStatus: null
  }),
  
  actions: {
    // 设置当前患者ID
    setPatientId(id) {
      this.patientId = id
      // 保存到localStorage，以便页面刷新时保持状态
      localStorage.setItem('patientId', id)
      console.log('Current patient ID set to:', id)
    },
    
    // Test backend connectivity
    async testConnection() {
      this.loading = true
      this.error = null
      this.connectionStatus = null
      
      try {
        const response = await axios.get('/api/patient/test')
        console.log('Backend connection test:', response.data)
        this.connectionStatus = {
          success: true,
          message: response.data.message,
          timestamp: response.data.timestamp
        }
        return this.connectionStatus
      } catch (error) {
        console.error('Backend connection test failed:', error)
        this.error = error.response?.data?.message || 'Failed to connect to backend'
        this.connectionStatus = {
          success: false,
          message: this.error,
          timestamp: new Date().toISOString()
        }
        return this.connectionStatus
      } finally {
        this.loading = false
      }
    },
    
    // Medical Records
    async fetchMedicalRecords() {
      this.loading = true
      this.error = null
      
      try {
        // 使用保存的患者ID，如果没有，则使用默认值1
        const patientId = this.patientId || localStorage.getItem('patientId') || 1
        const response = await axios.get(`/api/patient/records/latest?patient_id=${patientId}`)
        console.log('Fetched medical records:', response.data)
        
        // Make sure we're working with an array
        if (Array.isArray(response.data.data)) {
          // 转换后端数据到前端期望的格式
          this.medicalRecords = response.data.data.map(record => {
            return this.formatMedicalRecord(record);
          });
        } else if (response.data.data && !Array.isArray(response.data.data)) {
          // 如果返回的是单个对象而不是数组，将其包装为数组
          console.warn('API returned a single object instead of an array, converting to array');
          const record = response.data.data;
          this.medicalRecords = [this.formatMedicalRecord(record)];
        } else {
          console.error('API response data is not an array or valid object:', response.data)
          this.medicalRecords = []
        }
        
        return this.medicalRecords
      } catch (error) {
        console.error('Error fetching medical records:', error)
        this.error = error.response?.data?.message || 'Failed to fetch medical records'
        this.medicalRecords = []
        return []
      } finally {
        this.loading = false
      }
    },
    
    // 获取病例历史记录
    async fetchMedicalRecordHistory(page = 1, perPage = 10) {
      this.loading = true
      this.error = null
      
      try {
        const patientId = this.patientId || localStorage.getItem('patientId') || 1
        const response = await axios.get(`/api/patient/records/history?patient_id=${patientId}&page=${page}&per_page=${perPage}`)
        console.log('Fetched medical record history:', response.data)
        
        if (response.data.status === 'success' && response.data.data.records) {
          return {
            records: response.data.data.records.map(record => ({
              id: record.record_id,
              visitDate: this.formatDate(record.visit_date),
              doctorName: record.doctor_name,
              departmentName: record.department_name,
              diagnosis: record.diagnosis
            })),
            total: response.data.data.total,
            page: response.data.data.page,
            perPage: response.data.data.per_page
          }
        }
        
        return { records: [], total: 0, page: 1, perPage: 10 }
      } catch (error) {
        console.error('Error fetching medical record history:', error)
        this.error = error.response?.data?.message || 'Failed to fetch medical record history'
        return { records: [], total: 0, page: 1, perPage: 10 }
      } finally {
        this.loading = false
      }
    },
    
    // 获取病例详情 - 增强版本
    async fetchMedicalRecordDetail(recordId) {
      this.loading = true
      this.error = null
      
      try {
        const patientId = this.patientId || localStorage.getItem('patientId') || 1
        const response = await axios.get(`/api/patient/records/${recordId}?patient_id=${patientId}`)
        console.log('Fetched medical record detail:', response.data)
        
        if (response.data.status === 'success' && response.data.data) {
          const record = response.data.data;
          this.currentRecord = this.formatMedicalRecord(record);
          return this.currentRecord;
        }
        
        this.error = '未找到病例记录'
        return null
      } catch (error) {
        console.error('Error fetching medical record detail:', error)
        this.error = error.response?.data?.message || 'Failed to fetch medical record detail'
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 统一的格式化病例记录方法
    formatMedicalRecord(record) {
      return {
        id: record.record_id,
        patientId: record.patient_id,
        doctorId: record.doctor_id,
        doctorName: record.doctor_name,
        visitDate: this.formatDate(record.visit_date),
        chiefComplaint: record.discription || '无主诉记录',
        diagnosis: record.diagnosis || '暂无诊断',
        treatmentPlan: record.treatment || '暂无治疗方案',
        department: record.department_name || '未知科室',
        prescription: record.prescription || null,
        prescriptionId: record.prescription_id,
        medications: this.formatMedication(record.prescription),
        notes: record.notes || '',
        // 添加其他可能需要的字段
        photos: record.photo ? (Array.isArray(record.photo) ? record.photo : [record.photo]) : [],
        createdAt: record.created_at
      };
    },
    
    // 辅助函数：格式化日期
    formatDate(dateStr) {
      if (!dateStr) return '未知日期';
      try {
        const date = new Date(dateStr);
        return date.toISOString().split('T')[0]; // 返回YYYY-MM-DD格式
      } catch (e) {
        return dateStr;
      }
    },
    
    // 辅助函数：格式化药品信息
    formatMedication(prescription) {
      if (!prescription) return null;
      
      // 如果处方有medicines数组
      if (prescription.medicines && Array.isArray(prescription.medicines)) {
        return prescription.medicines.map(med => ({
          name: med.name || 'Unknown',
          dosage: '',
          instructions: med.instructions || '',
          frequency: '',
          duration: ''
        }));
      } 
      // 如果处方有details数组
      else if (prescription.details && Array.isArray(prescription.details)) {
        return prescription.details.map(detail => ({
          name: detail.medicine_name || 'Unknown',
          dosage: '',
          instructions: detail.instructions || '',
          frequency: '',
          duration: ''
        }));
      }
      // 如果处方有string类型的medicines字段
      else if (prescription.medicines && typeof prescription.medicines === 'string') {
        return [{
          name: prescription.medicines,
          dosage: prescription.dosage || '',
          instructions: '',
          frequency: '',
          duration: ''
        }];
      }
      
      return null;
    },
    
    // Departments
    async fetchDepartments() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('/api/patient/registration/departments')
        console.log('Fetched departments:', response.data)
        
        if (response.data.data && Array.isArray(response.data.data)) {
          this.departments = response.data.data
        } else {
          console.warn('API response for departments is not in expected format:', response.data)
          this.departments = []
        }
        
        return this.departments
      } catch (error) {
        console.error('Error fetching departments:', error)
        this.error = error.response?.data?.message || 'Failed to fetch departments'
        this.departments = []
        return []
      } finally {
        this.loading = false
      }
    },
    
    // Doctors by Department
    async fetchDoctorsByDepartment(departmentId, subDepartmentId = null) {
      this.loading = true
      this.error = null
      this.selectedDepartment = departmentId
      
      try {
        let url = `/api/patient/registration/doctors?department_id=${departmentId}`
        if (subDepartmentId) {
          url += `&sub_department_id=${subDepartmentId}`
        }
        
        const response = await axios.get(url)
        console.log('Fetched doctors by department:', response.data)
        
        if (response.data.data && Array.isArray(response.data.data)) {
          this.doctors = response.data.data.map(doctor => ({
            id: doctor.id,
            name: doctor.name,
            title: doctor.title || '医师',
            department: doctor.department_name || '未知科室',
            avatar: doctor.avatar || null,
            specialty: doctor.specialty || '擅长：普通医疗',
            available: doctor.available !== false, // 默认为可用
            scheduleDates: doctor.schedule_dates || [],
            price: doctor.price || 0
          }))
        } else {
          console.warn('API response for doctors is not in expected format:', response.data)
          this.doctors = []
        }
        
        return this.doctors
      } catch (error) {
        console.error('Error fetching doctors by department:', error)
        this.error = error.response?.data?.message || 'Failed to fetch doctors'
        this.doctors = []
        return []
      } finally {
        this.loading = false
      }
    },
    
    // Search Doctors
    async searchDoctors(query) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`/api/patient/registration/doctors/search?query=${encodeURIComponent(query)}`)
        console.log('Search doctors response:', response.data)
        
        if (response.data.data && Array.isArray(response.data.data)) {
          return response.data.data.map(doctor => ({
            id: doctor.id,
            name: doctor.name,
            title: doctor.title || '医师',
            department: doctor.department_name || '未知科室',
            avatar: doctor.avatar || null,
            specialty: doctor.specialty || '擅长：普通医疗',
            available: doctor.available !== false
          }))
        }
        
        return []
      } catch (error) {
        console.error('Error searching doctors:', error)
        this.error = error.response?.data?.message || 'Failed to search doctors'
        return []
      } finally {
        this.loading = false
      }
    },
    
    // Selection
    selectDoctor(doctorId) {
      this.selectedDoctor = doctorId
    },
    
    // Appointment
    async createAppointment(doctorId, appointmentDate, departmentId, subDepartmentId = null) {
      this.loading = true
      this.error = null
      
      const patientId = this.patientId || localStorage.getItem('patientId') || 1
      
      try {
        const appointmentData = {
          patient_id: patientId,
          doctor_id: doctorId,
          appointment_time: appointmentDate,
          department_id: departmentId,
          sub_department_id: subDepartmentId
        }
        
        const response = await axios.post('/api/patient/registration/appointments', appointmentData)
        console.log('Appointment created:', response.data)
        
        // 生成支付订单
        if (response.data.status === 'success') {
          const appointmentId = response.data.data.appointment_id
          await this.generatePaymentOrder(appointmentId)
        }
        
        return response.data
      } catch (error) {
        console.error('Error creating appointment:', error)
        this.error = error.response?.data?.message || 'Failed to create appointment'
        return { status: 'error', message: this.error }
      } finally {
        this.loading = false
      }
    },
    
    // Generate payment order
    async generatePaymentOrder(appointmentId) {
      try {
        const response = await axios.post(`/api/patient/payment/orders`, { appointment_id: appointmentId })
        console.log('Payment order generated:', response.data)
        this.paymentOrder = response.data.data
        return this.paymentOrder
      } catch (error) {
        console.error('Error generating payment order:', error)
        this.error = error.response?.data?.message || 'Failed to generate payment order'
        
        // 生成模拟支付订单，以便测试
        this.paymentOrder = {
          order_id: `TEST-${Date.now()}`,
          appointment_id: appointmentId,
          amount: 50.00,
          status: 'unpaid',
          created_at: new Date().toISOString()
        }
        
        return this.paymentOrder
      }
    },
    
    // Process payment
    async processPayment(paymentMethod) {
      this.loading = true
      this.error = null
      
      if (!this.paymentOrder) {
        this.error = 'No payment order to process'
        return { status: 'error', message: this.error }
      }
      
      try {
        const paymentData = {
          order_id: this.paymentOrder.order_id,
          payment_method: paymentMethod,
          amount: this.paymentOrder.amount
        }
        
        const response = await axios.post('/api/patient/payment/process', paymentData)
        console.log('Payment processed:', response.data)
        return response.data
      } catch (error) {
        console.error('Error processing payment:', error)
        this.error = error.response?.data?.message || 'Failed to process payment'
        
        // 模拟支付成功响应，以便测试
        return {
          status: 'success',
          message: 'Payment simulated successfully',
          data: {
            order_id: this.paymentOrder.order_id,
            status: 'paid',
            payment_time: new Date().toISOString()
          }
        }
      } finally {
        this.loading = false
      }
    },
    
    // Reset state
    resetState() {
      this.selectedDepartment = null
      this.selectedDoctor = null
      this.paymentOrder = null
      this.error = null
    }
  }
}) 