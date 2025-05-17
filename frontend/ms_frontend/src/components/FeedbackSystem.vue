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
          list-type="picture-card"
          :on-preview="handlePictureCardPreview"
          :on-remove="handleRemove"
          :file-list="fileList"
          :limit="3"
          :on-exceed="handleExceed"
          :before-upload="beforeUpload"
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
        <el-button type="default" @click="showHistory = !showHistory" style="margin-left: 16px;">
          {{ showHistory ? '收起历史反馈' : '查看历史反馈' }}
        </el-button>
      </el-form-item>
    </el-form>

    <!-- 历史反馈展示 -->
    <el-card v-if="showHistory" class="history-card" style="margin-top: 32px;">
      <h3 style="margin-bottom: 16px;">历史反馈记录</h3>
      <el-table :data="limitedFeedbackHistory" style="width: 100%" border>
        <el-table-column prop="created_at" label="提交时间" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template #default="scope">
            <el-button size="small" @click="viewFeedback(scope.row)">查看</el-button>
            <el-button size="small" type="danger" @click="deleteFeedback(scope.row.id)" style="margin-left: 8px;">撤回</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="feedbackHistory.length > 3" style="text-align: center; margin-top: 16px;">
        <el-button type="text" @click="showAllFeedback = !showAllFeedback">
          {{ showAllFeedback ? '收起' : '查看更多' }}
        </el-button>
      </div>
      <div v-if="!loadingHistory && feedbackHistory.length === 0" style="text-align:center;color:#aaa;padding:24px;">暂无历史反馈</div>
    </el-card>

    <el-dialog v-model="feedbackDetailDialogVisible" title="反馈详情" :width="'600px'">
      <div v-if="selectedFeedback" style="max-height: 400px; overflow-y: auto;">
        <p><strong>提交时间：</strong>{{ selectedFeedback.created_at }}</p>
        <p><strong>满意度：</strong>{{ selectedFeedback.rating }}</p>
        <p><strong>服务态度：</strong>{{ selectedFeedback.categoryRatings.service }}</p>
        <p><strong>界面设计：</strong>{{ selectedFeedback.categoryRatings.interface }}</p>
        <p><strong>功能完整性：</strong>{{ selectedFeedback.categoryRatings.function }}</p>
        <p><strong>系统性能：</strong>{{ selectedFeedback.categoryRatings.performance }}</p>
        <p><strong>反馈内容：</strong>{{ selectedFeedback.content }}</p>
        <p><strong>联系方式：</strong>{{ selectedFeedback.contact }}</p>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  name: 'FeedbackSystem',
  components: { Plus },
  data() {
    return {
      feedbackForm: {
        rating: 0,
        categoryRatings: {
          service: 0,
          interface: 0,
          function: 0,
          performance: 0
        },
        content: '',
        contact: '',
        images: []
      },
      rules: {
        rating: [
          { required: true, message: '请选择整体满意度', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请填写反馈内容', trigger: 'blur' },
          { min: 10, message: '反馈内容至少10个字符', trigger: 'blur' }
        ]
      },
      ratingCategories: [
        { key: 'service', label: '服务态度' },
        { key: 'interface', label: '界面设计' },
        { key: 'function', label: '功能完整性' },
        { key: 'performance', label: '系统性能' }
      ],
      fileList: [],
      dialogImageUrl: '',
      dialogVisible: false,
      submitting: false,
      showHistory: false,
      loadingHistory: false,
      feedbackHistory: [],
      feedbackDetailDialogVisible: false,
      selectedFeedback: null,
      showAllFeedback: false
    }
  },
  computed: {
    limitedFeedbackHistory() {
      return this.showAllFeedback ? this.feedbackHistory : this.feedbackHistory.slice(0, 3);
    }
  },
  methods: {
    handleRemove(file) {
      const fileUrl = file.url || file.response?.url
      this.feedbackForm.images = this.feedbackForm.images.filter(url => url !== fileUrl)
      this.fileList = this.fileList.filter(f => f.uid !== file.uid)
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url || file.response?.url || ''
      this.dialogVisible = true
    },
    handleExceed() {
      ElMessage.warning('最多只能上传3张图片')
    },
    beforeUpload(file) {
      const isImage = file.type.startsWith('image/')
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isImage) {
        this.$message.error('只能上传图片文件！')
      }
      if (!isLt2M) {
        this.$message.error('图片大小不能超过 2MB！')
      }
      return isImage && isLt2M
    },
    handleUpload(file) {
      // 模拟上传成功后将图片 URL 添加到 feedbackForm.images
      const fakeUrl = URL.createObjectURL(file)
      this.feedbackForm.images.push(fakeUrl)
      this.fileList.push({
        name: file.name,
        url: fakeUrl,
        uid: file.uid
      })
      this.$message.success('图片已添加！')
    },
    async fetchHistory() {
      this.loadingHistory = true
      try {
        const res = await axios.get('/api/feedbacks')
        if (res.data.success) {
          this.feedbackHistory = res.data.data || []
        } else {
          ElMessage.error(res.data.msg || '获取历史反馈失败')
        }
      } catch (e) {
        ElMessage.error('获取历史反馈失败')
      } finally {
        this.loadingHistory = false
      }
    },
    async submitForm() {
      this.submitting = true
      try {
        this.feedbackForm.images = this.fileList.map(f => f.url || f.response?.url || '')
        const payload = {
          rating: this.feedbackForm.rating,
          categoryRatings: {
            service: this.feedbackForm.categoryRatings.service,
            interface: this.feedbackForm.categoryRatings.interface,
            function: this.feedbackForm.categoryRatings.function,
            performance: this.feedbackForm.categoryRatings.performance
          },
          content: this.feedbackForm.content,
          contact: this.feedbackForm.contact,
          images: this.feedbackForm.images
        }
        const res = await axios.post('/api/feedbacks', payload)
        if (res.data.success) {
          ElMessage.success('反馈提交成功！感谢您的宝贵意见')
          this.resetForm()
          if (this.showHistory) this.fetchHistory()
        } else {
          ElMessage.error(res.data.msg || '提交失败')
        }
      } catch (e) {
        ElMessage.error('提交失败')
      } finally {
        this.submitting = false
      }
    },
    resetForm() {
      this.feedbackForm.rating = 0
      this.feedbackForm.categoryRatings = { service: 0, interface: 0, function: 0, performance: 0 }
      this.feedbackForm.content = ''
      this.feedbackForm.contact = ''
      this.feedbackForm.images = []
      this.fileList = []
    },
    async deleteFeedback(id) {
      try {
        const confirm = await this.$confirm('确定要撤回这条反馈记录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });
        if (confirm) {
          const response = await axios.delete(`/api/feedbacks/${id}`);
          if (response.data.success) {
            this.$message.success('反馈记录已撤回');
            this.feedbackHistory = this.feedbackHistory.filter(feedback => feedback.id !== id);
          } else {
            this.$message.error(response.data.msg || '撤回失败');
          }
        }
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('请求失败，请稍后重试');
        }
      }
    },
    viewFeedback(feedback) {
      this.selectedFeedback = feedback;
      this.feedbackDetailDialogVisible = true;
    }
  },
  watch: {
    showHistory(val) {
      if (val) this.fetchHistory()
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

.history-card {
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-table {
  width: 100%;
}

.el-table th,
.el-table td {
  text-align: center;
}

.el-table .cell {
  padding: 16px 0;
}
</style>