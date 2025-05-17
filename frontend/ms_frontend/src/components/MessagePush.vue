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
      <el-table :data="limitedMessages" style="width: 100%">
        <el-table-column prop="title" label="消息标题"></el-table-column>
        <el-table-column prop="publish_time" label="日期"></el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button size="small" @click="viewMessage(scope.row.id)">查看</el-button>
            <el-button size="small" type="danger" @click="deleteMessage(scope.row.id)" style="margin-left: 8px;">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="messages.length > 3" style="text-align: center; margin-top: 16px;">
        <el-button type="text" @click="showAllMessages = !showAllMessages">
          {{ showAllMessages ? '收起' : '查看更多' }}
        </el-button>
      </div>
    </el-card>

    <!-- 消息详情弹窗 -->
    <el-dialog v-model="dialogVisible" title="消息详情" :width="'600px'">
      <div style="max-height: 400px; overflow-y: auto; overflow-x: hidden;">
        <p><strong>标题：</strong>{{ messageDetail.title }}</p>
        <p><strong>发布时间：</strong>{{ messageDetail.publish_time }}</p>
        <p><strong>内容：</strong>{{ messageDetail.content }}</p>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MessagePush',
  data() {
    return {
      receiveMessages: true,
      showChannelSetting: false,
      channels: ['站内信'],
      messages: [],
      showAllMessages: false,
      dialogVisible: false,
      messageDetail: {}
    };
  },
  computed: {
    limitedMessages() {
      return this.showAllMessages ? this.messages : this.messages.slice(0, 3);
    }
  },
  methods: {
    async fetchMessages() {
      try {
        const response = await axios.get('/api/messages'); // 更新路径
        if (response.data.success) {
          this.messages = response.data.data;
          this.updateLimitedMessages();
        } else {
          this.$message.error('获取消息列表失败');
        }
      } catch (error) {
        this.$message.error('请求失败，请稍后重试');
      }
    },
    updateLimitedMessages() {
      this.limitedMessages = this.showAllMessages ? this.messages : this.messages.slice(0, 3);
    },
    async viewMessage(id) {
      try {
        const response = await axios.get(`/api/messages/${id}`); // 更新路径
        if (response.data.success) {
          this.messageDetail = response.data.data;
          this.dialogVisible = true;
        } else {
          this.$message.error('获取消息详情失败');
        }
      } catch (error) {
        this.$message.error('请求失败，请稍后重试');
      }
    },
    async deleteMessage(id) {
      try {
        const confirm = await this.$confirm('确定要删除这条消息吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });
        if (confirm) {
          const response = await axios.delete(`/api/messages/${id}`);
          if (response.data.success) {
            this.$message.success('消息已删除');
            this.messages = this.messages.filter(message => message.id !== id);
          } else {
            this.$message.error(response.data.message || '删除失败');
          }
        }
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('请求失败，请稍后重试');
        }
      }
    }
  },
  watch: {
    showAllMessages() {
      this.updateLimitedMessages();
    }
  },
  mounted() {
    this.fetchMessages();
  }
};
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