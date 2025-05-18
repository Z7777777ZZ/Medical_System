<template>
  <div class="recovery-feedback">
    <div class="page-header card">
      <h1>康复情况反馈</h1>
      <p>请告诉我们您的康复情况，这将帮助医生更好地了解治疗效果</p>
    </div>

    <div class="feedback-form-container card">
      <el-form 
        ref="feedbackFormRef"
        :model="feedbackForm"
        :rules="rules"
        label-position="top"
        class="feedback-form"
      >
        <h2 class="form-title">填写康复情况反馈</h2>
        
        <!-- 关联病历 -->
        <el-form-item label="选择病历记录" prop="medical_record_id">
          <el-select 
            v-model="feedbackForm.medical_record_id"
            placeholder="请选择要反馈的病历记录"
            style="width: 100%"
            filterable
          >
            <el-option 
              v-for="record in medicalRecords" 
              :key="record.id" 
              :label="record.label" 
              :value="record.id"
            />
          </el-select>
        </el-form-item>
        
        <!-- 病历信息 -->
        <div v-if="selectedRecord" class="record-info">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="就诊医生">{{ selectedRecord.doctor_name }}</el-descriptions-item>
            <el-descriptions-item label="就诊日期">{{ selectedRecord.visit_date }}</el-descriptions-item>
            <el-descriptions-item label="诊断结果" :span="2">{{ selectedRecord.diagnosis }}</el-descriptions-item>
            <el-descriptions-item label="治疗方案" :span="2">{{ selectedRecord.treatment }}</el-descriptions-item>
          </el-descriptions>
        </div>
        
        <!-- 康复状态 -->
        <el-form-item label="康复状态" prop="recovery_status">
          <el-radio-group v-model="feedbackForm.recovery_status">
            <el-radio label="worse">病情恶化</el-radio>
            <el-radio label="same">没有变化</el-radio>
            <el-radio label="better">有所好转</el-radio>
            <el-radio label="cured">已基本痊愈</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <!-- 症状描述 -->
        <el-form-item label="当前症状描述" prop="symptom_description">
          <el-input
            type="textarea"
            v-model="feedbackForm.symptom_description"
            :rows="4"
            placeholder="请详细描述您目前的症状和身体状况..."
          />
        </el-form-item>
        
        <!-- 服药情况 -->
        <el-form-item label="服药依从性" prop="medication_adherence">
          <el-radio-group v-model="feedbackForm.medication_adherence">
            <el-radio label="good">严格按照医嘱服药</el-radio>
            <el-radio label="moderate">基本按照医嘱服药，偶尔有遗漏</el-radio>
            <el-radio label="poor">服药不规律或已停药</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <!-- 副作用 -->
        <el-form-item label="药物副作用（如有）" prop="side_effects">
          <el-input
            type="textarea"
            v-model="feedbackForm.side_effects"
            :rows="3"
            placeholder="如果您在服药过程中出现了不适或副作用，请在此描述..."
          />
        </el-form-item>
        
        <!-- 其他反馈 -->
        <el-form-item label="其他反馈" prop="content">
          <el-input
            type="textarea"
            v-model="feedbackForm.content"
            :rows="3"
            placeholder="其他您想补充的情况或建议..."
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
        <p>我们已收到您的康复情况反馈，医生会根据您的反馈对后续治疗进行调整。</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="thanksVisible = false">
            完成
          </el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 无病历提示 -->
    <el-dialog
      v-model="noRecordVisible"
      title="提示"
      width="30%"
      center
    >
      <div class="warning-content">
        <el-icon size="40" color="#E6A23C"><WarningFilled /></el-icon>
        <p>您暂无可反馈的病历记录，请在就诊后再来提交康复反馈。</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="goToAppointment">前往预约</el-button>
          <el-button type="primary" @click="noRecordVisible = false">
            我知道了
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { CircleCheckFilled, WarningFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()

// 表单引用
const feedbackFormRef = ref(null)

// 对话框
const thanksVisible = ref(false)
const noRecordVisible = ref(false)

// 提交状态
const loading = ref(false)

// 病历记录列表
const medicalRecords = ref([])

// 表单数据
const feedbackForm = reactive({
  patient_id: 1, // 模拟用户ID，实际应从登录状态获取
  medical_record_id: null,
  recovery_status: '',
  symptom_description: '',
  medication_adherence: '',
  side_effects: '',
  content: ''
})

// 当前选中的病历
const selectedRecord = computed(() => {
  if (!feedbackForm.medical_record_id) return null
  return medicalRecords.value.find(record => record.id === feedbackForm.medical_record_id)
})

// 表单验证规则
const rules = {
  medical_record_id: [
    { required: true, message: '请选择要反馈的病历记录', trigger: 'change' }
  ],
  recovery_status: [
    { required: true, message: '请选择您的康复状态', trigger: 'change' }
  ],
  symptom_description: [
    { required: true, message: '请描述您当前的症状', trigger: 'blur' },
    { min: 10, message: '症状描述不能少于10个字符', trigger: 'blur' }
  ],
  medication_adherence: [
    { required: true, message: '请选择您的服药情况', trigger: 'change' }
  ]
}

// 获取病历记录
const getMedicalRecords = async () => {
  try {
    // 实际应通过API获取
    // 模拟数据
    medicalRecords.value = [
      {
        id: 1,
        label: '2023-11-10 - 内科 - 高血压随访',
        doctor_name: '张医生',
        visit_date: '2023-11-10',
        diagnosis: '原发性高血压，血压控制一般',
        treatment: '服用硝苯地平缓释片，每日一次，每次一片',
        department: '内科'
      },
      {
        id: 2,
        label: '2023-11-15 - 外科 - 腕部扭伤',
        doctor_name: '李医生',
        visit_date: '2023-11-15',
        diagnosis: '右腕关节扭伤',
        treatment: '冷敷，制动，服用布洛芬缓解疼痛',
        department: '外科'
      },
      {
        id: 3,
        label: '2023-11-20 - 眼科 - 结膜炎',
        doctor_name: '王医生',
        visit_date: '2023-11-20',
        diagnosis: '双眼急性结膜炎',
        treatment: '滴用左氧氟沙星滴眼液，每日4次',
        department: '眼科'
      }
    ]
    
    // 如果没有可反馈的病历，显示提示对话框
    if (medicalRecords.value.length === 0) {
      noRecordVisible.value = true
    }
  } catch (error) {
    console.error('获取病历记录失败:', error)
    ElMessage.error('获取病历记录失败，请刷新页面重试')
  }
}

// 提交反馈
const submitFeedback = () => {
  feedbackFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const { data } = await axios.post('/api/recovery-feedbacks', feedbackForm)
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
  noRecordVisible.value = false
  // 实际应该跳转到预约页面
  router.push('/')
}

onMounted(() => {
  getMedicalRecords()
})
</script>

<style scoped>
.recovery-feedback {
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

.record-info {
  margin: 20px 0;
  padding: 15px;
  background-color: #f9fafc;
  border-radius: 8px;
  border-left: 4px solid #409EFF;
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
  
  .record-info {
    padding: 10px;
  }
}
</style> 