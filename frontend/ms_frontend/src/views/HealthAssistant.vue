<template>
  <div class="health-assistant">
    <div class="page-header card">
      <h1>健康日报助手</h1>
      <p>每日健康资讯和个性化健康建议</p>
    </div>

    <div class="daily-container">
      <el-row :gutter="20">
        <!-- 左侧健康日报 -->
        <el-col :xs="24" :md="16">
          <div class="daily-report card">
            <div class="card-title">今日健康日报</div>
            
            <!-- 日期显示 -->
            <div class="date-display">
              <span class="today-date">{{ formatDate(currentDate) }}</span>
              <span class="weather" v-if="weather">
                <el-icon><Sunny /></el-icon> {{ weather.temperature }}°C {{ weather.description }}
              </span>
            </div>
            
            <!-- 健康状态 -->
            <div class="health-status-section">
              <h3>健康状态</h3>
              <el-row :gutter="20">
                <el-col :span="6" v-for="(item, index) in healthStatus" :key="index">
                  <div class="status-card">
                    <el-progress 
                      type="dashboard" 
                      :percentage="item.value" 
                      :color="item.color"
                      :stroke-width="8"
                    >
                      <template #default>
                        <div class="progress-content">
                          <el-icon :size="20"><component :is="item.icon" /></el-icon>
                          <span>{{ item.value }}{{ item.unit }}</span>
                        </div>
                      </template>
                    </el-progress>
                    <div class="status-label">{{ item.label }}</div>
                  </div>
                </el-col>
              </el-row>
            </div>
            
            <!-- 健康建议 -->
            <div class="health-advice-section">
              <h3>健康建议</h3>
              <el-card class="advice-card">
                <div class="advice-content">
                  <p>{{ personalizedAdvice }}</p>
                </div>
              </el-card>
            </div>
            
            <!-- 医院资讯 -->
            <div class="hospital-news-section">
              <h3>医院资讯</h3>
              <el-timeline>
                <el-timeline-item
                  v-for="(activity, index) in activities"
                  :key="index"
                  :timestamp="activity.timestamp"
                  :color="activity.color"
                >
                  {{ activity.content }}
                </el-timeline-item>
              </el-timeline>
            </div>
          </div>
        </el-col>
        
        <!-- 右侧健康贴士和广告 -->
        <el-col :xs="24" :md="8">
          <!-- 今日贴士 -->
          <div class="daily-tips card">
            <div class="card-title">今日健康贴士</div>
            <div class="tip-content">
              <div class="tip-icon">
                <el-icon :size="40" color="#409EFF"><Light /></el-icon>
              </div>
              <div class="tip-text">
                <h3>{{ dailyTip.title }}</h3>
                <p>{{ dailyTip.content }}</p>
              </div>
            </div>
          </div>
          
          <!-- 广告区域 -->
          <div class="ad-section">
            <el-carousel 
              height="200px" 
              indicator-position="outside"
              :interval="4000"
              class="ad-carousel"
            >
              <el-carousel-item v-for="(ad, index) in advertisements" :key="index">
                <div class="ad-item" @click="openAdvertisement(ad)">
                  <el-image 
                    :src="ad.image" 
                    fit="cover"
                    class="ad-image"
                  />
                  <div class="ad-overlay">
                    <span class="ad-title">{{ ad.title }}</span>
                    <span class="ad-tag">广告</span>
                  </div>
                </div>
              </el-carousel-item>
            </el-carousel>
          </div>
          
          <!-- 健康文章 -->
          <div class="articles-section card">
            <div class="card-title">精选健康文章</div>
            <div class="article-list">
              <div 
                v-for="(article, index) in healthArticles" 
                :key="index"
                class="article-item"
                @click="openArticle(article)"
              >
                <div class="article-content">
                  <h4>{{ article.title }}</h4>
                  <div class="article-meta">
                    <span>{{ article.source }}</span>
                    <span>{{ article.date }}</span>
                  </div>
                </div>
                <div class="article-image">
                  <el-image 
                    :src="article.image" 
                    fit="cover"
                  />
                </div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    
    <!-- 文章详情对话框 -->
    <el-dialog
      v-model="articleDialogVisible"
      :title="currentArticle.title"
      width="60%"
      destroy-on-close
    >
      <div class="article-dialog-content">
        <div class="article-dialog-meta">
          <span>{{ currentArticle.source }}</span>
          <span>{{ currentArticle.date }}</span>
        </div>
        <div class="article-dialog-body">
          <div class="article-image-large">
            <el-image 
              :src="currentArticle.image" 
              fit="cover"
            />
          </div>
          <div v-html="currentArticle.content" class="article-content-full"></div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Sunny, Light } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

// 当前日期
const currentDate = ref(new Date())

// 天气信息
const weather = ref({
  temperature: 18,
  description: '晴朗'
})

// 个人健康状态
const healthStatus = ref([
  {
    label: '睡眠',
    value: 87,
    unit: '%',
    icon: 'Moon',
    color: '#409EFF'
  },
  {
    label: '活动',
    value: 65,
    unit: '%',
    icon: 'Lightning',
    color: '#67C23A'
  },
  {
    label: '饮食',
    value: 72,
    unit: '%',
    icon: 'Medal',
    color: '#E6A23C'
  },
  {
    label: '情绪',
    value: 90,
    unit: '%',
    icon: 'Watch',
    color: '#F56C6C'
  }
])

// 个性化健康建议
const personalizedAdvice = ref('您今天的睡眠质量较好，但近期的运动量略有不足。建议今天多安排一些户外活动，增加身体活动量。中午饮食请注意减少高油脂食物摄入，多补充蔬菜水果。午后工作压力较大时，可以适当进行5-10分钟的休息和伸展。')

// 医院活动信息
const activities = ref([
  {
    content: '本周六上午9:00-11:00将举办"高血压健康讲座"，欢迎参加',
    timestamp: '2023-11-25 09:00',
    color: '#409EFF'
  },
  {
    content: '流感疫苗接种活动正在进行中，请有需要的患者前往2楼预防接种门诊',
    timestamp: '2023-11-20 - 2023-12-10',
    color: '#67C23A'
  },
  {
    content: '系统将于本周日凌晨2:00-4:00进行维护升级，请提前安排相关业务办理时间',
    timestamp: '2023-11-26 02:00',
    color: '#E6A23C'
  }
])

// 今日健康贴士
const dailyTip = ref({
  title: '预防颈椎病的小技巧',
  content: '长时间伏案工作后，可以做颈部拉伸运动：双手十指交叉放在脑后，向上托举头部10秒；向左右缓慢转动头部各5次；向前后轻轻牵拉颈部各5次。每隔1小时做一次，可以有效缓解颈部疲劳。'
})

// 广告数据
const advertisements = ref([
  {
    title: '秋冬养生套餐特惠',
    image: 'https://via.placeholder.com/400x200',
    link: 'https://example.com/ad1',
    tag: '活动'
  },
  {
    title: '新型健康监测手环',
    image: 'https://via.placeholder.com/400x200',
    link: 'https://example.com/ad2',
    tag: '产品'
  },
  {
    title: '中医养生保健课程',
    image: 'https://via.placeholder.com/400x200',
    link: 'https://example.com/ad3',
    tag: '课程'
  }
])

// 健康文章
const healthArticles = ref([
  {
    title: '秋冬季节如何科学预防感冒',
    image: 'https://via.placeholder.com/100x100',
    source: '健康时报',
    date: '2023-11-20',
    content: '<p>随着气温逐渐降低，感冒高发季节已经到来。预防感冒，除了常规的勤洗手、戴口罩、多饮水外，还有哪些科学有效的方法呢？</p><p>首先，保持充足的睡眠非常重要。研究表明，睡眠不足会降低免疫系统功能，使人更容易感染病毒。成年人应每晚保持7-8小时的高质量睡眠。</p><p>其次，均衡饮食和适当补充维生素也是提高免疫力的关键。增加富含维生素C的食物摄入，如柑橘类水果、猕猴桃、红椒等。适量补充维生素D也有助于增强免疫系统。</p><p>此外，规律的适度运动可以促进血液循环，增强身体抵抗力。每周至少进行150分钟的中等强度有氧运动，如快走、慢跑、游泳等。</p><p>保持室内空气流通也很重要。即使在寒冷的季节，也应每天开窗通风1-2次，每次15-30分钟，以减少室内病毒和细菌的浓度。</p><p>最后，学会管理压力也是预防感冒的重要一环。长期的精神压力会导致体内应激激素水平升高，抑制免疫系统功能。可以通过冥想、深呼吸、瑜伽等方式来缓解压力。</p>'
  },
  {
    title: '每天8000步真的是最健康的吗？',
    image: 'https://via.placeholder.com/100x100',
    source: '医学研究周刊',
    date: '2023-11-15',
    content: '<p>近年来，"每天走10000步"的目标被广泛推广，但这个数字真的有科学依据吗？最新研究表明，健康收益与步数之间并非简单的线性关系。</p><p>美国一项涉及20000名参与者的大型研究发现，对于大多数成年人，每天步行6000-8000步就能带来显著的健康益处，包括降低心血管疾病风险和全因死亡率。步数超过8000后，额外的健康收益逐渐减少。</p><p>对于老年人(65岁以上)，每天4000-6000步可能更为合适。而年轻人可能需要更多的身体活动，建议每天达到8000-10000步。</p><p>值得注意的是，步行速度和强度也很重要。快步走比慢速散步能提供更多的健康益处。每周进行150分钟中等强度的有氧运动依然是权威健康机构的建议。</p><p>总之，虽然10000步并非"神奇数字"，但增加日常身体活动量对健康确实益处多多。根据自己的年龄和身体状况，设定合理的步数目标，并在日常生活中多走动，才是最健康的生活方式。</p>'
  },
  {
    title: '膳食纤维：被忽视的营养素',
    image: 'https://via.placeholder.com/100x100',
    source: '营养学报',
    date: '2023-11-10',
    content: '<p>在我们关注蛋白质、脂肪、碳水化合物等主要营养素的同时，膳食纤维常常被忽视。然而，充足的膳食纤维摄入对健康至关重要。</p><p>膳食纤维是植物食物中不能被人体消化酶分解的部分。虽然它不提供能量，但对消化系统健康有着重要影响。膳食纤维可分为可溶性和不可溶性两种，两者对健康都有独特的益处。</p><p>可溶性纤维能吸收水分形成凝胶状物质，有助于降低血液中的胆固醇和稳定血糖。不可溶性纤维则增加粪便体积，促进肠道蠕动，预防便秘。</p><p>研究表明，高纤维饮食与多种慢性疾病风险降低相关，包括心脏病、2型糖尿病、某些癌症(尤其是结肠癌)以及肥胖。此外，膳食纤维还能滋养肠道有益菌群，增强肠道健康和免疫功能。</p><p>成年人每天应摄入25-30克膳食纤维，但大多数人的摄入量只有推荐量的一半。增加全谷物、豆类、水果、蔬菜和坚果的摄入是提高膳食纤维摄入量的最佳方式。</p><p>值得注意的是，如果你目前的膳食纤维摄入量较低，应逐渐增加，同时增加水分摄入，以避免消化不适。</p>'
  }
])

// 文章对话框
const articleDialogVisible = ref(false)
const currentArticle = ref({})

// 格式化日期
const formatDate = (date) => {
  return dayjs(date).format('YYYY年MM月DD日 dddd')
}

// 获取天气信息
const getWeather = async () => {
  try {
    // 实际应通过API获取
    // 模拟数据
    setTimeout(() => {
      weather.value = {
        temperature: Math.floor(Math.random() * 10) + 15, // 15-25度之间
        description: ['晴朗', '多云', '小雨', '阴天'][Math.floor(Math.random() * 4)]
      }
    }, 300)
  } catch (error) {
    console.error('获取天气信息失败:', error)
  }
}

// 获取健康贴士
const getHealthTips = async () => {
  try {
    // 实际应通过API获取
    // 模拟数据已经在上面定义
  } catch (error) {
    console.error('获取健康贴士失败:', error)
  }
}

// 打开文章详情
const openArticle = (article) => {
  currentArticle.value = article
  articleDialogVisible.value = true
}

// 打开广告链接
const openAdvertisement = (ad) => {
  // 实际应该跳转或显示详情
  window.open(ad.link, '_blank')
}

onMounted(() => {
  getWeather()
  getHealthTips()
})
</script>

<style scoped>
.health-assistant {
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

.daily-container {
  margin-bottom: 30px;
}

.daily-report, .daily-tips, .articles-section {
  margin-bottom: 20px;
}

.date-display {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px dashed #EBEEF5;
}

.today-date {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.weather {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #606266;
}

.health-status-section, .health-advice-section, .hospital-news-section {
  margin-bottom: 30px;
}

.health-status-section h3, .health-advice-section h3, .hospital-news-section h3 {
  margin-bottom: 15px;
  font-size: 18px;
  color: #303133;
}

.status-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.progress-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.status-label {
  margin-top: 10px;
  color: #606266;
}

.advice-card {
  background-color: #f0f9ff;
  border: none;
}

.advice-content {
  padding: 10px;
  line-height: 1.6;
  color: #606266;
}

.daily-tips {
  background-color: #f0f9ff;
}

.tip-content {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 15px 0;
}

.tip-icon {
  flex-shrink: 0;
}

.tip-text h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #303133;
}

.tip-text p {
  color: #606266;
  line-height: 1.6;
}

.ad-section {
  margin-bottom: 20px;
}

.ad-carousel {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.ad-item {
  position: relative;
  height: 100%;
  cursor: pointer;
}

.ad-image {
  width: 100%;
  height: 100%;
}

.ad-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
  padding: 15px;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ad-title {
  font-size: 16px;
  font-weight: bold;
}

.ad-tag {
  background-color: rgba(0,0,0,0.5);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.article-item {
  display: flex;
  padding: 10px 0;
  border-bottom: 1px solid #EBEEF5;
  cursor: pointer;
}

.article-item:last-child {
  border-bottom: none;
}

.article-content {
  flex: 1;
  padding-right: 15px;
}

.article-content h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #303133;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  color: #909399;
  font-size: 12px;
}

.article-image {
  width: 80px;
  height: 80px;
  border-radius: 4px;
  overflow: hidden;
  flex-shrink: 0;
}

.article-dialog-content {
  padding: 20px 0;
}

.article-dialog-meta {
  display: flex;
  justify-content: space-between;
  color: #909399;
  font-size: 14px;
  margin-bottom: 20px;
}

.article-image-large {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
  max-height: 300px;
}

.article-content-full {
  line-height: 1.8;
  color: #303133;
}

.article-content-full p {
  margin-bottom: 15px;
}

@media (max-width: 768px) {
  .status-card {
    margin-bottom: 20px;
  }
  
  .tip-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .article-item {
    align-items: center;
  }
}
</style> 