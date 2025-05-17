<template>
  <div class="page-content">
    <h2>系统消息推送</h2>
    <el-table :data="messages" style="width: 100%">
      <el-table-column prop="title" label="消息标题"></el-table-column>
      <el-table-column prop="date" label="日期"></el-table-column>
      <el-table-column label="操作">
        <template #default>
          <el-button size="small">查看</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'MessagePush',
  data() {
    return {
      messages: [
        { title: '系统更新通知', date: '2023-05-01' },
        { title: '维护公告', date: '2023-04-28' }
      ]
    }
  }
}
</script>