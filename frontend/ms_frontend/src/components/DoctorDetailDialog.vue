<template>
  <el-dialog v-model="visible" title="医生详情" width="50%">
    <div v-if="doctor">
      <div style="display: flex; margin-bottom: 20px;">
        <div style="flex: 1;">
          <h3>{{ doctor.name }}</h3>
          <p><strong>医院:</strong> {{ doctor.hospital }}</p>
          <p><strong>科室:</strong> {{ doctor.department }}</p>
          <p><strong>专长:</strong> {{ doctor.specialty }}</p>
          <p><strong>电话:</strong> {{ doctor.phone }}</p>
          
          <!-- 评分展示 -->
          <div style="margin-top: 10px;">
            <el-rate 
              v-model="doctor.average_rating" 
              disabled 
              show-score 
              text-color="#ff9900" 
              :score-template="`${doctor.average_rating.toFixed(1)} 分`"
            />
            <span style="margin-left: 10px; color: #999;">
              ({{ doctor.review_count || 0 }}条评价)
            </span>
          </div>
        </div>
        <div style="flex: 1;">
          <p><strong>简介:</strong></p>
          <p>{{ doctor.bio || '暂无详细介绍' }}</p>
        </div>
      </div>

      <!-- <div v-if="doctor.schedule" style="margin-top: 20px;">
        <h4>出诊时间</h4>
        <el-table :data="doctor.schedule" border style="width: 100%">
          <el-table-column prop="day" label="星期" width="120" />
          <el-table-column prop="time" label="时间段" />
          <el-table-column prop="location" label="地点" />
        </el-table>
      </div> -->
      
      <!-- 评价区域 -->
      <el-tabs type="border-card">
        <el-tab-pane label="患者评价">
          <div v-if="reviews.length > 0">
            <div v-for="review in reviews" :key="review.review_id" style="margin-bottom: 15px; padding: 10px; border-bottom: 1px solid #eee;">
              <div style="display: flex; justify-content: space-between;">
                <span style="font-weight: bold;">{{ review.patient_name }}</span>
                <span style="color: #999;">{{ review.review_date }}</span>
              </div>
              <el-rate v-model="review.rating" disabled style="margin: 5px 0;"></el-rate>
              <p>{{ review.comment }}</p>
            </div>
          </div>
          <div v-else style="text-align: center; color: #999; padding: 20px;">
            暂无患者评价
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="添加评价" v-if="showReviewForm">
          <el-form :model="reviewForm" label-width="80px" style="margin-top: 20px;">
            <el-form-item label="评分" required>
                <el-rate v-model="reviewForm.rating" show-text :texts="['很差', '差', '一般', '好', '很好']"></el-rate>
            </el-form-item>
            <el-form-item label="评价内容">
              <el-input
                v-model="reviewForm.comment"
                type="textarea"
                :rows="4"
                placeholder="请写下您的评价..."
              ></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitReview">提交评价</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </el-dialog>
</template>

<script>
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  name: 'DoctorDetail',
  props: {
    doctorId: {
      type: Number,
      default: null
    },
    showReviewForm: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      visible: false,
      doctor: null,
      reviews: [],
      reviewForm: {
        rating: 5,
        comment: ''
      }
    }
  },
  methods: {
    async show(doctorId = null) {
      const id = doctorId || this.doctorId
      if (!id) {
        console.error('需要提供医生ID')
        return
      }

      try {
        // 获取医生详情
        const doctorResponse = await axios.get(`/doctors/${id}`)
        this.doctor = doctorResponse.data

        // 获取医生评价
        const response = await axios.get(`/doctors/${id}/reviews`)
        this.reviews = response.data
        
        // 重置评价表单
        this.reviewForm = {
          rating: 5,
          comment: ''
        }
        
        this.visible = true
      } catch (error) {
        console.error('获取医生详情失败:', error)
        ElMessage.error('获取医生详情失败')
      }
    },
    
    async submitReview() {
      if (!this.reviewForm.rating) {
        ElMessage.warning('请选择评分')
        return
      }
      
      try {
        await axios.post('/reviews', {
          doctor_id: this.doctor.doctor_id,
          patient_id: 1, // 这里应该是当前登录患者的ID，暂时用1代替
          rating: this.reviewForm.rating,
          comment: this.reviewForm.comment
        })
        
        ElMessage.success('评价提交成功')
        // 刷新详情数据
        await this.show(this.doctor.doctor_id)
        
        // 通知父组件评价已提交
        this.$emit('review-submitted')
      } catch (error) {
        console.error('提交评价失败:', error)
        ElMessage.error('提交评价失败')
      }
    }
  }
}
</script>