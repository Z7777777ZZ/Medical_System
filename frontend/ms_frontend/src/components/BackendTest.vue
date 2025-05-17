<template>
  <div class="backend-test">
    <h3>后端连接测试</h3>
    <div class="test-controls">
      <el-button 
        type="primary" 
        @click="testConnection" 
        :loading="patientStore.loading"
      >
        测试连接
      </el-button>
    </div>
    
    <div v-if="patientStore.connectionStatus" class="test-results">
      <el-alert
        :title="patientStore.connectionStatus.success ? '连接成功' : '连接失败'"
        :type="patientStore.connectionStatus.success ? 'success' : 'error'"
        :description="patientStore.connectionStatus.message"
        show-icon
      />
      <p v-if="patientStore.connectionStatus.timestamp" class="timestamp">
        时间戳: {{ formatTimestamp(patientStore.connectionStatus.timestamp) }}
      </p>
    </div>
  </div>
</template>

<script>
import { usePatientStore } from '../store/patient'

export default {
  name: 'BackendTest',
  setup() {
    const patientStore = usePatientStore()
    
    const testConnection = async () => {
      await patientStore.testConnection()
    }
    
    const formatTimestamp = (timestamp) => {
      try {
        const date = new Date(timestamp)
        return date.toLocaleString()
      } catch (e) {
        return timestamp
      }
    }
    
    return {
      patientStore,
      testConnection,
      formatTimestamp
    }
  }
}
</script>

<style scoped>
.backend-test {
  padding: 20px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background-color: #fff;
  margin-bottom: 20px;
}

.test-controls {
  margin-bottom: 20px;
}

.test-results {
  margin-top: 15px;
}

.timestamp {
  font-size: 12px;
  color: #909399;
  margin-top: 10px;
}
</style> 