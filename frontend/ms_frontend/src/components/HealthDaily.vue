<template>
  <div class="page-content">
    <h2>健康日报助手</h2>
    <el-card>
      <el-form>
        <el-form-item label="今日步数">
          <el-input-number v-model="steps"></el-input-number>
        </el-form-item>
        <el-form-item label="饮水量(ml)">
          <el-input-number v-model="water"></el-input-number>
        </el-form-item>
        <el-form-item label="睡眠时间(h)">
          <el-input-number v-model="sleep" :precision="1"></el-input-number>
        </el-form-item>
        <el-button type="primary">提交日报</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'HealthDaily',
  data() {
    return {
      steps: 0,
      water: 0,
      sleep: 0
    }
  }
}
</script>