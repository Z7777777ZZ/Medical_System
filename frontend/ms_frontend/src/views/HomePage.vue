<template>
  <div class="home-page">
    <!-- 欢迎区域 -->
    <div class="welcome-section card">
      <div class="welcome-content">
        <h1>欢迎使用互联网医疗系统</h1>
        <p>为您提供便捷、高效、专业的在线医疗服务</p>
        <div class="action-buttons">
          <el-button type="primary" size="large" @click="startGuide">开始使用指南</el-button>
          <el-button size="large">了解更多</el-button>
          <el-button type="info" size="large" @click="testApiConnection">测试连接</el-button>
        </div>
      </div>
      <div class="welcome-image">
        <img src="https://via.placeholder.com/400x300/e0f7fa/2c3e50?text=医生形象" alt="医生形象" />
      </div>
    </div>

    <!-- 功能区域 -->
    <div class="features-grid">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8" v-for="(feature, index) in features" :key="index">
          <el-card class="feature-card" :body-style="{ padding: '0px' }">
            <div class="feature-icon">
              <el-icon :size="40"><component :is="feature.icon" /></el-icon>
            </div>
            <div class="feature-content">
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
            </div>
            <div class="feature-link">
              <router-link :to="feature.link">
                <el-button type="text">{{ feature.buttonText }}<el-icon><ArrowRight /></el-icon></el-button>
              </router-link>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 健康贴士 -->
    <div class="health-tips card">
      <div class="card-title">每日健康贴士</div>
      <el-carousel :interval="5000" height="200px" indicator-position="outside" arrow="always">
        <el-carousel-item v-for="(tip, index) in healthTips" :key="index">
          <div class="tip-card">
            <h3>{{ tip.title }}</h3>
            <p>{{ tip.content }}</p>
            <div class="tip-source" v-if="tip.source">来源: {{ tip.source }}</div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { 
  Guide, 
  ChatDotSquare, 
  Bell, 
  Calendar, 
  Histogram, 
  Document,
  ArrowRight
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 功能列表
const features = ref([
  {
    title: '新手引导',
    description: '全面了解系统功能，轻松上手使用',
    icon: Guide,
    link: '/guide',
    buttonText: '开始引导'
  },
  {
    title: '用户反馈',
    description: '提交您的使用体验，帮助我们不断改进',
    icon: ChatDotSquare,
    link: '/feedback',
    buttonText: '去反馈'
  },
  {
    title: '消息中心',
    description: '查看系统通知、预约提醒等重要信息',
    icon: Bell,
    link: '/notifications',
    buttonText: '查看消息'
  },
  {
    title: '预约挂号',
    description: '在线预约医生，省去排队等候的烦恼',
    icon: Calendar,
    link: '/',
    buttonText: '立即预约'
  },
  {
    title: '行为时间轴',
    description: '查看您在系统中的各项活动记录',
    icon: Histogram,
    link: '/timeline',
    buttonText: '查看记录'
  },
  {
    title: '健康日报',
    description: '获取每日健康资讯和个性化健康建议',
    icon: Document,
    link: '/health-assistant',
    buttonText: '查看日报'
  }
])

// 健康贴士
const healthTips = ref([
  {
    title: '保持充足睡眠的重要性',
    content: '研究表明，成年人每晚应保持7-8小时的睡眠时间，良好的睡眠有助于提高免疫力，降低心脏病和抑郁症风险。',
    source: '中国睡眠研究会'
  },
  {
    title: '饮食均衡与健康',
    content: '每天摄入足够的蔬菜、水果和全谷物，限制高糖、高盐和加工食品的摄入，有助于维持健康体重和预防慢性疾病。',
    source: '中国营养学会'
  },
  {
    title: '适度运动的益处',
    content: '每周至少进行150分钟中等强度有氧运动，如快走、游泳或骑自行车，可以显著降低患心脏病、糖尿病和某些癌症的风险。',
    source: '世界卫生组织'
  },
  {
    title: '减轻压力的方法',
    content: '长期压力可能导致多种健康问题。尝试通过冥想、深呼吸练习或瑜伽等方式来减轻压力，保持心理健康。',
    source: '中国心理卫生协会'
  }
])

// 获取健康贴士
const getHealthTips = async () => {
  try {
    // 尝试从API获取数据
    const response = await axios.get('/api/health-tips', { timeout: 3000 })
    if (response.data && response.data.status === 'success' && response.data.data && response.data.data.length > 0) {
      healthTips.value = response.data.data
    }
  } catch (error) {
    console.error('获取健康贴士失败:', error)
    // 使用默认数据，已在上面定义
    // 不需要做其他处理，因为已经有默认数据
  }
}

// 测试API连接
const testApiConnection = async () => {
  try {
    const response = await axios.get('/api/test', { timeout: 5000 })
    if (response.data && response.data.status === 'success') {
      ElMessage.success(`API连接成功! 服务器时间: ${response.data.timestamp}`)
    } else {
      ElMessage.warning('API响应异常，请检查服务器状态')
    }
  } catch (error) {
    console.error('API连接测试失败:', error)
    ElMessage.error(`API连接失败: ${error.message || '未知错误'}`)
  }
}

// 开始引导
const startGuide = () => {
  router.push('/guide')
}

onMounted(() => {
  getHealthTips()
})
</script>

<style scoped>
.home-page {
  padding: 20px 0;
}

.welcome-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 40px;
  margin-bottom: 30px;
  background: linear-gradient(135deg, #e0f7fa 0%, #bbdefb 100%);
  border-radius: 12px;
}

.welcome-content {
  flex: 1;
}

.welcome-content h1 {
  font-size: 32px;
  margin-bottom: 20px;
  color: #2c3e50;
}

.welcome-content p {
  font-size: 18px;
  margin-bottom: 30px;
  color: #546e7a;
}

.action-buttons {
  display: flex;
  gap: 15px;
}

.welcome-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.welcome-image img {
  max-width: 100%;
  max-height: 300px;
}

.features-grid {
  margin-bottom: 30px;
}

.feature-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s;
  margin-bottom: 20px;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  background-color: #ecf5ff;
  color: #409eff;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.feature-content {
  padding: 20px;
  flex: 1;
}

.feature-content h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.feature-content p {
  color: #606266;
  line-height: 1.5;
}

.feature-link {
  padding: 0 20px 20px;
  text-align: right;
}

.health-tips {
  margin-bottom: 30px;
}

.tip-card {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.tip-card h3 {
  font-size: 20px;
  margin-bottom: 15px;
  color: #409eff;
}

.tip-card p {
  line-height: 1.6;
  color: #606266;
}

.tip-source {
  margin-top: 15px;
  text-align: right;
  font-size: 12px;
  color: #909399;
  font-style: italic;
}

@media (max-width: 768px) {
  .welcome-section {
    flex-direction: column;
    padding: 20px;
  }
  
  .welcome-content {
    margin-bottom: 30px;
    text-align: center;
  }
  
  .action-buttons {
    justify-content: center;
  }
  
  .welcome-content h1 {
    font-size: 24px;
  }
  
  .welcome-content p {
    font-size: 16px;
  }
}
</style> 