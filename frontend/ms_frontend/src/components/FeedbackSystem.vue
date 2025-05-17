<template>
  <div class="feedback-container">
    <div class="feedback-header">
      <h2>医疗服务反馈</h2>
      <p class="subtitle">您的意见将帮助我们提供更好的医疗服务</p>
    </div>

    <el-form :model="feedbackForm" :rules="rules" ref="feedbackForm" label-position="top">
      <!-- 星级评价 -->
      <el-form-item label="整体满意度" prop="rating">
        <el-rate
          v-model="feedbackForm.rating"
          :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
          :max="5"
          show-text
          text-color="#ff9900"
          :texts="['非常差', '差', '一般', '好', '非常好']"
        />
      </el-form-item>

      <!-- 分类评价 -->
      <el-form-item label="分类评价" prop="categoryRatings">
        <div class="category-ratings">
          <div v-for="category in ratingCategories" :key="category.key" class="category-item">
            <span>{{ category.label }}</span>
            <el-rate
              v-model="feedbackForm.categoryRatings[category.key]"
              :max="5"
              :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
            />
          </div>
        </div>
      </el-form-item>

      <!-- 反馈内容 -->
      <el-form-item label="详细反馈" prop="content">
        <el-input
          type="textarea"
          v-model="feedbackForm.content"
          :rows="5"
          placeholder="请详细描述您的使用体验、遇到的问题或改进建议"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <!-- 图片上传 -->
      <el-form-item label="上传截图（可选）">
        <el-upload
          action="https://your-upload-api.com"
          list-type="picture-card"
          :on-preview="handlePictureCardPreview"
          :on-remove="handleRemove"
          :file-list="fileList"
          :limit="3"
          :on-exceed="handleExceed"
        >
          <el-icon><Plus /></el-icon>
        </el-upload>
        <el-dialog v-model="dialogVisible">
          <img w-full :src="dialogImageUrl" alt="预览图片" />
        </el-dialog>
      </el-form-item>

      <!-- 联系方式 -->
      <el-form-item label="联系方式（可选）" prop="contact">
        <el-input
          v-model="feedbackForm.contact"
          placeholder="请输入您的邮箱或手机号，方便我们回复您"
        />
      </el-form-item>

      <!-- 提交按钮 -->
      <el-form-item>
        <el-button
          type="primary"
          @click="submitForm"
          :loading="submitting"
          size="large"
        >
          {{ submitting ? '提交中...' : '提交反馈' }}
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'FeedbackSystem',
  components: { Plus },
  setup() {
    // 使用 reactive 确保响应式对象完整初始化
    const feedbackForm = reactive({
      rating: 0,
      categoryRatings: {
        service: 0,
        interface: 0,
        function: 0,
        performance: 0
      },
      content: '',
      contact: ''
    })

    const rules = {
      rating: [
        { required: true, message: '请选择整体满意度', trigger: 'blur' }
      ],
      content: [
        { required: true, message: '请填写反馈内容', trigger: 'blur' },
        { min: 10, message: '反馈内容至少10个字符', trigger: 'blur' }
      ]
    }

    const ratingCategories = ref([
      { key: 'service', label: '服务态度' },
      { key: 'interface', label: '界面设计' },
      { key: 'function', label: '功能完整性' },
      { key: 'performance', label: '系统性能' }
    ])

    const fileList = ref([])
    const dialogImageUrl = ref('')
    const dialogVisible = ref(false)
    const submitting = ref(false)

    const handleRemove = (file) => {
      console.log(file)
    }

    const handlePictureCardPreview = (file) => {
      dialogImageUrl.value = file.url
      dialogVisible.value = true
    }

    const handleExceed = () => {
      ElMessage.warning('最多只能上传3张图片')
    }

    const submitForm = () => {
      submitting.value = true
      // 这里替换为实际的提交逻辑
      setTimeout(() => {
        ElMessage.success('反馈提交成功！感谢您的宝贵意见')
        submitting.value = false
      }, 1500)
    }

    return {
      feedbackForm,
      rules,
      ratingCategories,
      fileList,
      dialogImageUrl,
      dialogVisible,
      submitting,
      handleRemove,
      handlePictureCardPreview,
      handleExceed,
      submitForm
    }
  }
}
</script>

<style scoped>
.feedback-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.feedback-header {
  text-align: center;
  margin-bottom: 30px;
}

.feedback-header h2 {
  color: #303133;
  font-size: 24px;
  margin-bottom: 8px;
}

.subtitle {
  color: #909399;
  font-size: 14px;
}

.category-ratings {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.category-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.category-item span {
  color: #606266;
  font-size: 14px;
}

:deep(.el-form-item__label) {
  font-weight: bold;
  color: #303133;
}

:deep(.el-textarea__inner) {
  min-height: 120px;
}

:deep(.el-upload--picture-card) {
  background-color: #f5f7fa;
  border: 1px dashed #d9d9d9;
}

:deep(.el-upload--picture-card:hover) {
  border-color: #409eff;
}

.submit-btn {
  width: 200px;
  margin-top: 20px;
}
</style>