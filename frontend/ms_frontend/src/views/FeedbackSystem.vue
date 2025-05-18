<template>
  <div class="feedback-system">
    <div class="page-header card">
      <h1>系统反馈</h1>
      <p>您的意见对我们非常重要，我们会根据您的反馈不断完善系统</p>
    </div>

    <div class="feedback-form-container card">
      <el-form 
        ref="feedbackFormRef"
        :model="feedbackForm"
        :rules="rules"
        label-position="top"
        class="feedback-form"
      >
        <h2 class="form-title">填写反馈信息</h2>
        
        <!-- 评分区域 -->
        <div class="rating-section">
          <el-form-item label="整体满意度" prop="rating">
            <el-rate
              v-model="feedbackForm.rating"
              :colors="colors"
              :texts="rateTexts"
              show-text
            />
          </el-form-item>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="服务态度评分" prop="service_rating">
                <el-rate
                  v-model="feedbackForm.service_rating"
                  :colors="colors"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="界面设计评分" prop="interface_rating">
                <el-rate
                  v-model="feedbackForm.interface_rating"
                  :colors="colors"
                />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="功能完整性评分" prop="function_rating">
                <el-rate
                  v-model="feedbackForm.function_rating"
                  :colors="colors"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="系统性能评分" prop="performance_rating">
                <el-rate
                  v-model="feedbackForm.performance_rating"
                  :colors="colors"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <!-- 反馈内容 -->
        <el-form-item label="详细反馈内容" prop="content">
          <el-input
            type="textarea"
            v-model="feedbackForm.content"
            :rows="6"
            placeholder="请详细描述您的使用体验、遇到的问题或建议..."
          />
        </el-form-item>
        
        <!-- 联系方式 -->
        <el-form-item label="联系方式（选填）" prop="contact">
          <el-input
            v-model="feedbackForm.contact"
            placeholder="请留下您的邮箱或手机号，方便我们与您联系"
          >
            <template #prepend>
              <el-select v-model="contactType" style="width: 100px">
                <el-option label="邮箱" value="email" />
                <el-option label="手机" value="phone" />
              </el-select>
            </template>
          </el-input>
        </el-form-item>
        
        <!-- 截图上传 -->
        <el-form-item label="相关截图（选填）">
          <el-upload
            :action="uploadUrl"
            list-type="picture-card"
            :on-preview="handlePictureCardPreview"
            :on-remove="handleRemove"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
            multiple
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
          <el-dialog v-model="dialogVisible">
            <img w-full :src="dialogImageUrl" alt="图片预览" />
          </el-dialog>
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
        <p>我们已收到您的宝贵反馈，感谢您帮助我们改进系统！</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="thanksVisible = false">
            完成
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Plus, CircleCheckFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

// 表单引用
const feedbackFormRef = ref(null)

// 联系方式类型
const contactType = ref('email')

// 图片预览
const dialogImageUrl = ref('')
const dialogVisible = ref(false)

// 感谢对话框
const thanksVisible = ref(false)

// 提交状态
const loading = ref(false)

// 上传地址
const uploadUrl = '/api/upload'

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

// 表单数据
const feedbackForm = reactive({
  patient_id: 1, // 模拟用户ID，实际应从登录状态获取
  rating: 0,
  service_rating: 0,
  interface_rating: 0,
  function_rating: 0,
  performance_rating: 0,
  content: '',
  contact: '',
  images: []
})

// 表单验证规则
const rules = {
  rating: [
    { required: true, message: '请对整体满意度进行评分', trigger: 'change' },
    { type: 'number', min: 1, message: '请至少选择一颗星', trigger: 'change' }
  ],
  service_rating: [
    { required: true, message: '请对服务态度进行评分', trigger: 'change' },
    { type: 'number', min: 1, message: '请至少选择一颗星', trigger: 'change' }
  ],
  interface_rating: [
    { required: true, message: '请对界面设计进行评分', trigger: 'change' },
    { type: 'number', min: 1, message: '请至少选择一颗星', trigger: 'change' }
  ],
  function_rating: [
    { required: true, message: '请对功能完整性进行评分', trigger: 'change' },
    { type: 'number', min: 1, message: '请至少选择一颗星', trigger: 'change' }
  ],
  performance_rating: [
    { required: true, message: '请对系统性能进行评分', trigger: 'change' },
    { type: 'number', min: 1, message: '请至少选择一颗星', trigger: 'change' }
  ],
  content: [
    { required: true, message: '请填写详细反馈内容', trigger: 'blur' },
    { min: 10, message: '反馈内容不能少于10个字符', trigger: 'blur' }
  ],
  contact: [
    { 
      validator: (rule, value, callback) => {
        if (!value) {
          callback()
          return
        }
        
        if (contactType.value === 'email') {
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
          if (!emailRegex.test(value)) {
            callback(new Error('请输入正确的邮箱格式'))
          } else {
            callback()
          }
        } else {
          const phoneRegex = /^1[3-9]\d{9}$/
          if (!phoneRegex.test(value)) {
            callback(new Error('请输入正确的手机号格式'))
          } else {
            callback()
          }
        }
      }, 
      trigger: 'blur' 
    }
  ]
}

// 图片预览
const handlePictureCardPreview = (file) => {
  dialogImageUrl.value = file.url
  dialogVisible.value = true
}

// 移除图片
const handleRemove = (file) => {
  const index = feedbackForm.images.indexOf(file.url)
  if (index !== -1) {
    feedbackForm.images.splice(index, 1)
  }
}

// 上传成功
const handleUploadSuccess = (response) => {
  if (response.status === 'success') {
    feedbackForm.images.push(response.data.url)
  }
}

// 上传前校验
const beforeUpload = (file) => {
  const isJPG = file.type === 'image/jpeg'
  const isPNG = file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG && !isPNG) {
    ElMessage.error('上传图片只能是 JPG 或 PNG 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('上传图片大小不能超过 2MB!')
    return false
  }
  return true
}

// 提交反馈
const submitFeedback = () => {
  feedbackFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const { data } = await axios.post('/api/feedbacks', feedbackForm)
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
  feedbackForm.images = []
}
</script>

<style scoped>
.feedback-system {
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
  margin-bottom: 20px;
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

.thanks-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 20px 0;
}

.thanks-content p {
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