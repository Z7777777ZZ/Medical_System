<template>
  <div class="page-container">
    <div class="page-header">
      <h2>我的病历记录</h2>
      <el-button type="primary" @click="refreshMedicalRecords">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>
    
    <div class="filter-section">
      <el-input
        v-model="searchQuery"
        placeholder="搜索病历（按疾病关键词）"
        prefix-icon="Search"
        clearable
        @clear="resetSearch"
        style="width: 250px"
      />
      
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        value-format="YYYY-MM-DD"
        @change="filterByDate"
      />
    </div>
    
    <div v-if="loading" class="loading-section">
      <el-skeleton :rows="5" animated />
    </div>
    
    <div v-else-if="filteredRecords.length === 0" class="empty-section">
      <el-empty description="暂无病历记录" />
    </div>
    
    <div v-else class="records-section">
      <el-timeline>
        <el-timeline-item
          v-for="record in filteredRecords"
          :key="record.id"
          :timestamp="record.visitDate"
          :type="getTimelineType(record)"
        >
          <el-card class="record-card">
            <template #header>
              <div class="record-header">
                <h3>{{ record.diagnosis }}</h3>
                <el-tag>{{ record.department }}</el-tag>
              </div>
            </template>
            
            <div class="record-content">
              <div class="record-detail">
                <div class="detail-item">
                  <strong>医生：</strong>
                  <span>{{ record.doctorName }}</span>
                </div>
                <div class="detail-item">
                  <strong>主诉：</strong>
                  <span>{{ record.chiefComplaint }}</span>
                </div>
                <div class="detail-item">
                  <strong>诊断结果：</strong>
                  <span>{{ record.diagnosis }}</span>
                </div>
                <div class="detail-item">
                  <strong>治疗方案：</strong>
                  <span>{{ record.treatmentPlan }}</span>
                </div>
                <div v-if="record.medications" class="detail-item">
                  <strong>用药记录：</strong>
                  <div class="medication-list">
                    <div v-for="(med, index) in record.medications" :key="index" class="medication-item">
                      {{ med.name }} {{ med.instructions }}
                    </div>
                  </div>
                </div>
                <div v-if="record.notes" class="detail-item">
                  <strong>注意事项：</strong>
                  <span>{{ record.notes }}</span>
                </div>
                <div class="detail-actions">
                  <el-button type="primary" size="small" @click="viewRecordDetail(record.id)">
                    查看详情
                  </el-button>
                </div>
              </div>
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </div>
    
    <div class="pagination-section" v-if="filteredRecords.length > 0">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[5, 10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="filteredRecords.length"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 详细查看弹窗 -->
    <el-dialog
      v-model="recordDetailVisible"
      title="病历详情"
      width="70%"
      destroy-on-close
    >
      <div v-if="detailLoading" class="loading-section">
        <el-skeleton :rows="8" animated />
      </div>
      <div v-else-if="!currentRecord" class="empty-section">
        <el-empty description="无法加载病例详情" />
      </div>
      <div v-else class="record-detail-dialog">
        <el-descriptions title="基本信息" :column="2" border>
          <el-descriptions-item label="就诊日期">{{ currentRecord.visitDate }}</el-descriptions-item>
          <el-descriptions-item label="主诊医生">{{ currentRecord.doctorName }}</el-descriptions-item>
          <el-descriptions-item label="就诊科室">{{ currentRecord.department }}</el-descriptions-item>
          <el-descriptions-item label="记录时间">{{ formatDateTime(currentRecord.createdAt) }}</el-descriptions-item>
        </el-descriptions>

        <el-divider content-position="left">病情信息</el-divider>
        
        <el-descriptions :column="1" border>
          <el-descriptions-item label="主诉">{{ currentRecord.chiefComplaint }}</el-descriptions-item>
          <el-descriptions-item label="诊断结果">{{ currentRecord.diagnosis }}</el-descriptions-item>
          <el-descriptions-item label="治疗方案">{{ currentRecord.treatmentPlan }}</el-descriptions-item>
        </el-descriptions>

        <el-divider v-if="currentRecord.prescription" content-position="left">处方信息</el-divider>
        
        <div v-if="currentRecord.prescription" class="prescription-section">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="处方编号">{{ currentRecord.prescription.prescription_id }}</el-descriptions-item>
            <el-descriptions-item label="开具时间">{{ formatDateTime(currentRecord.prescription.created_at) }}</el-descriptions-item>
          </el-descriptions>
          
          <el-table v-if="currentRecord.medications" :data="currentRecord.medications" stripe style="width: 100%; margin-top: 20px">
            <el-table-column prop="name" label="药品名称" min-width="150" />
            <el-table-column prop="instructions" label="用药说明" min-width="250" />
          </el-table>
        </div>

        <el-divider v-if="currentRecord.photos && currentRecord.photos.length > 0" content-position="left">检查照片</el-divider>
        
        <div v-if="currentRecord.photos && currentRecord.photos.length > 0" class="photos-section">
          <el-carousel :interval="5000" height="300px">
            <el-carousel-item v-for="(photo, index) in currentRecord.photos" :key="index">
              <div class="photo-container">
                <img :src="photo" alt="检查照片" class="medical-photo" />
              </div>
            </el-carousel-item>
          </el-carousel>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="recordDetailVisible = false">关闭</el-button>
          <el-button type="primary" @click="printMedicalRecord">
            打印病历
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { usePatientStore } from '../../store/patient'
import { Refresh } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'MedicalRecordsPage',
  components: {
    Refresh
  },
  setup() {
    const patientStore = usePatientStore()
    const searchQuery = ref('')
    const dateRange = ref(null)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const loading = ref(false)
    const recordDetailVisible = ref(false)
    const detailLoading = ref(false)
    const currentRecord = ref(null)
    
    // Get all medical records
    const fetchMedicalRecords = async () => {
      loading.value = true
      try {
        await patientStore.fetchMedicalRecords()
      } catch (error) {
        ElMessage.error('获取病历记录失败')
      } finally {
        loading.value = false
      }
    }
    
    // Refresh records
    const refreshMedicalRecords = () => {
      fetchMedicalRecords()
      ElMessage.success('病历记录已更新')
    }
    
    // View record detail
    const viewRecordDetail = async (recordId) => {
      recordDetailVisible.value = true
      detailLoading.value = true
      currentRecord.value = null
      
      try {
        const record = await patientStore.fetchMedicalRecordDetail(recordId)
        currentRecord.value = record
      } catch (error) {
        ElMessage.error('获取病历详情失败')
      } finally {
        detailLoading.value = false
      }
    }
    
    // Print medical record
    const printMedicalRecord = () => {
      ElMessage.success('正在准备打印...')
      window.print()
    }
    
    // Format date time
    const formatDateTime = (dateTimeStr) => {
      if (!dateTimeStr) return '未知时间'
      
      try {
        const date = new Date(dateTimeStr)
        return date.toLocaleString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        })
      } catch (e) {
        return dateTimeStr
      }
    }
    
    // Filter records by search query and date range
    const filteredRecords = computed(() => {
      let records = patientStore.medicalRecords
      
      // Filter by search query
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        records = records.filter(record => 
          record.diagnosis.toLowerCase().includes(query) ||
          record.chiefComplaint.toLowerCase().includes(query) ||
          record.treatmentPlan.toLowerCase().includes(query)
        )
      }
      
      // Filter by date range
      if (dateRange.value && dateRange.value[0] && dateRange.value[1]) {
        const startDate = new Date(dateRange.value[0])
        const endDate = new Date(dateRange.value[1])
        
        records = records.filter(record => {
          const recordDate = new Date(record.visitDate)
          return recordDate >= startDate && recordDate <= endDate
        })
      }
      
      // Sort by date (newest first)
      return records.sort((a, b) => new Date(b.visitDate) - new Date(a.visitDate))
    })
    
    // Reset search
    const resetSearch = () => {
      searchQuery.value = ''
    }
    
    // Filter by date
    const filterByDate = () => {
      currentPage.value = 1
    }
    
    // Pagination handlers
    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
    }
    
    const handleCurrentChange = (page) => {
      currentPage.value = page
    }
    
    // Get timeline item type based on diagnosis (for visual indication)
    const getTimelineType = (record) => {
      // Simplified logic - could be more sophisticated in real app
      if (record.diagnosis.includes('急') || record.diagnosis.includes('重症')) {
        return 'danger'
      } else if (record.diagnosis.includes('慢性')) {
        return 'warning'
      }
      return 'primary'
    }
    
    // Load records on mount
    onMounted(() => {
      fetchMedicalRecords()
    })
    
    return {
      searchQuery,
      dateRange,
      currentPage,
      pageSize,
      loading,
      filteredRecords,
      resetSearch,
      filterByDate,
      handleSizeChange,
      handleCurrentChange,
      getTimelineType,
      refreshMedicalRecords,
      recordDetailVisible,
      detailLoading,
      currentRecord,
      viewRecordDetail,
      printMedicalRecord,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-section {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.loading-section,
.empty-section {
  margin: 40px 0;
}

.records-section {
  margin-top: 20px;
}

.record-card {
  margin-bottom: 10px;
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.record-header h3 {
  margin: 0;
  font-size: 16px;
}

.record-content {
  font-size: 14px;
}

.detail-item {
  margin-bottom: 10px;
}

.medication-list {
  margin-top: 5px;
}

.medication-item {
  padding: 3px 0;
}

.record-detail-dialog {
  max-height: 70vh;
  overflow-y: auto;
  padding: 10px;
}

.prescription-section {
  margin-top: 20px;
}

.photo-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

.medical-photo {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.pagination-section {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

.detail-actions {
  margin-top: 15px;
}

@media print {
  .page-header, 
  .filter-section, 
  .pagination-section,
  .el-dialog__header,
  .el-dialog__footer {
    display: none !important;
  }
  
  .record-detail-dialog {
    overflow: visible;
    max-height: none;
  }
}
</style> 