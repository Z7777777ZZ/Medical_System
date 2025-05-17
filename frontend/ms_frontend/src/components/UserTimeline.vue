<template>
  <div class="page-content">
    <h2>用户行为时间轴</h2>
    <el-timeline>
      <el-timeline-item
        v-for="(item, index) in timeline"
        :key="index"
        :timestamp="item.time"
      >
        {{ item.content }}
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script>
export default {
  name: 'UserTimeline',
  data() {
    return {
      timeline: [
        { time: '2023-05-01 09:00', content: '登录系统' },
        { time: '2023-05-01 10:30', content: '查看新手引导' },
        { time: '2023-05-01 14:15', content: '提交反馈' }
      ]
    }
  }
}
</script>