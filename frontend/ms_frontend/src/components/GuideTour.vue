<template>
  <div class="page-content">
    <el-card class="guide-header" shadow="hover">
      <div class="header-content">
        <el-icon style="font-size:32px;color:#409EFF;margin-right:12px;"><i class="el-icon-Guide"></i></el-icon>
        <div>
          <h2 style="margin:0;">新手引导漫游系统</h2>
          <p class="subtitle">欢迎来到医疗服务平台，跟随指引快速上手！</p>
        </div>
      </div>
    </el-card>

    <el-steps :active="step" finish-status="success" align-center style="margin:32px 0;">
      <el-step v-for="(item, idx) in steps" :key="item.title" :title="item.title" :description="item.description" @click="showGuide(idx)" style="cursor:pointer;" />
    </el-steps>

    <div v-if="currentGuide" class="guide-detail-area">
      <el-card shadow="never" style="margin-bottom: 24px;">
        <h3 style="color:#409EFF;margin-bottom:8px;">{{ currentGuide.title }}</h3>
        <p style="font-size:16px;line-height:1.8;">{{ currentGuide.detail }}</p>
        <div v-if="step === 1" class="guide-extra">
          <el-alert title="建议使用常用手机号或邮箱注册，便于找回密码。" type="info" show-icon style="margin-bottom:12px;" />
          <el-tag type="success">支持第三方登录</el-tag>
          <p style="margin-top:10px;color:#888;">注册后可享受平台全部功能，信息安全有保障。</p>
        </div>
        <div v-else-if="step === 2" class="guide-extra">
          <el-alert title="完善资料可获得更精准的健康建议。" type="success" show-icon style="margin-bottom:12px;" />
          <el-tag>个人信息仅自己可见</el-tag>
          <p style="margin-top:10px;color:#888;">请如实填写健康档案，方便医生为您提供服务。</p>
        </div>
        <div v-else-if="step === 3" class="guide-extra">
          <el-alert title="每日健康打卡，关注身体变化。" type="warning" show-icon style="margin-bottom:12px;" />
          <el-tag type="info">可设置健康提醒</el-tag>
          <p style="margin-top:10px;color:#888;">健康日报数据将用于生成健康趋势图。</p>
        </div>
        <div v-else-if="step === 4" class="guide-extra">
          <el-alert title="开启推送，重要消息不错过。" type="info" show-icon style="margin-bottom:12px;" />
          <el-tag type="danger">支持多种推送方式</el-tag>
          <p style="margin-top:10px;color:#888;">可在“消息推送”页面自定义推送设置。</p>
        </div>
        <div v-else-if="step === 5" class="guide-extra">
          <el-alert title="您的建议是我们前进的动力！" type="success" show-icon style="margin-bottom:12px;" />
          <el-tag type="primary">反馈可匿名提交</el-tag>
          <p style="margin-top:10px;color:#888;">遇到问题或有建议，欢迎随时反馈，我们会及时处理。</p>
        </div>
      </el-card>
    </div>

    <el-alert
      title="温馨提示：如有疑问可随时点击右下角客服按钮咨询！"
      type="info"
      show-icon
      style="margin:32px 0 0 0;"
    />
  </div>
</template>

<script>
export default {
  name: 'GuideTour',
  data() {
    return {
      step: 1,
      steps: [
        {
          title: '注册/登录',
          description: '创建账号，安全登录平台',
          detail: '点击右上角“注册/登录”按钮，输入手机号或邮箱，设置密码即可完成注册。已有账号可直接登录。'
        },
        {
          title: '完善信息',
          description: '补充个人资料，提升服务体验',
          detail: '进入个人中心，补充姓名、性别、年龄等信息，完善健康档案，享受个性化服务。'
        },
        {
          title: '健康日报',
          description: '每日填写健康信息，关注身体状况',
          detail: '在“健康日报”页面，每日打卡体温、症状等健康信息，系统将智能分析健康趋势。'
        },
        {
          title: '消息推送',
          description: '及时接收系统通知和健康提醒',
          detail: '开启消息推送后，您将第一时间收到系统公告、健康提醒和服务通知。'
        },
        {
          title: '意见反馈',
          description: '提交建议，帮助平台优化升级',
          detail: '如有建议或遇到问题，可在“意见反馈”页面提交，平台会及时处理并持续优化服务。'
        }
      ],
      currentGuide: null
    }
  },
  created() {
  this.currentGuide = this.steps[0]
  },
  methods: {
    showGuide(idx) {
      this.currentGuide = this.steps[idx]
      this.step = idx + 1
    }
  }
}
</script>

<style scoped>
.page-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 32px 16px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8f0fe 100%);
  min-height: 100vh;
}
.guide-header {
  margin-bottom: 32px;
  background: linear-gradient(90deg, #e0f7fa 0%, #f5f7fa 100%);
  border-radius: 16px;
}
.header-content {
  display: flex;
  align-items: center;
}
.subtitle {
  color: #909399;
  font-size: 15px;
  margin-top: 4px;
}
.guide-detail-area {
  margin-top: 16px;
}
.el-card {
  border-radius: 14px;
}
.el-card h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}
.el-card p {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
}
.guide-extra {
  margin-top: 16px;
}
</style>