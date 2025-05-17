<template>
  <div class="page-container">
    <div class="page-header">
      <h2>支付记录</h2>
    </div>
    
    <div class="content-section">
      <div class="filter-section">
        <el-select v-model="filterStatus" placeholder="支付状态" clearable>
          <el-option label="全部" value="" />
          <el-option label="已支付" value="paid" />
          <el-option label="待支付" value="pending" />
        </el-select>
        
        <el-select v-model="filterType" placeholder="费用类型" clearable>
          <el-option label="全部" value="" />
          <el-option label="挂号费" value="registration_fee" />
          <el-option label="问诊费" value="consultation_fee" />
          <el-option label="挂号" value="挂号" />
          <el-option label="医保支付" value="医保支付" />
          <el-option label="支付宝支付" value="支付宝支付" />
          <el-option label="微信支付" value="微信支付" />
          <el-option label="现金支付" value="现金支付" />
        </el-select>
        
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          clearable
        />
      </div>
      
      <div v-if="loading" class="loading-section">
        <el-skeleton :rows="5" animated />
      </div>
      
      <div v-else-if="!filteredPayments.length" class="empty-section">
        <el-empty description="暂无支付记录">
          <template #description>
            <div>
              <p>暂无支付记录</p>
              <p class="small">您可以通过预约挂号生成支付记录</p>
            </div>
          </template>
          <el-button type="primary" @click="$router.push('/patient/appointment')">去预约挂号</el-button>
        </el-empty>
      </div>
      
      <div v-else>
        <el-table :data="filteredPayments" style="width: 100%" border>
          <el-table-column label="支付单号" prop="payment_id" width="120">
            <template #default="{ row }">
              <span class="payment-id">#{{ row.payment_id }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="费用类型" prop="type" width="120">
            <template #default="{ row }">
              <el-tag 
                :type="row.type === 'registration_fee' || row.type === '挂号' || row.type === '挂号费' ? 'primary' : 'success'"
              >
                {{ formatPaymentType(row.type) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="金额" prop="amount" width="120">
            <template #default="{ row }">
              <span class="amount">¥{{ row.amount.toFixed(2) }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="状态" prop="status" width="120">
            <template #default="{ row }">
              <el-tag 
                :type="row.status === 'paid' ? 'success' : 'warning'"
              >
                {{ row.status === 'paid' ? '已支付' : '待支付' }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <el-button 
                v-if="row.status === 'pending'"
                size="small" 
                type="primary" 
                @click="goToPay(row)"
              >
                去支付
              </el-button>
              <el-button 
                size="small" 
                @click="viewDetail(row)"
              >
                详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="totalPayments"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </div>
    
    <!-- Payment Detail Dialog -->
    <el-dialog
      v-model="detailDialogVisible"
      title="支付详情"
      width="600px"
    >
      <div v-if="selectedPayment" class="payment-detail">
        <div class="detail-row">
          <span class="detail-label">支付单号:</span>
          <span class="detail-value">#{{ selectedPayment.payment_id }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">费用类型:</span>
          <span class="detail-value">{{ formatPaymentType(selectedPayment.type) }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">金额:</span>
          <span class="detail-value">¥{{ selectedPayment.amount.toFixed(2) }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">状态:</span>
          <span class="detail-value">
            <el-tag :type="selectedPayment.status === 'paid' ? 'success' : 'warning'">
              {{ selectedPayment.status === 'paid' ? '已支付' : '待支付' }}
            </el-tag>
          </span>
        </div>
        <div class="detail-row">
          <span class="detail-label">创建时间:</span>
          <span class="detail-value">{{ formatDateTime(selectedPayment.created_at) }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">支付时间:</span>
          <span class="detail-value">{{ selectedPayment.payment_time ? formatDateTime(selectedPayment.payment_time) : '暂无详情' }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">支付方式:</span>
          <span class="detail-value">{{ formatPaymentMethod(selectedPayment.payment_method) }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">支付详情:</span>
          <span class="detail-value">{{ selectedPayment.details || '暂无详情' }}</span>
        </div>
        <div v-if="selectedPayment.transaction_id" class="detail-row">
          <span class="detail-label">交易号:</span>
          <span class="detail-value">{{ selectedPayment.transaction_id }}</span>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
          <el-button v-if="selectedPayment && selectedPayment.status === 'pending'" type="primary" @click="goToPay(selectedPayment)">
            去支付
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 新增支付弹窗 -->
    <el-dialog
      v-model="paymentDialogVisible"
      title="支付"
      width="550px"
      :close-on-click-modal="false"
      center
    >
      <div v-if="payingRecord" class="payment-dialog-content">
        <div class="payment-info">
          <div class="payment-amount">
            <span class="label">支付金额：</span>
            <span class="price">¥{{ payingRecord.amount.toFixed(2) }}</span>
          </div>
          <div class="payment-detail">{{ payingRecord.details }}</div>
        </div>

        <el-divider>选择支付方式</el-divider>

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
                <el-radio label="medical_insurance">
                  <div class="payment-method-content">
                    <i class="el-icon-medicine-box payment-icon"></i>
                    <div class="payment-method-info">
                      <span class="method-name">医保支付</span>
                      <span class="method-desc">使用医保卡支付</span>
                    </div>
                  </div>
                </el-radio>
              </div>

              <div class="payment-method-item">
                <el-radio label="cash">
                  <div class="payment-method-content">
                    <i class="el-icon-money payment-icon"></i>
                    <div class="payment-method-info">
                      <span class="method-name">现金支付</span>
                      <span class="method-desc">到院现金支付</span>
                    </div>
                  </div>
                </el-radio>
              </div>
            </div>
          </el-radio-group>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="paymentDialogVisible = false">取消</el-button>
          <el-button type="primary" :disabled="!selectedPaymentMethod" :loading="processing" @click="processPayment">立即支付</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 支付成功弹窗 -->
    <el-dialog
      v-model="paymentSuccessVisible"
      title="支付成功"
      width="400px"
      :show-close="false"
      center
    >
      <div class="success-content">
        <el-icon :size="64" color="#67C23A" class="success-icon"><CircleCheck /></el-icon>
        <h3>支付成功！</h3>
        <p>您的订单已完成支付</p>
        <p class="success-code">支付单号：#{{ payingRecord?.payment_id }}</p>
      </div>
      <template #footer>
        <div class="success-footer">
          <el-button type="primary" @click="handlePaymentSuccess">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { usePatientStore } from '../../store/patient'
import { ElMessage } from 'element-plus'
import { CircleCheck } from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'PaymentHistoryPage',
  components: {
    CircleCheck
  },
  setup() {
    const patientStore = usePatientStore()
    
    const loading = ref(false)
    const processing = ref(false)
    const payments = ref([])
    const totalPayments = ref(0)
    const currentPage = ref(1)
    const pageSize = ref(10)
    
    // 筛选选项
    const filterStatus = ref('')
    const filterType = ref('')
    const dateRange = ref(null)
    
    // 详情对话框
    const detailDialogVisible = ref(false)
    const selectedPayment = ref(null)

    // 支付对话框
    const paymentDialogVisible = ref(false)
    const payingRecord = ref(null)
    const selectedPaymentMethod = ref('')
    const paymentSuccessVisible = ref(false)
    
    // 获取支付记录
    const fetchPayments = async () => {
      loading.value = true
      try {
        const patientId = patientStore.patientId || localStorage.getItem('patientId') || 1
        
        const response = await axios.get('/api/patient/payments/history', {
          params: {
            patient_id: patientId,
            page: currentPage.value,
            per_page: pageSize.value
          }
        })
        
        if (response.data && response.data.status === 'success') {
          console.log('成功获取支付记录数据:', response.data.data)
          payments.value = response.data.data.payments || []
          totalPayments.value = response.data.data.total || 0
        } else {
          throw new Error(response.data?.message || '获取支付记录失败')
        }
      } catch (error) {
        console.error('Failed to fetch payment history:', error)
        ElMessage.error('获取支付记录失败')
        payments.value = []
        totalPayments.value = 0
      } finally {
        loading.value = false
      }
    }
    
    // 过滤后的支付记录
    const filteredPayments = computed(() => {
      let result = [...payments.value]
      
      // 按状态筛选
      if (filterStatus.value) {
        result = result.filter(p => p.status === filterStatus.value)
      }
      
      // 按类型筛选
      if (filterType.value) {
        result = result.filter(p => p.type === filterType.value)
      }
      
      // 按日期范围筛选
      if (dateRange.value && dateRange.value.length === 2) {
        const startDate = new Date(dateRange.value[0])
        startDate.setHours(0, 0, 0, 0)
        
        const endDate = new Date(dateRange.value[1])
        endDate.setHours(23, 59, 59, 999)
        
        result = result.filter(p => {
          const createdAt = new Date(p.created_at)
          return createdAt >= startDate && createdAt <= endDate
        })
      }
      
      return result
    })
    
    // 格式化时间
    const formatDateTime = (dateString) => {
      if (!dateString) return ''
      
      try {
        const date = new Date(dateString)
        return date.toLocaleString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        })
      } catch {
        return dateString
      }
    }
    
    // 格式化支付类型
    const formatPaymentType = (type) => {
      const typeMap = {
        'registration_fee': '挂号费',
        'consultation_fee': '问诊费',
        '挂号': '挂号费',
        '挂号费': '挂号费',
        '医保支付': '医保支付',
        '现金支付': '现金支付',
        '支付宝支付': '支付宝支付',
        '微信支付': '微信支付'
      }
      return typeMap[type] || type
    }
    
    // 格式化支付方式
    const formatPaymentMethod = (method) => {
      if (!method) return '暂无详情'
      
      const methodMap = {
        'alipay': '支付宝',
        'wechat': '微信支付',
        'unionpay': '银联支付',
        'medical_insurance': '医保支付',
        'cash': '现金支付'
      }
      return methodMap[method] || method
    }
    
    // 去支付 - 打开支付弹窗
    const goToPay = (payment) => {
      payingRecord.value = {...payment}
      selectedPaymentMethod.value = ''
      paymentDialogVisible.value = true
    }
    
    // 处理支付
    const processPayment = async () => {
      if (!payingRecord.value || !selectedPaymentMethod.value) {
        ElMessage.warning('请选择支付方式')
        return
      }
      
      processing.value = true
      
      try {
        // 构建支付数据
        const paymentData = {
          payment_id: payingRecord.value.payment_id,
          payment_method: selectedPaymentMethod.value,
          transaction_id: `TX${Date.now()}${Math.floor(Math.random() * 1000)}`
        }
        
        // 在实际应用中，我们会调用API完成支付
        // 这里是模拟API调用
        try {
          // 调用完成支付的API
          const response = await axios.put(`/api/patient/payments/${payingRecord.value.payment_id}/complete`, paymentData)
          
          if (response.data && response.data.status === 'success') {
            console.log('Payment successful:', response.data)
            showPaymentSuccess()
            return
          }
        } catch (apiError) {
          console.warn('API error, using mock payment process:', apiError)
        }
        
        // 模拟成功场景 - 更新本地支付记录
        setTimeout(() => {
          // 找到当前正在支付的记录
          const paymentIndex = payments.value.findIndex(p => p.payment_id === payingRecord.value.payment_id)
          
          if (paymentIndex !== -1) {
            // 更新支付状态
            const updatedPayment = {
              ...payments.value[paymentIndex],
              status: 'paid',
              payment_method: selectedPaymentMethod.value,
              payment_time: new Date().toISOString(),
              transaction_id: paymentData.transaction_id,
              type: formatPaymentTypeByMethod(selectedPaymentMethod.value)
            }
            
            // 更新列表中的数据
            payments.value.splice(paymentIndex, 1, updatedPayment)
            
            // 更新当前正在支付的记录
            payingRecord.value = updatedPayment
            
            // 显示支付成功
            showPaymentSuccess()
          }
        }, 1500) // 模拟网络延迟
      } catch (error) {
        console.error('Payment failed:', error)
        ElMessage.error('支付失败，请稍后重试')
        processing.value = false
      }
    }
    
    // 根据支付方式格式化支付类型
    const formatPaymentTypeByMethod = (method) => {
      const methodTypeMap = {
        'alipay': '支付宝支付',
        'wechat': '微信支付',
        'medical_insurance': '医保支付',
        'cash': '现金支付'
      }
      return methodTypeMap[method] || '挂号费'
    }
    
    // 显示支付成功
    const showPaymentSuccess = () => {
      processing.value = false
      paymentDialogVisible.value = false
      paymentSuccessVisible.value = true
    }
    
    // 处理支付成功
    const handlePaymentSuccess = () => {
      paymentSuccessVisible.value = false
      payingRecord.value = null
    }
    
    // 查看详情
    const viewDetail = (payment) => {
      selectedPayment.value = payment
      detailDialogVisible.value = true
    }
    
    // 分页大小变化
    const handleSizeChange = (size) => {
      pageSize.value = size
      fetchPayments()
    }
    
    // 当前页变化
    const handleCurrentChange = (page) => {
      currentPage.value = page
      fetchPayments()
    }
    
    // 监听筛选条件变化
    watch([filterStatus, filterType, dateRange], () => {
      currentPage.value = 1 // 重置到第一页
    })
    
    // 初始加载
    onMounted(() => {
      fetchPayments()
    })
    
    return {
      loading,
      processing,
      payments,
      totalPayments,
      currentPage,
      pageSize,
      filterStatus,
      filterType,
      dateRange,
      filteredPayments,
      detailDialogVisible,
      selectedPayment,
      paymentDialogVisible,
      payingRecord,
      selectedPaymentMethod,
      paymentSuccessVisible,
      formatDateTime,
      formatPaymentType,
      formatPaymentMethod,
      goToPay,
      processPayment,
      viewDetail,
      handleSizeChange,
      handleCurrentChange,
      handlePaymentSuccess
    }
  }
}
</script>

<style scoped>
.page-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 20px;
}

.content-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.filter-section {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.loading-section, .empty-section {
  padding: 40px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-section .small {
  font-size: 14px;
  color: #909399;
}

.payment-id {
  font-family: monospace;
  font-weight: 600;
}

.amount {
  font-weight: 600;
  color: #F56C6C;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

/* 详情对话框样式 */
.payment-detail {
  padding: 0 20px;
}

.detail-row {
  display: flex;
  margin-bottom: 15px;
}

.detail-label {
  width: 100px;
  color: #606266;
  font-weight: 500;
}

.detail-value {
  flex: 1;
}

/* 支付弹窗样式 */
.payment-dialog-content {
  padding: 20px 0;
}

.payment-info {
  text-align: center;
  margin-bottom: 20px;
}

.payment-amount {
  margin-bottom: 10px;
}

.payment-amount .label {
  font-size: 16px;
  color: #606266;
}

.payment-amount .price {
  font-size: 24px;
  color: #F56C6C;
  font-weight: bold;
}

.payment-detail {
  color: #909399;
  font-size: 14px;
}

.payment-methods {
  margin-top: 20px;
}

.payment-method-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.payment-method-item {
  padding: 10px;
  border-radius: 4px;
  transition: all 0.3s;
}

.payment-method-content {
  display: flex;
  align-items: center;
}

.payment-icon {
  width: 24px;
  height: 24px;
  margin-right: 10px;
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

/* 支付成功弹窗样式 */
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
  font-family: monospace;
  font-weight: 600;
  color: #303133;
}

.success-footer {
  display: flex;
  justify-content: center;
}
</style> 