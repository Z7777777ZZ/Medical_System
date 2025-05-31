<template>
  <div class="user-timeline">
    <div class="page-header card">
      <h1>行为时间轴</h1>
      <p>查看您在系统中的所有活动记录</p>
    </div>

    <div class="timeline-container">
      <el-row :gutter="20">
        <!-- 左侧过滤栏 -->
        <el-col :xs="24" :sm="6" :md="5">
          <div class="filter-sidebar card">
            <div class="sidebar-header">
              <h3>活动类型</h3>
            </div>
            <el-menu
              :default-active="activeType"
              @select="handleTypeSelect"
              class="filter-menu"
            >
              <el-menu-item index="all">
                <el-icon><List /></el-icon>
                <span>全部活动</span>
              </el-menu-item>
              <el-menu-item index="login">
                <el-icon><Key /></el-icon>
                <span>登录记录</span>
              </el-menu-item>
              <el-menu-item index="appointment">
                <el-icon><Calendar /></el-icon>
                <span>预约活动</span>
              </el-menu-item>
              <el-menu-item index="feedback">
                <el-icon><ChatDotSquare /></el-icon>
                <span>反馈记录</span>
              </el-menu-item>
              <el-menu-item index="view_record">
                <el-icon><Document /></el-icon>
                <span>查看记录</span>
              </el-menu-item>
              <el-menu-item index="payment">
                <el-icon><Money /></el-icon>
                <span>支付记录</span>
              </el-menu-item>
            </el-menu>
            
            <div class="date-filter">
              <h3>日期范围</h3>
              <el-divider />
              <el-date-picker
                v-model="dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                :shortcuts="dateShortcuts"
                style="width: 100%"
                value-format="YYYY-MM-DD"
                @change="handleDateChange"
              />
            </div>
          </div>
        </el-col>
        
        <!-- 右侧时间轴 -->
        <el-col :xs="24" :sm="18" :md="19">
          <div class="timeline-content card">
            <div class="timeline-header">
              <div class="header-title">
                <h3>{{ getTypeTitle() }}</h3>
                <span class="total-count">共 {{ activities.length }} 条记录</span>
              </div>
              <div class="header-actions">
                <el-select 
                  v-model="sortOrder" 
                  size="small" 
                  placeholder="排序方式" 
                  @change="handleSortChange"
                >
                  <el-option label="最新优先" value="desc" />
                  <el-option label="最早优先" value="asc" />
                </el-select>
              </div>
            </div>
            
            <el-empty 
              v-if="activities.length === 0" 
              description="暂无活动记录" 
            />
            
            <div v-else class="timeline-list">
              <el-scrollbar height="600px">
                <div class="timeline-wrapper">
                  <el-timeline>
                    <el-timeline-item
                      v-for="(activity, index) in activities"
                      :key="index"
                      :timestamp="formatDateTime(activity.created_at)"
                      :type="getTimelineItemType(activity.activity_type)"
                      :color="getTimelineItemColor(activity.activity_type)"
                      :size="activity.important ? 'large' : 'normal'"
                      :hollow="false"
                    >
                      <div class="timeline-item-content">
                        <h4>{{ activity.description }}</h4>
                        <p v-if="activity.metadata" class="metadata">
                          {{ formatMetadata(activity.metadata) }}
                        </p>
                        <div class="activity-meta">
                          <span class="activity-type">{{ getActivityTypeName(activity.activity_type) }}</span>
                          <span class="activity-ip" v-if="activity.ip_address">IP: {{ activity.ip_address }}</span>
                        </div>
                      </div>
                    </el-timeline-item>
                  </el-timeline>
                </div>
              </el-scrollbar>
              
              <div class="pagination-container">
                <el-pagination
                  layout="prev, pager, next"
                  :total="totalActivities"
                  :page-size="pageSize"
                  :current-page="currentPage"
                  @current-change="handlePageChange"
                />
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    
    <!-- 数据分析 -->
    <div class="stats-section card">
      <div class="card-title">活动分析</div>
      <el-row :gutter="20">
        <el-col :sm="24" :md="12">
          <div class="chart-container">
            <h4>活动类型分布</h4>
            <div class="chart">
              <DoughnutChart :chart-data="typeChartData" :options="chartOptions" />
            </div>
          </div>
        </el-col>
        <el-col :sm="24" :md="12">
          <div class="chart-container">
            <h4>近期活动趋势</h4>
            <div class="chart">
              <LineChart :chart-data="trendChartData" :options="lineChartOptions" />
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { DoughnutChart, LineChart } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title } from 'chart.js'
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'
import { 
  List, Key, Calendar, ChatDotSquare, Document, 
  Money
} from '@element-plus/icons-vue'

// 注册Chart.js组件
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title)

// 活动列表
const activityList = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const totalActivities = ref(0)

// 活动类型筛选
const activeType = ref('all')

// 日期范围
const dateRange = ref([
  dayjs().subtract(30, 'day').format('YYYY-MM-DD'),
  dayjs().format('YYYY-MM-DD')
])

// 日期快捷选项
const dateShortcuts = [
  {
    text: '最近一周',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    },
  },
  {
    text: '最近一个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
      return [start, end]
    },
  },
  {
    text: '最近三个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
      return [start, end]
    },
  },
]

// 排序方式
const sortOrder = ref('desc')

// 获取活动列表
const getActivities = async () => {
  try {
    // 尝试从API获取数据
    // const response = await axios.get(`/api/activities/${patientId}?limit=${pageSize.value}&offset=${(currentPage.value - 1) * pageSize.value}`, { timeout: 3000 })
    // if (response.data && response.data.status === 'success') {
    //   activityList.value = response.data.data.activities
    //   totalActivities.value = response.data.data.total || 50
    // } else {
    //   // 使用模拟数据
    //   useMockData()
    // }
    
    // 目前使用模拟数据
    useMockData()
  } catch (error) {
    console.error('获取活动列表失败:', error)
    ElMessage.error('获取活动列表失败，使用默认数据')
    // 使用模拟数据
    useMockData()
  }
}

// 使用模拟数据
const useMockData = () => {
  const mockData = {
    status: 'success',
    data: {
      activities: generateMockActivities(),
      total: 50
    }
  }
  
  activityList.value = mockData.data.activities
  totalActivities.value = mockData.data.total
}

// 模拟数据生成
const generateMockActivities = () => {
  const activities = []
  const types = ['login', 'appointment', 'feedback', 'view_record', 'payment']
  
  for (let i = 1; i <= 20; i++) {
    const type = types[Math.floor(Math.random() * types.length)]
    const daysAgo = Math.floor(Math.random() * 30)
    
    let description, metadata
    
    switch (type) {
      case 'login':
        description = '登录系统'
        metadata = { device: ['PC', '移动端'][Math.floor(Math.random() * 2)], browser: ['Chrome', 'Safari', 'Firefox'][Math.floor(Math.random() * 3)] }
        break
      case 'appointment':
        description = ['预约了门诊', '取消了预约', '修改了预约时间'][Math.floor(Math.random() * 3)]
        metadata = { 
          doctor_name: ['张医生', '李医生', '王医生'][Math.floor(Math.random() * 3)],
          department: ['内科', '外科', '眼科'][Math.floor(Math.random() * 3)],
          appointment_time: dayjs().add(Math.floor(Math.random() * 10), 'day').format('YYYY-MM-DD HH:mm')
        }
        break
      case 'feedback':
        description = ['提交了系统反馈', '提交了就诊体验反馈', '提交了康复情况反馈'][Math.floor(Math.random() * 3)]
        metadata = { rating: Math.floor(Math.random() * 5) + 1 }
        break
      case 'view_record':
        description = ['查看了病历', '查看了检查报告', '查看了处方'][Math.floor(Math.random() * 3)]
        metadata = { 
          record_id: Math.floor(Math.random() * 1000) + 1,
          record_date: dayjs().subtract(Math.floor(Math.random() * 30), 'day').format('YYYY-MM-DD')
        }
        break
      case 'payment':
        description = '完成了支付'
        metadata = { 
          amount: (Math.random() * 1000).toFixed(2),
          payment_method: ['微信支付', '支付宝', '银联'][Math.floor(Math.random() * 3)]
        }
        break
    }
    
    activities.push({
      id: i,
      patient_id: 1,
      activity_type: type,
      description,
      metadata,
      ip_address: `192.168.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
      user_agent: 'Mozilla/5.0',
      created_at: dayjs().subtract(daysAgo, 'day').subtract(Math.floor(Math.random() * 24), 'hour').format('YYYY-MM-DD HH:mm:ss'),
      important: Math.random() > 0.8 // 随机将一些活动标记为重要
    })
  }
  
  // 排序
  if (sortOrder.value === 'asc') {
    activities.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
  } else {
    activities.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  }
  
  return activities
}

// 过滤后的活动列表
const activities = computed(() => {
  return activityList.value
})

// 饼图数据
const typeChartData = computed(() => {
  // 统计各类型活动数量
  const typeCounts = {}
  
  activityList.value.forEach(activity => {
    if (!typeCounts[activity.activity_type]) {
      typeCounts[activity.activity_type] = 0
    }
    typeCounts[activity.activity_type]++
  })
  
  const labels = []
  const data = []
  const backgroundColor = []
  
  for (const type in typeCounts) {
    labels.push(getActivityTypeName(type))
    data.push(typeCounts[type])
    backgroundColor.push(getTimelineItemColor(type))
  }
  
  return {
    labels,
    datasets: [
      {
        data,
        backgroundColor
      }
    ]
  }
})

// 线图数据（最近7天活动趋势）
const trendChartData = computed(() => {
  // 获取最近7天的日期
  const dates = []
  for (let i = 6; i >= 0; i--) {
    dates.push(dayjs().subtract(i, 'day').format('MM-DD'))
  }
  
  // 统计每天的活动数量
  const dailyCount = {}
  dates.forEach(date => {
    dailyCount[date] = 0
  })
  
  activityList.value.forEach(activity => {
    const date = dayjs(activity.created_at).format('MM-DD')
    if (dailyCount[date] !== undefined) {
      dailyCount[date]++
    }
  })
  
  return {
    labels: dates,
    datasets: [
      {
        label: '活动数量',
        data: dates.map(date => dailyCount[date]),
        borderColor: '#409EFF',
        backgroundColor: 'rgba(64, 158, 255, 0.2)',
        fill: true,
        tension: 0.4
      }
    ]
  }
})

// 图表选项
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
    }
  }
}

// 线图选项
const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        precision: 0
      }
    }
  }
}

// 获取类型标题
const getTypeTitle = () => {
  switch (activeType.value) {
    case 'all': return '全部活动'
    case 'login': return '登录记录'
    case 'appointment': return '预约活动'
    case 'feedback': return '反馈记录'
    case 'view_record': return '查看记录'
    case 'payment': return '支付记录'
    default: return '活动记录'
  }
}

// 获取活动类型名称
const getActivityTypeName = (type) => {
  switch (type) {
    case 'login': return '系统登录'
    case 'appointment': return '预约活动'
    case 'feedback': return '反馈记录'
    case 'view_record': return '查看记录'
    case 'payment': return '支付记录'
    default: return '其他活动'
  }
}

// 获取时间轴项类型
const getTimelineItemType = (type) => {
  switch (type) {
    case 'login': return 'primary'
    case 'appointment': return 'success'
    case 'feedback': return 'warning'
    case 'view_record': return 'info'
    case 'payment': return ''
    default: return ''
  }
}

// 获取时间轴项颜色
const getTimelineItemColor = (type) => {
  switch (type) {
    case 'login': return '#409EFF'
    case 'appointment': return '#67C23A'
    case 'feedback': return '#E6A23C'
    case 'view_record': return '#909399'
    case 'payment': return '#F56C6C'
    default: return '#409EFF'
  }
}

// 格式化日期时间
const formatDateTime = (dateTime) => {
  return dayjs(dateTime).format('YYYY-MM-DD HH:mm')
}

// 格式化元数据
const formatMetadata = (metadata) => {
  if (!metadata) return ''
  
  let result = ''
  for (const key in metadata) {
    // 格式化键名
    let formattedKey = key.replace(/_/g, ' ')
    formattedKey = formattedKey.charAt(0).toUpperCase() + formattedKey.slice(1)
    
    // 添加到结果
    result += `${formattedKey}: ${metadata[key]}  `
  }
  
  return result
}

// 切换活动类型
const handleTypeSelect = (type) => {
  activeType.value = type
  currentPage.value = 1
  getActivities()
}

// 处理日期变化
const handleDateChange = () => {
  currentPage.value = 1
  getActivities()
}

// 处理排序变化
const handleSortChange = () => {
  getActivities()
}

// 分页切换
const handlePageChange = (page) => {
  currentPage.value = page
  getActivities()
}

// 监听页面挂载
onMounted(() => {
  getActivities()
})

// 监听类型变化
watch(activeType, () => {
  getActivities()
})
</script>

<style scoped>
.user-timeline {
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

.timeline-container {
  margin-bottom: 30px;
}

.filter-sidebar {
  padding: 0;
  overflow: hidden;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #EBEEF5;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.filter-menu {
  border-right: none;
}

.date-filter {
  padding: 20px;
  border-top: 1px solid #EBEEF5;
}

.date-filter h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #303133;
}

.timeline-content {
  padding: 0;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #EBEEF5;
}

.header-title {
  display: flex;
  align-items: center;
}

.header-title h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.total-count {
  margin-left: 10px;
  color: #909399;
  font-size: 14px;
}

.timeline-list {
  padding: 20px;
}

.timeline-wrapper {
  padding: 0 10px;
}

.timeline-item-content h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #303133;
}

.timeline-item-content .metadata {
  color: #606266;
  margin-bottom: 10px;
  font-size: 14px;
}

.activity-meta {
  display: flex;
  justify-content: space-between;
  color: #909399;
  font-size: 12px;
}

.pagination-container {
  padding: 20px 0 0;
  display: flex;
  justify-content: center;
}

.stats-section {
  margin-bottom: 30px;
}

.chart-container {
  padding: 20px;
}

.chart-container h4 {
  margin: 0 0 20px 0;
  font-size: 16px;
  color: #303133;
  text-align: center;
}

.chart {
  height: 300px;
}

@media (max-width: 768px) {
  .filter-sidebar {
    margin-bottom: 20px;
  }
  
  .timeline-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .header-actions {
    margin-top: 10px;
    display: flex;
    justify-content: flex-end;
  }
  
  .chart-container {
    margin-bottom: 30px;
  }
}
</style> 