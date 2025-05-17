<template>
  <div class="user-service">
    <!-- 用户信息卡片 -->
    <el-card class="user-card" shadow="always">
      <div class="user-info">
        <el-avatar src="https://picsum.photos/100" :size="80" class="user-avatar"></el-avatar>
        <div class="user-details">
          <h3>{{ username }}</h3>
          <p class="welcome-text">欢迎回到健康服务平台！</p>
          <el-button type="primary" @click="goToProfile" class="profile-button" round>
            <el-icon><User /></el-icon>
            <span>个人中心</span>
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 第一行：三个功能卡片 -->
    <div class="card-row">
      <!-- 新手引导 -->
      <el-card class="function-card" shadow="hover">
        <div class="card-icon">
          <el-icon color="#409EFF" :size="40"><Guide /></el-icon>
        </div>
        <h3>新手漫游引导</h3>
        <p class="card-desc">快速了解平台功能和使用方法</p>
        <el-button @click="startGuide" type="primary" plain round>开始引导</el-button>
      </el-card>

      <!-- 用户反馈 -->
      <el-card class="function-card" shadow="hover">
        <div class="card-icon">
          <el-icon color="#67C23A" :size="40"><ChatDotRound /></el-icon>
        </div>
        <h3>用户反馈系统</h3>
        <p class="card-desc">您的建议是我们进步的动力</p>
        <el-button @click="openFeedback" type="success" plain round>提交反馈</el-button>
      </el-card>

      <!-- 消息推送 -->
      <el-card class="function-card" shadow="hover">
        <div class="card-icon">
          <el-icon color="#909399" :size="40"><Bell /></el-icon>
        </div>
        <h3>消息推送设置</h3>
        <p class="card-desc">个性化定制您的消息推送</p>
        <el-button @click="openMessages" type="info" plain round>推送设置</el-button>
      </el-card>
    </div>

    <!-- 健康日报轮播 -->
    <div class="section-title">
      <el-icon><Calendar /></el-icon>
      <span>健康日报助手</span>
    </div>
    <el-card class="health-card" shadow="hover">
      <el-carousel height="220px" :interval="5000" type="card" motion-blur>
        <el-carousel-item v-for="(tip, index) in healthTips" :key="index">
          <div class="health-tip">
            <h3>{{ tip.title }}</h3>
            <p>{{ tip.content }}</p>
            <el-tag :type="tip.type">{{ tip.tag }}</el-tag>
          </div>
        </el-carousel-item>
      </el-carousel>
    </el-card>

    <!-- 行为时间轴 -->
    <div class="section-title">
      <el-icon><Clock /></el-icon>
      <span>行为时间轴</span>
    </div>
    <el-card class="timeline-card" shadow="hover">
      <el-timeline>
        <el-timeline-item 
          v-for="(item, index) in timeline" 
          :key="index" 
          :timestamp="item.time"
          :type="item.type"
          :color="item.color"
          :size="item.size || 'large'"
          :hollow="item.hollow"
          :icon="item.icon">
          <el-card shadow="never" class="timeline-item-card">
            <div class="timeline-content">
              <h4>{{ item.action }}</h4>
              <p v-if="item.details">{{ item.details }}</p>
              <el-tag v-if="item.status" :type="item.statusType" size="small">{{ item.status }}</el-tag>
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-card>

    <!-- 新手引导弹窗 -->
    <el-dialog v-model="showGuideDialog" title="新手引导" width="50%">
      <GuideTour />
    </el-dialog>

    <!-- 用户反馈弹窗 -->
    <el-dialog v-model="showFeedbackDialog" title="用户反馈" width="50%">
      <FeedbackSystem />
    </el-dialog>

    <!-- 消息推送弹窗 -->
    <el-dialog v-model="showMessageDialog" title="消息推送设置" width="50%">
      <MessagePush v-if="showMessageDialog" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import {
  User,
  Guide,
  ChatDotRound,
  Bell,
  Calendar,
  Clock
} from '@element-plus/icons-vue';
import GuideTour from '@/components/GuideTour.vue';
import FeedbackSystem from '@/components/FeedbackSystem.vue';
import MessagePush from '@/components/MessagePush.vue';

const username = ref('张健康');
const showGuideDialog = ref(false);
const showFeedbackDialog = ref(false);
const showMessageDialog = ref(false);

const timeline = ref([
  { 
    time: '2025-05-17 09:30', 
    action: '预约挂号成功', 
    details: '已预约王医生5月20日的门诊',
    type: 'primary',
    icon: 'CircleCheck',
    status: '已完成',
    statusType: 'success'
  },
  { 
    time: '2025-05-16 14:15', 
    action: '提交健康问卷', 
    details: '完成了本周的健康状况调查',
    type: 'success',
    icon: 'Document',
    hollow: true
  },
  { 
    time: '2025-05-15 18:45', 
    action: '查看体检报告', 
    details: '查阅了2025年春季体检结果',
    type: 'warning',
    color: '#E6A23C',
    icon: 'Tickets'
  },
  { 
    time: '2025-05-10 10:00', 
    action: '复诊提醒', 
    details: '系统提醒您需要定期复诊',
    type: 'danger',
    icon: 'AlarmClock',
    status: '待处理',
    statusType: 'danger'
  }
]);

const healthTips = ref([
  {
    title: '水分补充小贴士',
    content: '建议每天饮用6-8杯水，保持身体水分平衡。早晨起床后空腹喝一杯温水有助于促进新陈代谢。',
    tag: '每日必读',
    type: 'primary'
  },
  {
    title: '健康饮食建议',
    content: '均衡饮食应包含谷物、蔬菜水果、优质蛋白和适量乳制品。减少高油高盐高糖食品摄入。',
    tag: '营养指南',
    type: 'success'
  },
  {
    title: '运动健康提醒',
    content: '每周至少进行150分钟中等强度有氧运动，如快走、游泳或骑自行车。运动前后做好热身和拉伸。',
    tag: '运动建议',
    type: 'warning'
  },
  {
    title: '睡眠质量提升',
    content: '保持规律作息，成年人每天应保证7-9小时睡眠。睡前避免使用电子设备，创造安静舒适的睡眠环境。',
    tag: '休息建议',
    type: 'info'
  }
]);

function startGuide() {
  showGuideDialog.value = true;
}

function openFeedback() {
  showFeedbackDialog.value = true;
}

function openMessages() {
  showMessageDialog.value = true;
}

function goToProfile() {
  console.log('跳转到个人中心');
}
</script>

<style scoped>
.user-service {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.user-card {
  margin-bottom: 20px;
  border-radius: 12px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.user-info {
  display: flex;
  align-items: center;
  padding: 20px;
}

.user-avatar {
  margin-right: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.user-details h3 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.welcome-text {
  margin: 8px 0 16px;
  color: #606266;
  font-size: 14px;
}

.profile-button {
  padding: 10px 20px;
}

.card-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  gap: 20px;
}

.function-card {
  flex: 1;
  border-radius: 12px;
  transition: all 0.3s ease;
  text-align: center;
  padding: 20px;
}

.function-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.card-icon {
  margin-bottom: 15px;
}

.card-desc {
  color: #909399;
  font-size: 14px;
  margin: 10px 0 20px;
  min-height: 40px;
}

.section-title {
  display: flex;
  align-items: center;
  margin: 30px 0 15px;
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.section-title .el-icon {
  margin-right: 8px;
  font-size: 20px;
}

.health-card {
  margin-bottom: 20px;
  border-radius: 12px;
}

.health-tip {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.health-tip h3 {
  margin-top: 0;
  color: #303133;
}

.health-tip p {
  color: #606266;
  line-height: 1.6;
  margin: 10px 0;
}

.timeline-card {
  border-radius: 12px;
}

.timeline-item-card {
  border: none;
  background-color: transparent;
}

.timeline-content h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
}

.timeline-content p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .card-row {
    flex-direction: column;
  }
  
  .function-card {
    margin-bottom: 15px;
  }
}
</style>