<template>
  <div class="notification-center">
    <div class="page-header card">
      <h1>消息中心</h1>
      <p>查看和管理您的系统消息、预约提醒和复诊通知</p>
    </div>

    <div class="notification-container">
      <el-row :gutter="20">
        <!-- 左侧过滤栏 -->
        <el-col :xs="24" :sm="6" :md="5">
          <div class="filter-sidebar card">
            <div class="sidebar-header">
              <h3>消息类型</h3>
            </div>
            <el-menu
              :default-active="activeType"
              @select="handleTypeSelect"
              class="filter-menu"
            >
              <el-menu-item index="all">
                <el-icon><Message /></el-icon>
                <span>全部消息</span>
                <el-badge :value="totalUnread" class="badge" v-if="totalUnread > 0" />
              </el-menu-item>
              <el-menu-item index="appointment">
                <el-icon><Calendar /></el-icon>
                <span>预约提醒</span>
                <el-badge :value="getUnreadByType('appointment')" class="badge" v-if="getUnreadByType('appointment') > 0" />
              </el-menu-item>
              <el-menu-item index="medication">
                <el-icon><Timer /></el-icon>
                <span>用药提醒</span>
                <el-badge :value="getUnreadByType('medication')" class="badge" v-if="getUnreadByType('medication') > 0" />
              </el-menu-item>
              <el-menu-item index="followup">
                <el-icon><Bell /></el-icon>
                <span>复诊提醒</span>
                <el-badge :value="getUnreadByType('followup')" class="badge" v-if="getUnreadByType('followup') > 0" />
              </el-menu-item>
              <el-menu-item index="health_tip">
                <el-icon><InfoFilled /></el-icon>
                <span>健康提示</span>
                <el-badge :value="getUnreadByType('health_tip')" class="badge" v-if="getUnreadByType('health_tip') > 0" />
              </el-menu-item>
              <el-menu-item index="system">
                <el-icon><Setting /></el-icon>
                <span>系统公告</span>
                <el-badge :value="getUnreadByType('system')" class="badge" v-if="getUnreadByType('system') > 0" />
              </el-menu-item>
            </el-menu>
            
            <div class="notification-settings">
              <h3>接收设置</h3>
              <el-divider />
              <div class="settings-item">
                <span>应用内消息</span>
                <el-switch v-model="settings.app" />
              </div>
              <div class="settings-item">
                <span>短信通知</span>
                <el-switch v-model="settings.sms" />
              </div>
              <div class="settings-item">
                <span>邮件通知</span>
                <el-switch v-model="settings.email" />
              </div>
              <el-button type="primary" size="small" class="save-settings" @click="saveSettings">保存设置</el-button>
            </div>
          </div>
        </el-col>
        
        <!-- 右侧消息列表 -->
        <el-col :xs="24" :sm="18" :md="19">
          <div class="notification-list card">
            <div class="list-header">
              <div class="list-title">
                <h3>{{ getTypeTitle() }}</h3>
                <span class="total-count">共 {{ notifications.length }} 条</span>
              </div>
              <div class="list-actions">
                <el-button 
                  type="primary" 
                  plain 
                  size="small" 
                  @click="markAllAsRead" 
                  :disabled="!hasUnread"
                >
                  全部标为已读
                </el-button>
              </div>
            </div>
            
            <el-empty 
              v-if="notifications.length === 0" 
              description="暂无消息" 
            />
            
            <div v-else class="notification-items">
              <el-scrollbar height="600px">
                <transition-group name="list">
                  <div 
                    v-for="notification in notifications" 
                    :key="notification.id"
                    :class="['notification-item', { unread: notification.status !== 'read' }]"
                    @click="openNotification(notification)"
                  >
                    <div class="notification-icon">
                      <el-icon :size="24" :color="getIconColor(notification.type)">
                        <component :is="getIcon(notification.type)" />
                      </el-icon>
                    </div>
                    <div class="notification-content">
                      <div class="notification-title">
                        <span>{{ notification.title }}</span>
                        <el-tag v-if="notification.status !== 'read'" size="small" type="danger">未读</el-tag>
                      </div>
                      <div class="notification-body">{{ notification.content }}</div>
                      <div class="notification-meta">
                        <span class="notification-time">
                          <TimeAgo :datetime="notification.scheduled_time" />
                        </span>
                        <span class="notification-type">{{ getTypeName(notification.type) }}</span>
                      </div>
                    </div>
                  </div>
                </transition-group>
              </el-scrollbar>
              
              <div class="pagination-container">
                <el-pagination
                  layout="prev, pager, next"
                  :total="totalNotifications"
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
    
    <!-- 消息详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      :title="currentNotification.title"
      width="50%"
      destroy-on-close
    >
      <div class="notification-detail">
        <div class="detail-meta">
          <span class="notification-type-tag">
            <el-tag :type="getTagType(currentNotification.type)">
              {{ getTypeName(currentNotification.type) }}
            </el-tag>
          </span>
          <span class="notification-time">
            {{ formatDateTime(currentNotification.scheduled_time) }}
          </span>
        </div>
        <div class="detail-content">
          <p v-html="formatContent(currentNotification.content)"></p>
        </div>
        
        <div v-if="currentNotification.type === 'appointment' && currentNotification.reference_id" class="detail-actions">
          <el-button type="primary" @click="viewAppointment(currentNotification.reference_id)">
            查看预约详情
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'
import { 
  Message, Calendar, Timer, Bell, InfoFilled, 
  Setting
} from '@element-plus/icons-vue'

const router = useRouter()

// 消息列表
const notificationList = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const totalNotifications = ref(0)

// 消息类型筛选
const activeType = ref('all')

// 消息设置
const settings = ref({
  app: true,
  sms: true,
  email: true
})

// 详情对话框
const detailVisible = ref(false)
const currentNotification = ref({})

// 获取消息列表
const getNotifications = async () => {
  try {
    // 尝试从API获取数据
    // const response = await axios.get(`/api/notifications/${patientId}?limit=${pageSize.value}&offset=${(currentPage.value - 1) * pageSize.value}`, { timeout: 3000 })
    // if (response.data && response.data.status === 'success') {
    //   notificationList.value = response.data.data.notifications
    //   totalNotifications.value = response.data.data.total || 30
    // } else {
    //   // 使用模拟数据
    //   useMockData()
    // }
    
    // 目前使用模拟数据
    useMockData()
  } catch (error) {
    console.error('获取消息失败:', error)
    ElMessage.error('获取消息失败，使用默认数据')
    // 使用模拟数据
    useMockData()
  }
}

// 使用模拟数据
const useMockData = () => {
  const mockData = {
    status: 'success',
    data: {
      notifications: generateMockNotifications(),
      unread_count: 5
    }
  }
  
  notificationList.value = mockData.data.notifications
  totalNotifications.value = 30 // 模拟总数
}

// 模拟数据生成
const generateMockNotifications = () => {
  const notifications = []
  const types = ['appointment', 'medication', 'followup', 'health_tip', 'system']
  const statusOptions = ['read', 'sent', 'pending']
  
  for (let i = 1; i <= 20; i++) {
    const type = types[Math.floor(Math.random() * types.length)]
    const status = statusOptions[Math.floor(Math.random() * statusOptions.length)]
    const daysAgo = Math.floor(Math.random() * 10)
    
    let title, content
    
    switch (type) {
      case 'appointment':
        title = '预约提醒'
        content = `您预约的${Math.floor(Math.random() * 3) + 1}月${Math.floor(Math.random() * 30) + 1}日上午9:30内科张医生的门诊即将开始，请提前安排好时间。`
        break
      case 'medication':
        title = '用药提醒'
        content = '请按时服用医生开具的药物，每日三次，饭后服用。'
        break
      case 'followup':
        title = '复诊提醒'
        content = '根据您的病情，建议两周后复诊，请提前预约。'
        break
      case 'health_tip':
        title = '健康小贴士'
        content = '秋冬季节，昼夜温差大，请注意及时添加衣物，预防感冒。'
        break
      case 'system':
        title = '系统公告'
        content = '系统将于本周六凌晨2:00-4:00进行维护升级，期间服务可能暂时不可用。'
        break
    }
    
    notifications.push({
      id: i,
      patient_id: 1,
      title,
      content,
      type,
      reference_id: type === 'appointment' ? Math.floor(Math.random() * 10) + 1 : null,
      delivery_method: 'app,sms,email',
      status,
      scheduled_time: dayjs().subtract(daysAgo, 'day').format('YYYY-MM-DD HH:mm:ss'),
      sent_time: status !== 'pending' ? dayjs().subtract(daysAgo, 'day').format('YYYY-MM-DD HH:mm:ss') : null,
      read_time: status === 'read' ? dayjs().subtract(daysAgo, 'day').add(2, 'hour').format('YYYY-MM-DD HH:mm:ss') : null
    })
  }
  
  return notifications
}

// 过滤后的消息列表
const notifications = computed(() => {
  return notificationList.value
})

// 总未读数
const totalUnread = computed(() => {
  return notificationList.value.filter(n => n.status !== 'read').length
})

// 是否有未读消息
const hasUnread = computed(() => {
  return totalUnread.value > 0
})

// 按类型获取未读数
const getUnreadByType = (type) => {
  return notificationList.value.filter(n => n.type === type && n.status !== 'read').length
}

// 获取类型标题
const getTypeTitle = () => {
  switch (activeType.value) {
    case 'all': return '全部消息'
    case 'appointment': return '预约提醒'
    case 'medication': return '用药提醒'
    case 'followup': return '复诊提醒'
    case 'health_tip': return '健康提示'
    case 'system': return '系统公告'
    default: return '消息列表'
  }
}

// 获取类型名称
const getTypeName = (type) => {
  switch (type) {
    case 'appointment': return '预约提醒'
    case 'medication': return '用药提醒'
    case 'followup': return '复诊提醒'
    case 'health_tip': return '健康提示'
    case 'system': return '系统公告'
    default: return '其他'
  }
}

// 获取类型图标
const getIcon = (type) => {
  switch (type) {
    case 'appointment': return Calendar
    case 'medication': return Timer
    case 'followup': return Bell
    case 'health_tip': return InfoFilled
    case 'system': return Setting
    default: return Message
  }
}

// 获取图标颜色
const getIconColor = (type) => {
  switch (type) {
    case 'appointment': return '#409EFF'
    case 'medication': return '#67C23A'
    case 'followup': return '#E6A23C'
    case 'health_tip': return '#909399'
    case 'system': return '#F56C6C'
    default: return '#409EFF'
  }
}

// 获取标签类型
const getTagType = (type) => {
  switch (type) {
    case 'appointment': return 'primary'
    case 'medication': return 'success'
    case 'followup': return 'warning'
    case 'health_tip': return 'info'
    case 'system': return 'danger'
    default: return 'primary'
  }
}

// 格式化日期时间
const formatDateTime = (dateTime) => {
  return dayjs(dateTime).format('YYYY-MM-DD HH:mm:ss')
}

// 格式化内容（支持简单HTML）
const formatContent = (content) => {
  return content.replace(/\n/g, '<br>')
}

// 切换消息类型
const handleTypeSelect = (type) => {
  activeType.value = type
  currentPage.value = 1
  getNotifications()
}

// 分页切换
const handlePageChange = (page) => {
  currentPage.value = page
  getNotifications()
}

// 保存通知设置
const saveSettings = async () => {
  try {
    // 实际应该调用API保存设置
    // 模拟保存成功
    setTimeout(() => {
      ElMessage.success('设置已保存')
    }, 500)
  } catch (error) {
    console.error('保存设置失败:', error)
    ElMessage.error('保存设置失败')
  }
}

// 标记所有消息为已读
const markAllAsRead = async () => {
  try {
    // 实际应该调用API标记所有为已读
    // 模拟成功
    const updatedList = notificationList.value.map(n => ({
      ...n,
      status: 'read',
      read_time: dayjs().format('YYYY-MM-DD HH:mm:ss')
    }))
    
    notificationList.value = updatedList
    ElMessage.success('已将所有消息标记为已读')
  } catch (error) {
    console.error('标记已读失败:', error)
    ElMessage.error('操作失败')
  }
}

// 打开消息详情
const openNotification = async (notification) => {
  currentNotification.value = notification
  detailVisible.value = true
  
  // 如果消息未读，标记为已读
  if (notification.status !== 'read') {
    try {
      // 实际应该调用API标记为已读
      // 模拟成功
      const index = notificationList.value.findIndex(n => n.id === notification.id)
      if (index !== -1) {
        notificationList.value[index] = {
          ...notification,
          status: 'read',
          read_time: dayjs().format('YYYY-MM-DD HH:mm:ss')
        }
      }
    } catch (error) {
      console.error('标记已读失败:', error)
    }
  }
}

// 查看预约详情
const viewAppointment = (appointmentId) => {
  detailVisible.value = false
  // 实际应跳转到预约详情页
  router.push(`/`)
  ElMessage.info(`查看预约ID: ${appointmentId}`)
}

// 监听页面挂载
onMounted(() => {
  getNotifications()
})

// 监听类型变化
watch(activeType, () => {
  getNotifications()
})
</script>

<style scoped>
.notification-center {
  min-height: 100vh;
  padding: var(--spacing-lg, 24px);
  background: linear-gradient(180deg, var(--bg-color, #ffffff) 0%, var(--bg-light, #f8fafe) 100%);
  overflow-y: auto;
  overflow-x: hidden;
}

.notification-header {
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

.notification-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-color, #409EFF), var(--success-color, #67C23A), var(--warning-color, #E6A23C));
}

.notification-header h1 {
  font-size: 32px;
  color: var(--text-primary, #2c3e50);
  margin-bottom: var(--spacing-md, 16px);
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-color, #409EFF) 0%, var(--success-color, #67C23A) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.notification-header p {
  font-size: 16px;
  color: var(--text-regular, #606266);
  margin-bottom: var(--spacing-lg, 24px);
  line-height: 1.6;
}

.header-stats {
  display: flex;
  justify-content: center;
  gap: var(--spacing-xl, 32px);
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary-color, #409EFF);
  display: block;
  margin-bottom: var(--spacing-xs, 4px);
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary, #909399);
}

.notification-main {
  background: var(--bg-color, #ffffff);
  border-radius: var(--border-radius-lg, 12px);
  box-shadow: var(--shadow-base, 0 4px 12px rgba(0, 0, 0, 0.08));
  margin-bottom: var(--spacing-xl, 32px);
  overflow: hidden;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.notification-filters {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg, 24px);
  border-bottom: 1px solid var(--border-lighter, #EBEEF5);
  background: var(--bg-lighter, #fafbfc);
}

.filter-tabs {
  display: flex;
  gap: var(--spacing-sm, 8px);
  flex-wrap: wrap;
}

.filter-actions {
  display: flex;
  gap: var(--spacing-sm, 8px);
  flex-wrap: wrap;
}

.notification-content {
  max-height: 600px;
  overflow-y: auto;
  padding: 0;
}

.notification-list {
  min-height: 400px;
}

.notification-item {
  padding: var(--spacing-lg, 24px);
  border-bottom: 1px solid var(--border-lighter, #EBEEF5);
  cursor: pointer;
  transition: all var(--transition-fast, 0.2s ease);
}

.notification-item:hover {
  background-color: var(--bg-light, #f8fafe);
}

.notification-item.unread {
  background-color: #fef9e7;
  border-left: 4px solid var(--warning-color, #E6A23C);
}

.notification-item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-sm, 8px);
}

.notification-icon {
  margin-right: var(--spacing-sm, 8px);
  flex-shrink: 0;
}

.notification-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary, #303133);
  margin-bottom: var(--spacing-xs, 4px);
  flex: 1;
}

.notification-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm, 8px);
  flex-shrink: 0;
}

.notification-content-text {
  color: var(--text-regular, #606266);
  line-height: 1.6;
  margin-bottom: var(--spacing-sm, 8px);
}

.notification-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--text-secondary, #909399);
  font-size: 12px;
}

.notification-time {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs, 4px);
}

.notification-actions {
  display: flex;
  gap: var(--spacing-sm, 8px);
}

.pagination-wrapper {
  padding: var(--spacing-lg, 24px);
  text-align: center;
  border-top: 1px solid var(--border-lighter, #EBEEF5);
  background: var(--bg-lighter, #fafbfc);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .notification-center {
    padding: var(--spacing-md, 16px);
  }
  
  .notification-header {
    padding: var(--spacing-xl, 32px) var(--spacing-lg, 24px);
  }
  
  .notification-header h1 {
    font-size: 24px;
  }
  
  .notification-header p {
    font-size: 14px;
  }
  
  .header-stats {
    gap: var(--spacing-lg, 24px);
  }
  
  .stat-number {
    font-size: 24px;
  }
  
  .notification-filters {
    flex-direction: column;
    gap: var(--spacing-md, 16px);
    align-items: stretch;
  }
  
  .filter-tabs {
    justify-content: center;
  }
  
  .filter-actions {
    justify-content: center;
  }
  
  .notification-content {
    max-height: 500px;
  }
  
  .notification-item {
    padding: var(--spacing-md, 16px);
  }
  
  .notification-item-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm, 8px);
  }
  
  .notification-meta {
    margin-top: var(--spacing-xs, 4px);
  }
}

@media (max-width: 480px) {
  .notification-header h1 {
    font-size: 20px;
  }
  
  .header-stats {
    flex-direction: column;
    gap: var(--spacing-md, 16px);
  }
  
  .stat-number {
    font-size: 20px;
  }
  
  .filter-tabs {
    flex-direction: column;
    gap: var(--spacing-xs, 4px);
  }
  
  .notification-content {
    max-height: 400px;
  }
  
  .notification-item {
    padding: var(--spacing-sm, 8px) var(--spacing-md, 16px);
  }
  
  .notification-title {
    font-size: 14px;
  }
  
  .notification-content-text {
    font-size: 13px;
  }
}
</style> 