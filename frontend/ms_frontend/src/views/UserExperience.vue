<template>
  <div class="user-service">
    <!-- 用户信息卡片 -->
    <el-card class="user-card" shadow="hover">
      <div class="user-info">
        <el-avatar src="https://picsum.photos/100" :size="90" class="user-avatar"></el-avatar>
        <div class="user-details">
          <h3>{{ username }}</h3>
          <p class="welcome-text">欢迎回到健康服务平台！</p>
          <el-button type="primary" @click="goToProfile" class="profile-button" :icon="User" round>
            个人中心
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 功能卡片区域 -->
    <div class="card-row">
      <el-card 
        v-for="(card, index) in functionCards" 
        :key="index"
        class="function-card" 
        shadow="hover"
      >
        <div class="card-icon">
          <el-icon :color="card.color" :size="40">
            <component :is="card.icon" />
          </el-icon>
        </div>
        <h3>{{ card.title }}</h3>
        <p class="card-desc">{{ card.description }}</p>
        <el-button 
          :type="card.buttonType" 
          @click="card.action" 
          :icon="card.icon"
          plain 
          round
        >
          {{ card.buttonText }}
        </el-button>
      </el-card>
    </div>

    <!-- 健康日报轮播 -->
    <div class="section-title">
      <el-icon><Calendar /></el-icon>
      <span>健康日报助手</span>
    </div>
    <el-card class="health-card" shadow="hover">
      <el-carousel 
        height="360px" 
        :interval="6000" 
        type="card" 
        :autoplay="true"
        trigger="click"
      >
        <el-carousel-item v-for="(tip, index) in healthTips" :key="index">
          <div class="health-tip" :style="{ backgroundImage: `url(${tip.image})` }">
            <div class="health-tip-content">
              <h3>{{ tip.title }}</h3>
              <p>{{ tip.content }}</p>
              <el-tag :type="tip.type" effect="light" round>{{ tip.tag }}</el-tag>
            </div>
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

    <!-- Dialog components -->
    <el-dialog 
      v-model="showGuideDialog" 
      title="新手引导" 
      width="60%" 
      destroy-on-close 
      :show-close="true"
    >
      <GuideTour @close="showGuideDialog = false" />
    </el-dialog>

    <el-dialog 
      v-model="showFeedbackDialog" 
      title="用户反馈" 
      width="50%" 
      destroy-on-close
      :show-close="true"
    >
      <FeedbackSystem @close="showFeedbackDialog = false" />
    </el-dialog>

    <el-dialog 
      v-model="showMessageDialog" 
      title="消息推送设置" 
      width="50%" 
      destroy-on-close
      :show-close="true"
    >
      <MessagePush @close="showMessageDialog = false" />
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

// 功能卡片数据
const functionCards = ref([
  {
    title: '新手漫游引导',
    description: '快速了解平台功能和使用方法',
    icon: Guide,
    color: '#409EFF',
    buttonType: 'primary',
    buttonText: '开始引导',
    action: () => showGuideDialog.value = true
  },
  {
    title: '用户反馈系统',
    description: '您的建议是我们进步的动力',
    icon: ChatDotRound,
    color: '#67C23A',
    buttonType: 'success',
    buttonText: '提交反馈',
    action: () => showFeedbackDialog.value = true
  },
  {
    title: '消息推送设置',
    description: '个性化定制您的消息推送',
    icon: Bell,
    color: '#909399',
    buttonType: 'info',
    buttonText: '推送设置',
    action: () => showMessageDialog.value = true
  }
]);

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
    type: 'primary',
    image: 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?ixlib=rb-4.0.3'
  },
  {
    title: '健康饮食建议',
    content: '均衡饮食应包含谷物、蔬菜水果、优质蛋白和适量乳制品。减少高油高盐高糖食品摄入。',
    tag: '营养指南',
    type: 'success',
    image: 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-4.0.3'
  },
  {
    title: '运动健康提醒',
    content: '每周至少进行150分钟中等强度有氧运动，如快走、游泳或骑自行车。运动前后做好热身和拉伸。',
    tag: '运动建议',
    type: 'warning',
    image: 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?ixlib=rb-4.0.3'
  },
  {
    title: '睡眠质量提升',
    content: '保持规律作息，成年人每天应保证7-9小时睡眠。睡前避免使用电子设备，创造安静舒适的睡眠环境。',
    tag: '休息建议',
    type: 'info',
    image: 'data:image/webp;base64,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'
  }
]);

function goToProfile() {
  console.log('跳转到个人中心');
}
</script>

<style scoped>
:root {
  --primary-color: #409EFF;
  --success-color: #67C23A;
  --info-color: #909399;
  --text-primary: #303133;
  --text-regular: #606266;
  --text-secondary: #909399;
}

.user-service {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* 用户卡片样式 */
.user-card {
  margin-bottom: 24px;
  border-radius: 16px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.user-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.user-info {
  display: flex;
  align-items: center;
  padding: 24px;
}

.user-avatar {
  margin-right: 24px;
  border: 3px solid #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.user-avatar:hover {
  transform: scale(1.05);
}

.user-details h3 {
  margin: 0;
  font-size: 28px;
  color: var(--text-primary);
  font-weight: 600;
}

.welcome-text {
  margin: 12px 0 20px;
  color: var(--text-regular);
  font-size: 16px;
}

.profile-button {
  padding: 12px 24px;
  font-weight: 500;
  transition: all 0.3s ease;
}

/* 功能卡片区域 */
.card-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.function-card {
  border-radius: 16px;
  transition: all 0.3s ease;
  text-align: center;
  padding: 24px;
  background: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.function-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.card-icon {
  margin-bottom: 20px;
  padding: 16px;
  background: rgba(64, 158, 255, 0.1);
  border-radius: 50%;
  display: inline-block;
}

.card-desc {
  color: var(--text-secondary);
  font-size: 15px;
  margin: 16px 0 24px;
  line-height: 1.6;
}

/* 健康日报区域 */
.section-title {
  display: flex;
  align-items: center;
  margin: 40px 0 20px;
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
}

.section-title .el-icon {
  margin-right: 12px;
  font-size: 24px;
  color: var(--primary-color);
}

.health-card {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.health-tip {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  background-size: cover;
  background-position: center;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
}

.health-tip::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.7));
  z-index: 1;
}

.health-tip-content {
  position: relative;
  z-index: 2;
  padding: 32px;
  color: #fff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.health-tip-content h3 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.health-tip-content p {
  margin: 16px 0;
  font-size: 16px;
  line-height: 1.6;
  opacity: 0.9;
}

/* 时间轴样式 */
.timeline-card {
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.timeline-item-card {
  background-color: #f5f7fa;
  border-radius: 12px;
  margin: 8px 0;
  transition: all 0.3s ease;
}

.timeline-item-card:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.timeline-content h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.timeline-content p {
  margin: 0;
  color: var(--text-regular);
  font-size: 14px;
  line-height: 1.6;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-service {
    padding: 16px;
  }

  .card-row {
    grid-template-columns: 1fr;
  }

  .user-info {
    flex-direction: column;
    text-align: center;
  }

  .user-avatar {
    margin: 0 0 16px 0;
  }

  .health-tip-content {
    padding: 24px;
  }

  .health-tip-content h3 {
    font-size: 20px;
  }

  .health-tip-content p {
    font-size: 14px;
  }
}
</style>