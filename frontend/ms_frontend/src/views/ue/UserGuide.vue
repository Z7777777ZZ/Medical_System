<template>
  <div class="user-guide">
    <div class="guide-header card">
      <h1>系统使用指南</h1>
      <p>欢迎使用互联网医疗系统，本指南将帮助您快速了解系统的各项功能</p>
      <div class="guide-actions">
        <el-button type="primary" @click="startTour">开始引导漫游</el-button>
        <el-button @click="resetProgress">重置引导进度</el-button>
      </div>
    </div>

    <!-- 引导内容 -->
    <div class="guide-content">
      <el-tabs v-model="activeTab" tab-position="left" class="guide-tabs">
        <el-tab-pane v-for="section in guideSections" :key="section.key" :label="section.title" :name="section.key">
          <div class="guide-section" :id="'section-' + section.key">
            <h2>{{ section.title }}</h2>
            <p>{{ section.description }}</p>
            
            <div class="guide-steps">
              <el-timeline>
                <el-timeline-item 
                  v-for="(step, index) in section.steps" 
                  :key="index"
                  :type="getStepType(section.key, index)"
                  :color="getStepColor(section.key, index)"
                  :hollow="!isStepCompleted(section.key, index)"
                  :timestamp="step.title"
                >
                  <div class="step-content">
                    <div class="step-text">
                      <p>{{ step.content }}</p>
                    </div>
                    <div class="step-image" v-if="step.image">
                      <el-image 
                        :src="step.image" 
                        :preview-src-list="[step.image]"
                        fit="contain"
                      />
                    </div>
                    <div class="step-tips" v-if="step.tips">
                      <el-alert
                        :title="step.tips"
                        type="info"
                        :closable="false"
                        show-icon
                      />
                    </div>
                  </div>
                </el-timeline-item>
              </el-timeline>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
    
    <!-- 视频教程区域 -->
    <div class="video-tutorials card">
      <div class="card-title">视频教程</div>
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8" v-for="(video, index) in videoTutorials" :key="index">
          <el-card class="video-card">
            <div class="video-thumbnail">
              <el-image :src="video.thumbnail" fit="cover" />
              <div class="play-button">
                <el-button circle>
                  <el-icon><VideoPlay /></el-icon>
                </el-button>
              </div>
            </div>
            <div class="video-info">
              <h3>{{ video.title }}</h3>
              <p>{{ video.description }}</p>
              <span class="video-duration">{{ video.duration }}</span>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 常见问题区域 -->
    <div class="faq-section card">
      <div class="card-title">常见问题</div>
      <el-collapse>
        <el-collapse-item v-for="(faq, index) in faqs" :key="index" :title="faq.question" :name="index">
          <div>{{ faq.answer }}</div>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { VideoPlay } from '@element-plus/icons-vue'
import { driver } from 'driver.js'
import 'driver.js/dist/driver.css'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

// 当前激活标签
const activeTab = ref('system')

// 用户进度
const userProgress = ref({
  system: { current_step: 0, is_completed: false },
  appointment: { current_step: 0, is_completed: false },
  feedback: { current_step: 0, is_completed: false },
  notification: { current_step: 0, is_completed: false }
})

// 引导章节
const guideSections = ref([
  {
    key: 'system',
    title: '系统概览',
    description: '了解互联网医疗系统的整体功能和使用流程',
    steps: [
      {
        title: '欢迎页面',
        content: '登录系统后，您将看到欢迎页面，其中包含系统主要功能的导航入口。点击相应的图标可以进入对应的功能模块。',
        image: 'https://via.placeholder.com/600x350',
        tips: '您可以随时点击左上角的系统logo返回首页。'
      },
      {
        title: '个人中心',
        content: '点击右上角的头像图标，可以进入个人中心，查看和编辑您的个人信息、医疗记录等。',
        image: 'https://via.placeholder.com/600x350'
      },
      {
        title: '导航菜单',
        content: '系统顶部的导航菜单提供了快速访问各个功能模块的入口。',
        image: 'https://via.placeholder.com/600x350'
      },
      {
        title: '消息通知',
        content: '右上角的铃铛图标会显示您的未读消息数量，点击可以查看所有通知。',
        image: 'https://via.placeholder.com/600x350'
      }
    ]
  },
  {
    key: 'appointment',
    title: '预约挂号',
    description: '学习如何在系统中完成医生预约挂号流程',
    steps: [
      {
        title: '选择科室',
        content: '在预约挂号页面，首先选择您要就诊的科室。',
        image: 'https://via.placeholder.com/600x350'
      },
      {
        title: '选择医生',
        content: '根据科室筛选医生列表，可以查看医生的详细信息，包括专长、职称、出诊时间等。',
        image: 'https://via.placeholder.com/600x350'
      },
      {
        title: '选择时间',
        content: '在医生的出诊日历中，选择合适的就诊时间段。',
        image: 'https://via.placeholder.com/600x350',
        tips: '绿色表示可预约，灰色表示已约满，黄色表示即将约满。'
      },
      {
        title: '填写信息',
        content: '填写就诊人信息、联系方式和症状描述等。',
        image: 'https://via.placeholder.com/600x350'
      },
      {
        title: '确认预约',
        content: '核对预约信息无误后，点击确认预约按钮完成预约。',
        image: 'https://via.placeholder.com/600x350'
      }
    ]
  },
  {
    key: 'feedback',
    title: '用户反馈',
    description: '了解如何提交系统反馈和就诊体验反馈',
    steps: [
      {
        title: '进入反馈页面',
        content: '点击导航菜单中的"用户反馈"选项，可以进入反馈系统。',
        image: 'https://via.placeholder.com/600x350'
      },
      {
        title: '选择反馈类型',
        content: '选择您要提交的反馈类型：系统反馈、就诊体验反馈或康复情况反馈。',
        image: 'https://via.placeholder.com/600x350'
      },
      {
        title: '填写反馈内容',
        content: '根据表单提示，填写反馈评分和详细内容，可以上传相关图片作为参考。',
        image: 'https://via.placeholder.com/600x350'
      },
      {
        title: '提交反馈',
        content: '确认信息无误后，点击提交按钮完成反馈。您的反馈将帮助我们不断改进系统和服务。',
        image: 'https://via.placeholder.com/600x350'
      }
    ]
  },
  {
    key: 'notification',
    title: '消息通知',
    description: '了解系统的消息通知功能和设置',
    steps: [
      {
        title: '查看通知',
        content: '点击右上角的铃铛图标，可以查看所有通知消息。',
        image: 'https://via.placeholder.com/600x350'
      },
      {
        title: '通知类型',
        content: '系统通知包括：预约提醒、复诊提醒、检查结果通知、健康提醒等多种类型。',
        image: 'https://via.placeholder.com/600x350'
      },
      {
        title: '通知设置',
        content: '在消息中心页面，可以设置接收通知的方式，如应用内、短信、邮件等。',
        image: 'https://via.placeholder.com/600x350',
        tips: '建议至少开启一种通知方式，以免错过重要信息。'
      }
    ]
  }
])

// 视频教程
const videoTutorials = ref([
  {
    title: '系统注册登录',
    description: '了解如何注册账号并登录系统',
    thumbnail: 'https://via.placeholder.com/400x225',
    duration: '3:45'
  },
  {
    title: '预约挂号详解',
    description: '完整演示预约挂号流程',
    thumbnail: 'https://via.placeholder.com/400x225',
    duration: '5:20'
  },
  {
    title: '移动端使用指南',
    description: '在手机上使用系统的操作指南',
    thumbnail: 'https://via.placeholder.com/400x225',
    duration: '4:10'
  }
])

// 常见问题
const faqs = ref([
  {
    question: '如何修改个人信息？',
    answer: '点击右上角头像，进入个人中心，在"基本资料"选项卡中可以修改您的个人信息。'
  },
  {
    question: '预约后可以取消吗？',
    answer: '可以。在预约后24小时内，您可以在"我的预约"中找到该预约，点击"取消预约"按钮进行取消。'
  },
  {
    question: '忘记密码怎么办？',
    answer: '在登录页面点击"忘记密码"，按照提示使用手机号或邮箱验证身份后可以重置密码。'
  },
  {
    question: '如何查看检查报告？',
    answer: '在个人中心的"健康档案"选项卡中，可以查看所有的检查报告和电子病历。'
  },
  {
    question: '系统支持哪些支付方式？',
    answer: '系统支持微信支付、支付宝、银联等多种支付方式，您可以在结算时选择合适的支付方式。'
  }
])

// Driver.js实例
let driverObj = null

// 初始化引导对象
const initDriver = () => {
  driverObj = driver({
    showProgress: true,
    showButtons: ['next', 'previous', 'close'],
    steps: [
      { 
        element: '.guide-header', 
        popover: { 
          title: '欢迎使用引导漫游', 
          description: '本引导将带您了解系统的主要功能和操作流程',
          side: 'bottom',
          align: 'center'
        }
      },
      { 
        element: '.guide-tabs', 
        popover: { 
          title: '功能导航', 
          description: '左侧是系统主要功能的分类导航，点击可以查看详细指南',
          side: 'right',
          align: 'start'
        }
      },
      { 
        element: '.guide-steps', 
        popover: { 
          title: '步骤指引', 
          description: '每个功能模块都有详细的操作步骤指引，按照步骤操作即可轻松使用系统',
          side: 'bottom',
          align: 'center'
        }
      },
      { 
        element: '.video-tutorials', 
        popover: { 
          title: '视频教程', 
          description: '我们提供了详细的视频教程，帮助您更直观地了解系统操作',
          side: 'top',
          align: 'center'
        }
      },
      { 
        element: '.faq-section', 
        popover: { 
          title: '常见问题', 
          description: '这里汇总了用户常见的问题和解答，可以帮助您快速解决使用中的疑惑',
          side: 'top',
          align: 'center'
        }
      }
    ],
    onDestroyed: () => {
      // 漫游结束后更新进度
      updateGuideProgress('system', 4, true)
    }
  })
}

// 开始引导漫游
const startTour = () => {
  if (!driverObj) {
    initDriver()
  }
  driverObj.drive()
}

// 获取用户引导进度
const getUserProgress = async () => {
  try {
    // 模拟用户ID，实际应从登录状态获取
    const patientId = 1
    for (const section of Object.keys(userProgress.value)) {
      try {
        const { data } = await axios.get(`/api/guides/progress/${patientId}?guide_key=${section}`)
        if (data.status === 'success') {
          userProgress.value[section] = {
            current_step: data.data.current_step,
            is_completed: Boolean(data.data.is_completed)
          }
        }
      } catch (error) {
        console.error(`获取${section}引导进度失败:`, error)
      }
    }
  } catch (error) {
    console.error('获取引导进度失败:', error)
  }
}

// 更新引导进度
const updateGuideProgress = async (guideKey, currentStep, isCompleted = false) => {
  try {
    // 更新本地状态
    userProgress.value[guideKey] = {
      current_step: currentStep,
      is_completed: isCompleted
    }
    
    // 模拟用户ID，实际应从登录状态获取
    const patientId = 1
    
    // 发送到服务器
    await axios.post('/api/guides/progress', {
      patient_id: patientId,
      guide_key: guideKey,
      current_step: currentStep,
      is_completed: isCompleted ? 1 : 0
    })
    
  } catch (error) {
    console.error('更新引导进度失败:', error)
    ElMessage.error('更新引导进度失败')
  }
}

// 重置引导进度
const resetProgress = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要重置所有引导进度吗？这将清除您已完成的所有引导记录。',
      '重置确认',
      {
        confirmButtonText: '确定重置',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    // 重置所有引导进度
    for (const section of Object.keys(userProgress.value)) {
      await updateGuideProgress(section, 0, false)
    }
    
    ElMessage.success('引导进度已重置')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('重置引导进度失败:', error)
      ElMessage.error('重置引导进度失败')
    }
  }
}

// 获取步骤状态类型
const getStepType = (section, index) => {
  const progress = userProgress.value[section]
  if (!progress) return ''
  
  if (progress.current_step > index) {
    return 'success'
  } else if (progress.current_step === index) {
    return 'primary'
  }
  return ''
}

// 获取步骤颜色
const getStepColor = (section, index) => {
  const progress = userProgress.value[section]
  if (!progress) return ''
  
  if (progress.current_step > index) {
    return '#67C23A'
  } else if (progress.current_step === index) {
    return '#409EFF'
  }
  return ''
}

// 步骤是否完成
const isStepCompleted = (section, index) => {
  const progress = userProgress.value[section]
  if (!progress) return false
  
  return progress.current_step > index
}

onMounted(() => {
  initDriver()
  getUserProgress()
})
</script>

<style scoped>
.user-guide {
  min-height: 100vh;
  padding: var(--spacing-lg, 24px);
  background: linear-gradient(180deg, var(--bg-color, #ffffff) 0%, var(--bg-light, #f8fafe) 100%);
  overflow-y: auto;
  overflow-x: hidden;
}

.guide-header {
  text-align: center;
  margin-bottom: var(--spacing-xl, 32px);
  padding: var(--spacing-xxl, 48px) var(--spacing-xl, 32px);
  background: linear-gradient(135deg, var(--bg-light, #f8fafe) 0%, #e3f2fd 100%);
  border-radius: var(--border-radius-xl, 16px);
  box-shadow: var(--shadow-base, 0 4px 12px rgba(0, 0, 0, 0.08));
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: var(--spacing-xl, 32px);
  position: relative;
  overflow: hidden;
}

.guide-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-color, #409EFF), var(--success-color, #67C23A), var(--warning-color, #E6A23C));
}

.guide-header h1 {
  font-size: 32px;
  color: var(--text-primary, #2c3e50);
  margin-bottom: var(--spacing-md, 16px);
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-color, #409EFF) 0%, var(--success-color, #67C23A) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.guide-header p {
  font-size: 16px;
  color: var(--text-regular, #606266);
  margin-bottom: var(--spacing-lg, 24px);
  line-height: 1.6;
}

.guide-actions {
  display: flex;
  gap: var(--spacing-md, 16px);
  justify-content: center;
  flex-wrap: wrap;
}

.guide-content {
  background: var(--bg-color, #ffffff);
  border-radius: var(--border-radius-lg, 12px);
  box-shadow: var(--shadow-base, 0 4px 12px rgba(0, 0, 0, 0.08));
  margin-bottom: var(--spacing-xl, 32px);
  overflow: hidden;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: var(--spacing-xl, 32px);
}

.guide-tabs {
  min-height: 600px;
}

.guide-section {
  padding: var(--spacing-xl, 32px);
}

.guide-section h2 {
  font-size: 24px;
  color: var(--text-primary, #2c3e50);
  margin-bottom: var(--spacing-md, 16px);
  font-weight: 600;
}

.guide-section p {
  color: var(--text-regular, #606266);
  margin-bottom: var(--spacing-lg, 24px);
  line-height: 1.6;
}

.guide-steps {
  margin-top: var(--spacing-lg, 24px);
}

.step-content {
  margin-top: var(--spacing-md, 16px);
}

.step-text {
  margin-bottom: var(--spacing-md, 16px);
}

.step-text p {
  color: var(--text-regular, #606266);
  line-height: 1.6;
  margin: 0;
}

.step-image {
  margin: var(--spacing-md, 16px) 0;
  text-align: center;
}

.step-image .el-image {
  max-width: 100%;
  border-radius: var(--border-radius-md, 8px);
  box-shadow: var(--shadow-light, 0 2px 4px rgba(0, 0, 0, 0.05));
}

.step-tips {
  margin-top: var(--spacing-md, 16px);
}

.video-tutorials {
  margin-bottom: var(--spacing-xl, 32px);
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: var(--spacing-xl, 32px);
}

.video-card {
  height: 100%;
  transition: all var(--transition-base, 0.3s ease);
  border-radius: var(--border-radius-lg, 12px);
  overflow: hidden;
}

.video-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-dark, 0 8px 24px rgba(0, 0, 0, 0.12));
}

.video-thumbnail {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.video-thumbnail .el-image {
  width: 100%;
  height: 100%;
}

.play-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.8;
  transition: opacity var(--transition-fast, 0.2s ease);
}

.video-thumbnail:hover .play-button {
  opacity: 1;
}

.play-button .el-button {
  width: 60px;
  height: 60px;
  background: rgba(64, 158, 255, 0.9);
  border: none;
  color: white;
  font-size: 24px;
}

.video-info {
  padding: var(--spacing-lg, 24px);
}

.video-info h3 {
  font-size: 16px;
  color: var(--text-primary, #2c3e50);
  margin-bottom: var(--spacing-sm, 8px);
  font-weight: 600;
}

.video-info p {
  color: var(--text-regular, #606266);
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: var(--spacing-sm, 8px);
}

.video-duration {
  color: var(--text-secondary, #909399);
  font-size: 12px;
}

.faq-section {
  margin-bottom: var(--spacing-xxl, 48px);
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-guide {
    padding: var(--spacing-md, 16px);
  }
  
  .guide-header {
    padding: var(--spacing-xl, 32px) var(--spacing-lg, 24px);
  }
  
  .guide-header h1 {
    font-size: 24px;
  }
  
  .guide-header p {
    font-size: 14px;
  }
  
  .guide-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .guide-section {
    padding: var(--spacing-lg, 24px);
  }
  
  .guide-section h2 {
    font-size: 20px;
  }
  
  .guide-tabs {
    min-height: 400px;
  }
  
  :deep(.el-tabs--left .el-tabs__header) {
    width: 120px;
  }
  
  :deep(.el-tabs--left .el-tabs__content) {
    padding-left: 140px;
  }
}

@media (max-width: 480px) {
  .guide-header h1 {
    font-size: 20px;
  }
  
  .guide-section {
    padding: var(--spacing-md, 16px);
  }
  
  :deep(.el-tabs--left) {
    flex-direction: column;
  }
  
  :deep(.el-tabs--left .el-tabs__header) {
    width: 100%;
    margin-bottom: var(--spacing-md, 16px);
  }
  
  :deep(.el-tabs--left .el-tabs__content) {
    padding-left: 0;
  }
  
  :deep(.el-tabs--left .el-tabs__nav) {
    display: flex;
    overflow-x: auto;
  }
  
  .video-thumbnail {
    height: 150px;
  }
}
</style> 