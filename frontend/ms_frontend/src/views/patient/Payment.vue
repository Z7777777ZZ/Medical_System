<template>
  <div class="page-container">
    <div class="page-header">
      <h2>在线缴费</h2>
    </div>
    
    <div v-if="!paymentOrder" class="empty-section">
      <el-empty description="当前没有待支付订单">
        <template #description>
          <div>
            <p>当前没有待支付订单</p>
            <p class="small">您可以通过预约挂号生成待支付订单</p>
          </div>
        </template>
        <el-button type="primary" @click="$router.push('/patient/appointment')">去预约挂号</el-button>
      </el-empty>
    </div>
    
    <div v-else class="payment-container">
      <el-card class="payment-card">
        <template #header>
          <div class="card-header">
            <h3>订单信息</h3>
            <el-tag>待支付</el-tag>
          </div>
        </template>
        
        <div class="order-details">
          <div class="detail-row">
            <span class="detail-label">订单编号:</span>
            <span class="detail-value">{{ paymentOrder.id }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">预约科室:</span>
            <span class="detail-value">{{ paymentOrder.departmentName }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">就诊医生:</span>
            <span class="detail-value">{{ paymentOrder.doctorName }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">就诊时间:</span>
            <span class="detail-value">{{ formatDateTime(paymentOrder.appointmentTime) }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">挂号费用:</span>
            <span class="detail-value price">¥{{ paymentOrder.amount.toFixed(2) }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">下单时间:</span>
            <span class="detail-value">{{ formatDateTime(paymentOrder.createdAt) }}</span>
          </div>
        </div>
        
        <el-divider content-position="center">支付方式</el-divider>
        
        <div class="payment-methods">
          <el-radio-group v-model="selectedPaymentMethod">
            <div class="payment-method-list">
              <div class="payment-method-item">
                <el-radio label="alipay">
                  <div class="payment-method-content">
                    <img src="https://www.alipay.com/favicon.ico" alt="支付宝" class="payment-icon" />
                    <div class="payment-method-info">
                      <span class="method-name">支付宝</span>
                      <span class="method-desc">推荐使用支付宝快捷支付</span>
                    </div>
                  </div>
                </el-radio>
              </div>
              
              <div class="payment-method-item">
                <el-radio label="wechat">
                  <div class="payment-method-content">
                    <img src="https://res.wx.qq.com/a/wx_fed/assets/res/NTI4MWU5.ico" alt="微信支付" class="payment-icon" />
                    <div class="payment-method-info">
                      <span class="method-name">微信支付</span>
                      <span class="method-desc">推荐使用微信扫码支付</span>
                    </div>
                  </div>
                </el-radio>
              </div>
              
              <div class="payment-method-item">
                <el-radio label="unionpay">
                  <div class="payment-method-content">
                    <img src="https://www.unionpayintl.com/profiles/unionpay2/themes/unionpay/images/favicon.ico" alt="银联" class="payment-icon" />
                    <div class="payment-method-info">
                      <span class="method-name">银联支付</span>
                      <span class="method-desc">银联卡扫码支付</span>
                    </div>
                  </div>
                </el-radio>
              </div>
            </div>
          </el-radio-group>
        </div>
        
        <div class="payment-actions">
          <div class="total-container">
            <span>待支付：</span>
            <span class="total-price">¥{{ paymentOrder.amount.toFixed(2) }}</span>
          </div>
          <el-button 
            type="primary" 
            :disabled="!selectedPaymentMethod"
            @click="processPayment"
            :loading="loading"
            size="large"
          >
            立即支付
          </el-button>
        </div>
      </el-card>
      
      <el-card class="notice-card">
        <h4>支付须知</h4>
        <ul class="notice-list">
          <li>支付成功后，系统会自动为您生成挂号凭证</li>
          <li>请在就诊当天提前30分钟到达医院</li>
          <li>凭借预约号和本人身份证件到医院取号</li>
          <li>如需退费，请按照医院规定办理相关手续</li>
        </ul>
      </el-card>
    </div>
    
    <!-- Payment success dialog -->
    <el-dialog
      v-model="paymentSuccess"
      title="支付成功"
      width="400px"
      :show-close="false"
      center
    >
      <div class="success-content">
        <el-icon :size="64" color="#67C23A" class="success-icon"><CircleCheck /></el-icon>
        <h3>支付成功！</h3>
        <p>您的挂号已完成，请按时前往医院就诊</p>
        <p class="success-code">挂号凭证号：{{ successData.receiptNumber }}</p>
      </div>
      <template #footer>
        <div class="success-footer">
          <el-button @click="$router.push('/patient/medical-records')">查看我的病历</el-button>
          <el-button type="primary" @click="goHome">返回首页</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { usePatientStore } from '../../store/patient'
import { CircleCheck } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'PaymentPage',
  components: {
    CircleCheck
  },
  setup() {
    const router = useRouter()
    const patientStore = usePatientStore()
    
    const loading = ref(false)
    const selectedPaymentMethod = ref('')
    const paymentSuccess = ref(false)
    const successData = ref({
      receiptNumber: '',
      paymentTime: ''
    })
    
    // Get payment order from store
    const paymentOrder = computed(() => patientStore.paymentOrder)
    
    // Format date and time
    const formatDateTime = (timestamp) => {
      if (!timestamp) return ''
      
      const date = new Date(timestamp)
      const year = date.getFullYear()
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      const day = date.getDate().toString().padStart(2, '0')
      const hours = date.getHours().toString().padStart(2, '0')
      const minutes = date.getMinutes().toString().padStart(2, '0')
      
      return `${year}-${month}-${day} ${hours}:${minutes}`
    }
    
    // Process payment
    const processPayment = async () => {
      if (!selectedPaymentMethod.value) {
        ElMessage.warning('请选择支付方式')
        return
      }
      
      // Confirm payment
      try {
        const confirmed = await ElMessageBox.confirm(
          `确认使用${getPaymentMethodName(selectedPaymentMethod.value)}支付${paymentOrder.value.amount.toFixed(2)}元？`,
          '确认支付',
          {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'info'
          }
        ).then(() => true)
          .catch(() => false)
        
        if (!confirmed) return
      } catch (error) {
        return
      }
      
      loading.value = true
      
      try {
        // In a real app, this would integrate with actual payment APIs
        const result = await patientStore.processPayment(selectedPaymentMethod.value)
        
        if (result.success) {
          // Show success message
          successData.value = {
            receiptNumber: result.data.receiptNumber || generateReceiptNumber(),
            paymentTime: new Date().toISOString()
          }
          paymentSuccess.value = true
        } else {
          ElMessage.error(result.error || '支付失败，请重试')
        }
      } catch (error) {
        ElMessage.error('系统错误，请稍后重试')
        console.error(error)
      } finally {
        loading.value = false
      }
    }
    
    // Get payment method name
    const getPaymentMethodName = (method) => {
      const methods = {
        'alipay': '支付宝',
        'wechat': '微信支付',
        'unionpay': '银联支付'
      }
      return methods[method] || method
    }
    
    // Generate mock receipt number
    const generateReceiptNumber = () => {
      const prefix = 'REC'
      const timestamp = Date.now().toString().slice(-8)
      const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0')
      return `${prefix}${timestamp}${random}`
    }
    
    // Navigate home after payment
    const goHome = () => {
      paymentSuccess.value = false
      router.push('/patient/medical-records')
    }
    
    return {
      loading,
      paymentOrder,
      selectedPaymentMethod,
      paymentSuccess,
      successData,
      processPayment,
      formatDateTime,
      goHome
    }
  }
}
</script>

<style scoped>
.empty-section {
  margin: 60px 0;
  text-align: center;
}

.small {
  font-size: 13px;
  color: #909399;
}

.payment-container {
  display: grid;
  grid-template-columns: 3fr 1fr;
  gap: 20px;
}

@media (max-width: 768px) {
  .payment-container {
    grid-template-columns: 1fr;
  }
}

.payment-card,
.notice-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
}

.order-details {
  margin: 20px 0;
}

.detail-row {
  display: flex;
  margin-bottom: 15px;
}

.detail-label {
  width: 100px;
  color: #909399;
}

.detail-value {
  font-weight: 500;
}

.detail-value.price {
  color: #F56C6C;
  font-weight: bold;
}

.payment-methods {
  margin: 20px 0;
}

.payment-method-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.payment-method-item {
  border: 1px solid #EBEEF5;
  border-radius: 4px;
  padding: 10px;
  transition: all 0.3s;
}

.payment-method-item:hover {
  border-color: #C0C4CC;
  background-color: #f5f7fa;
}

.payment-method-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.payment-icon {
  width: 32px;
  height: 32px;
  object-fit: contain;
}

.payment-method-info {
  display: flex;
  flex-direction: column;
}

.method-name {
  font-weight: 500;
}

.method-desc {
  font-size: 12px;
  color: #909399;
}

.payment-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
}

.total-container {
  font-size: 14px;
}

.total-price {
  font-size: 24px;
  color: #F56C6C;
  font-weight: bold;
}

.notice-card h4 {
  margin-top: 0;
  margin-bottom: 15px;
}

.notice-list {
  padding-left: 20px;
}

.notice-list li {
  margin-bottom: 10px;
  color: #606266;
}

.success-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.success-icon {
  margin-bottom: 15px;
}

.success-content h3 {
  margin: 0 0 10px 0;
  color: #67C23A;
}

.success-content p {
  margin: 5px 0;
  color: #606266;
}

.success-code {
  margin-top: 15px;
  padding: 10px 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-family: monospace;
  font-size: 16px;
}

.success-footer {
  display: flex;
  justify-content: center;
  gap: 15px;
}
</style> 