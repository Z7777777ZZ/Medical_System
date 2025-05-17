<template>
  <div class="page-content">
    <h2>系统消息推送</h2>
    <!-- 消息接收设置模块 -->
    <el-card class="setting-card">
      <div class="setting-row">
        <span>接收系统消息：</span>
        <el-switch v-model="receiveMessages" active-text="开启" inactive-text="关闭" />
        <el-button type="primary" size="small" @click="showChannelSetting = !showChannelSetting" style="margin-left: 16px;">
          {{ showChannelSetting ? '收起推送方式' : '管理推送方式' }}
        </el-button>
      </div>
      <div class="channels">
        <span>当前推送方式：</span>
        <el-tag v-for="channel in channels" :key="channel" style="margin-right: 8px;">{{ channel }}</el-tag>
      </div>
      <el-card v-show="showChannelSetting" class="channel-setting-card" shadow="never">
        <el-checkbox-group v-model="channels">
          <el-checkbox label="站内信">站内信</el-checkbox>
          <el-checkbox label="短信">短信</el-checkbox>
          <el-checkbox label="邮件">邮件</el-checkbox>
        </el-checkbox-group>
      </el-card>
    </el-card>

    <!-- 消息列表模块 -->
    <el-card class="msg-list-card">
      <el-table :data="messages" style="width: 100%">
        <el-table-column prop="title" label="消息标题"></el-table-column>
        <el-table-column prop="date" label="日期"></el-table-column>
        <el-table-column label="操作">
          <template #default>
            <el-button size="small">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'MessagePush',
  data() {
    return {
      receiveMessages: true,
      showChannelSetting: false,
      channels: ['站内信'],
      messages: [
        { title: '系统更新通知', date: '2023-05-01' },
        { title: '维护公告', date: '2023-04-28' }
      ]
    }
  }
}
</script>

<style scoped>
.page-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 32px 16px;
}
.setting-card {
  margin-bottom: 24px;
}
.setting-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}
.channels {
  margin-top: 8px;
}
.channel-setting-card {
  margin-top: 12px;
  background: #f9fafc;
  border: 1px solid #ebeef5;
}
.msg-list-card {
  margin-top: 24px;
}
</style>