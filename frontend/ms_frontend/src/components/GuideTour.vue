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
      <el-step title="注册/登录" description="创建账号，安全登录平台" />
      <el-step title="完善信息" description="补充个人资料，提升服务体验" />
      <el-step title="健康日报" description="每日填写健康信息，关注身体状况" />
      <el-step title="消息推送" description="及时接收系统通知和健康提醒" />
      <el-step title="意见反馈" description="提交建议，帮助平台优化升级" />
    </el-steps>

    <el-row :gutter="24" class="guide-cards">
      <el-col :xs="24" :sm="12" :md="8">
        <el-card shadow="hover" class="feature-card">
          <el-icon class="feature-icon" style="color:#67C23A"><i class="el-icon-User"></i></el-icon>
          <h3>个人中心</h3>
          <p>管理个人信息、查看健康档案、修改密码等。</p>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8">
        <el-card shadow="hover" class="feature-card">
          <el-icon class="feature-icon" style="color:#E6A23C"><i class="el-icon-Calendar"></i></el-icon>
          <h3>健康日报</h3>
          <p>每日打卡健康状况，系统智能分析健康趋势。</p>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8">
        <el-card shadow="hover" class="feature-card">
          <el-icon class="feature-icon" style="color:#409EFF"><i class="el-icon-Bell"></i></el-icon>
          <h3>消息推送</h3>
          <p>第一时间获取系统公告、健康提醒和服务通知。</p>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8">
        <el-card shadow="hover" class="feature-card">
          <el-icon class="feature-icon" style="color:#F56C6C"><i class="el-icon-Edit"></i></el-icon>
          <h3>意见反馈</h3>
          <p>随时提交建议和问题，平台持续优化服务。</p>
        </el-card>
      </el-col>
    </el-row>

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
      step: 1
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
.guide-cards {
  margin-top: 16px;
}
.feature-card {
  margin-bottom: 24px;
  border-radius: 14px;
  text-align: center;
  transition: box-shadow 0.2s;
  min-height: 180px;
}
.feature-icon {
  font-size: 32px;
  margin-bottom: 12px;
}
.feature-card h3 {
  margin: 8px 0 6px;
  font-size: 20px;
  color: #303133;
}
.feature-card p {
  color: #606266;
  font-size: 15px;
}
</style>