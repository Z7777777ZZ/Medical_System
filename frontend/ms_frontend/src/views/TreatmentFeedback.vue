<template>
  <div class="treatment-feedback">
    <div class="page-header card">
      <h1>就诊体验反馈</h1>
      <p>请对您的就诊过程进行评价，您的反馈将帮助我们提升服务质量</p>
    </div>

    <div class="feedback-form-container card">
      <el-form 
        ref="feedbackFormRef"
        :model="feedbackForm"
        :rules="rules"
        label-position="top"
        class="feedback-form"
      >
        <h2 class="form-title">填写就诊体验反馈</h2>
        
        <!-- 关联预约 -->
        <el-form-item label="选择就诊记录" prop="appointment_id">
          <el-select 
            v-model="feedbackForm.appointment_id"
            placeholder="请选择要评价的就诊记录"
            style="width: 100%"
            filterable
          >
            <el-option 
              v-for="appointment in recentAppointments" 
              :key="appointment.id" 
              :label="appointment.label" 
              :value="appointment.id"
            />
          </el-select>
        </el-form-item>
        
        <!-- 评分区域 -->
        <div class="rating-section">
          <el-form-item label="就诊体验总评" prop="treatment_rating">
            <el-rate
              v-model="feedbackForm.treatment_rating"
              :colors="colors"
              :texts="rateTexts"
              show-text
            />
          </el-form-item>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="医生评分" prop="doctor_rating">
                <el-rate
                  v-model="feedbackForm.doctor_rating"
                  :colors="colors"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="医院环境评分" prop="hospital_rating">
                <el-rate
                  v-model="feedbackForm.hospital_rating"
                  :colors="colors"
                />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-form-item label="等待时间评分" prop="waiting_rating">
            <el-rate
              v-model="feedbackForm.waiting_rating"
              :colors="colors"
            />
          </el-form-item>
        </div>
        
        <!-- 反馈内容 -->
        <el-form-item label="详细反馈内容" prop="content">
          <el-input
            type="textarea"
            v-model="feedbackForm.content"
            :rows="6"
            placeholder="请详细描述您的就诊体验、满意/不满意的地方，以及改进建议..."
          />
        </el-form-item>
        
        <!-- 提交按钮 -->
        <div class="form-actions">
          <el-button type="primary" :loading="loading" @click="submitFeedback">提交反馈</el-button>
          <el-button @click="resetForm">重置</el-button>
        </div>
      </el-form>
    </div>
    
    <!-- 感谢提示 -->
    <el-dialog
      v-model="thanksVisible"
      title="感谢您的反馈"
      width="30%"
      center
    >
      <div class="thanks-content">
        <el-icon size="40" color="#67C23A"><CircleCheckFilled /></el-icon>
        <p>我们已收到您的就诊体验反馈，感谢您的宝贵意见！</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="thanksVisible = false">
            完成
          </el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 无预约提示 -->
    <el-dialog
      v-model="noAppointmentVisible"
      title="提示"
      width="30%"
      center
    >
      <div class="warning-content">
        <el-icon size="40" color="#E6A23C"><WarningFilled /></el-icon>
        <p>您暂无可评价的就诊记录，请在就诊后再来评价。</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="goToAppointment">前往预约</el-button>
          <el-button type="primary" @click="noAppointmentVisible = false">
            我知道了
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { CircleCheckFilled, WarningFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()

// 表单引用
const feedbackFormRef = ref(null)

// 对话框
const thanksVisible = ref(false)
const noAppointmentVisible = ref(false)

// 提交状态
const loading = ref(false)

// 评分级别文字
const rateTexts = ['非常不满意', '不满意', '一般', '满意', '非常满意']

// 评分颜色
const colors = {
  1: '#F56C6C',  // 红色
  2: '#E6A23C',  // 橙色
  3: '#909399',  // 灰色
  4: '#67C23A',  // 绿色
  5: '#409EFF'   // 蓝色
}

// 近期预约列表
const recentAppointments = ref([])

// 表单数据
const feedbackForm = reactive({
  patient_id: 1, // 模拟用户ID，实际应从登录状态获取
  appointment_id: null,
  treatment_rating: 0,
  doctor_rating: 0,
  hospital_rating: 0,
  waiting_rating: 0,
  content: ''
})

// 表单验证规则
const rules = {
  appointment_id: [
    { required: true, message: '请选择要评价的就诊记录', trigger: 'change' }
  ],
  treatment_rating: [
    { required: true, message: '请对就诊体验进行总评', trigger: 'change' },
    { type: 'number', min: 1, message: '请至少选择一颗星', trigger: 'change' }
  ],
  doctor_rating: [
    { required: true, message: '请对医生进行评分', trigger: 'change' },
    { type: 'number', min: 1, message: '请至少选择一颗星', trigger: 'change' }
  ],
  hospital_rating: [
    { required: true, message: '请对医院环境进行评分', trigger: 'change' },
    { type: 'number', min: 1, message: '请至少选择一颗星', trigger: 'change' }
  ],
  waiting_rating: [
    { required: true, message: '请对等待时间进行评分', trigger: 'change' },
    { type: 'number', min: 1, message: '请至少选择一颗星', trigger: 'change' }
  ],
  content: [
    { required: true, message: '请填写详细反馈内容', trigger: 'blur' },
    { min: 10, message: '反馈内容不能少于10个字符', trigger: 'blur' }
  ]
}

// 获取近期预约
const getRecentAppointments = async () => {
  try {
    // 实际应通过API获取
    // 模拟数据
    recentAppointments.value = [
      {
        id: 1,
        label: '2023-11-10 上午 - 内科 - 张医生',
        doctor_name: '张医生',
        department: '内科',
        appointment_time: '2023-11-10 09:30:00',
        status: 'completed'
      },
      {
        id: 2,
        label: '2023-11-15 下午 - 外科 - 李医生',
        doctor_name: '李医生',
        department: '外科',
        appointment_time: '2023-11-15 14:00:00',
        status: 'completed'
      },
      {
        id: 3,
        label: '2023-11-20 上午 - 眼科 - 王医生',
        doctor_name: '王医生',
        department: '眼科',
        appointment_time: '2023-11-20 10:30:00',
        status: 'completed'
      }
    ]
    
    // 如果没有可评价的预约，显示提示对话框
    if (recentAppointments.value.length === 0) {
      noAppointmentVisible.value = true
    }
  } catch (error) {
    console.error('获取近期预约失败:', error)
    ElMessage.error('获取近期预约失败，请刷新页面重试')
  }
}

// 提交反馈
const submitFeedback = () => {
  feedbackFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const { data } = await axios.post('/api/treatment-feedbacks', feedbackForm)
        if (data.status === 'success') {
          thanksVisible.value = true
          resetForm()
        } else {
          ElMessage.error(data.message || '提交失败，请稍后重试')
        }
      } catch (error) {
        console.error('提交反馈失败:', error)
        ElMessage.error('提交失败，请稍后重试')
      } finally {
        loading.value = false
      }
    } else {
      ElMessage.warning('请完善表单信息')
      return false
    }
  })
}

// 重置表单
const resetForm = () => {
  feedbackFormRef.value.resetFields()
}

// 前往预约页面
const goToAppointment = () => {
  noAppointmentVisible.value = false
  // 实际应该跳转到预约页面
  router.push('/')
}

onMounted(() => {
  getRecentAppointments()
})
</script>

<style scoped>
.treatment-feedback {
  padding-bottom: 30px;
}

.page-header {
  text-align: center;
  padding: 30px;
  margin-bottom: 30px;
  background-color: #f0f9ff;
}

.page-header h1 {
  font-size: 28px;
  margin-bottom: 10px;
  color: #409EFF;
}

.page-header p {
  color: #606266;
}

.feedback-form-container {
  max-width: 800px;
  margin: 0 auto 30px;
  padding: 30px;
}

.form-title {
  font-size: 20px;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid #EBEEF5;
  color: #303133;
}

.rating-section {
  margin: 20px 0;
  padding: 20px;
  background-color: #f9fafc;
  border-radius: 8px;
}

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  gap: 20px;
}

.thanks-content, .warning-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 20px 0;
}

.thanks-content p, .warning-content p {
  font-size: 16px;
  color: #606266;
  text-align: center;
}

@media (max-width: 768px) {
  .feedback-form-container {
    padding: 20px;
  }
  
  .rating-section {
    padding: 15px;
  }
}
</style> 