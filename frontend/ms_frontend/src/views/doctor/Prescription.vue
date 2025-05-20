<template>
  <div class="doctor-prescription">
    <el-card class="prescription-card">
      <template #header>
        <div class="card-header">
          <h3>处方管理</h3>
          <div class="header-actions">
            <el-button type="primary" @click="goToDashboard">返回工作台</el-button>
            <el-button type="success" @click="goToQueue">患者队列</el-button>
          </div>
        </div>
      </template>

      <div class="doctor-prescription-view">
        <!-- 顶部操作栏 -->
        <div class="toolbar">
          <el-button type="primary" @click="createNewPrescription">
            <el-icon><el-icon-plus /></el-icon>
            新建处方
          </el-button>
          
          <div class="search-box">
            <el-input
              v-model="searchQuery"
              placeholder="搜索处方..."
              prefix-icon="el-icon-search"
              clearable
              @input="handleSearch">
            </el-input>
            <el-select v-model="dateFilter" placeholder="时间筛选" style="width: 130px; margin-left: 10px;">
              <el-option label="全部时间" value="all"></el-option>
              <el-option label="今天" value="today"></el-option>
              <el-option label="本周" value="week"></el-option>
              <el-option label="本月" value="month"></el-option>
            </el-select>
            <el-select v-model="statusFilter" placeholder="状态筛选" style="width: 130px; margin-left: 10px;">
              <el-option label="全部状态" value="all"></el-option>
              <el-option label="草稿" value="draft"></el-option>
              <el-option label="已完成" value="completed"></el-option>
              <el-option label="作废" value="cancelled"></el-option>
            </el-select>
          </div>
        </div>
        
        <!-- 处方列表卡片 -->
        <el-card class="prescription-list-card">
          <template #header>
            <div class="card-header">
              <h3>处方列表</h3>
              <el-button-group>
                <el-button @click="refreshPrescriptions" :loading="loading">
                  <el-icon><el-icon-refresh /></el-icon>
                  刷新
                </el-button>
                <el-button @click="exportToExcel">
                  <el-icon><el-icon-document /></el-icon>
                  导出
                </el-button>
              </el-button-group>
            </div>
          </template>
          
          <div class="prescription-list-content">
            <el-table
              v-if="filteredPrescriptions.length > 0"
              :data="filteredPrescriptions"
              style="width: 100%"
              @row-click="handleRowClick">
              <el-table-column prop="id" label="处方编号" width="120" />
              <el-table-column label="开具日期" width="180">
                <template #default="scope">
                  {{ formatDate(scope.row.date) }}
                </template>
              </el-table-column>
              <el-table-column prop="patientName" label="患者姓名" width="120" />
              <!-- <el-table-column prop="diagnosis" label="诊断" show-overflow-tooltip /> -->
              <el-table-column label="药品数量" width="80">
                <template #default="scope">
                  {{ scope.row.medicines.length }}
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="120">
                <template #default="scope">
                  <el-tag :type="getStatusType(scope.row.status)">
                    {{ getStatusText(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="240" fixed="right">
                <template #default="scope">
                  <el-button-group>
                    <el-button 
                      type="primary" 
                      size="small" 
                      @click.stop="viewPrescription(scope.row)"
                    >
                      查看
                    </el-button>
                    <el-button 
                      v-if="scope.row.status === 'draft'"
                      type="success" 
                      size="small" 
                      @click.stop="editPrescription(scope.row)"
                    >
                      编辑
                    </el-button>
                    <el-button 
                      v-if="scope.row.status === 'draft'"
                      type="danger" 
                      size="small" 
                      @click.stop="confirmCancelPrescription(scope.row)"
                    >
                      作废
                    </el-button>
                    <el-button 
                      type="info" 
                      size="small" 
                      @click.stop="printPrescription(scope.row)"
                    >
                      打印
                    </el-button>
                  </el-button-group>
                </template>
              </el-table-column>
            </el-table>
            
            <div v-else-if="loading" class="loading-placeholder">
              <el-skeleton animated :rows="6" />
            </div>
            
            <el-empty v-else description="暂无处方记录" />
          </div>
          
          <div class="pagination-container">
            <el-pagination
              v-if="filteredPrescriptions.length > 0"
              :currentPage="currentPage"
              :page-size="pageSize"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              :total="filteredTotalCount"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange">
            </el-pagination>
          </div>
        </el-card>
        
        <!-- 处方表单对话框 -->
        <el-dialog
          v-model="prescriptionFormVisible"
          :title="currentPrescription.id ? '编辑处方' : '新建处方'"
          width="80%"
          destroy-on-close>
          <prescription-form
            :prescription="currentPrescription"
            @save="savePrescription"
            @cancel="prescriptionFormVisible = false"
          />
        </el-dialog>
        
        <!-- 处方详情对话框 -->
        <el-dialog
          v-model="prescriptionDetailVisible"
          title="处方详情"
          width="70%"
          destroy-on-close>
          <div v-if="currentPrescription" class="prescription-detail">
            <div class="prescription-header">
              <div class="hospital-info">
                <h2>医疗系统门诊部</h2>
                <p>电子处方笺</p>
              </div>
              <div class="prescription-id">
                <p>处方编号: {{ currentPrescription.id }}</p>
                <p>日期: {{ formatDate(currentPrescription.date) }}</p>
              </div>
            </div>
            
            <el-divider />
            
            <div class="prescription-info">
              <div class="info-row">
                <div class="info-item"><span class="label">患者姓名:</span> {{ currentPrescription.patientName }}</div>
                <div class="info-item"><span class="label">性别:</span> {{ currentPrescription.patientGender === 'male' ? '男' : '女' }}</div>
                <div class="info-item"><span class="label">年龄:</span> {{ currentPrescription.patientAge }}岁</div>
              </div>
              <!-- <div class="info-row">
                <div class="info-item"><span class="label">诊断:</span> {{ currentPrescription.diagnosis }}</div>
              </div> -->
            </div>
            
            <el-divider />
            
            <div class="medicine-list">
              <h3>药品清单</h3>
              <el-table
                :data="currentPrescription.medicines"
                style="width: 100%"
                border
                stripe>
                <el-table-column type="index" label="序号" width="60" />
                <el-table-column prop="name" label="药品名称" min-width="180" />
                <el-table-column prop="specification" label="规格" width="150" />
                <el-table-column prop="quantity" label="数量" width="80" />
                <el-table-column prop="usage" label="用法用量" min-width="200" />
              </el-table>
            </div>
            
            <div v-if="currentPrescription.instructions" class="instructions">
              <h3>医嘱</h3>
              <div class="instructions-text">{{ currentPrescription.instructions }}</div>
            </div>
            
            <div class="prescription-footer">
              <div class="doctor-signature">
                <p><span class="label">医生签名:</span> {{ currentPrescription.doctorName }}</p>
                <p><span class="label">医师资格证号:</span> {{ currentPrescription.doctorLicenseNumber || '****' }}</p>
              </div>
              <div class="pharmacy-info">
                <p><span class="label">有效期:</span> 3天（自开具日起计算）</p>
              </div>
            </div>
          </div>
          
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="prescriptionDetailVisible = false">关闭</el-button>
              <el-button type="primary" @click="printPrescription(currentPrescription)">打印</el-button>
            </span>
          </template>
        </el-dialog>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usePrescriptionStore } from '../../stores/prescriptionStore'
import PrescriptionForm from '../../components/doctor/PrescriptionForm.vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const BASE_API_URL = 'http://127.0.0.1:5000'
export default {
  name: 'DoctorPrescription',
  components: {
    PrescriptionForm
  },
  setup() {
    /* eslint-disable no-unused-vars */
    const router = useRouter()
    const prescriptionStore = usePrescriptionStore()
    /* eslint-enable no-unused-vars */
    
    const route = useRoute()
    
    // 状态
    const loading = ref(false)
    // TODO 不能获取的数据我都没有清空，具体需要患者信息的调用和医生信息的调用
    const prescriptions = ref([
      {
        id: '',
        patientId: '',
        patientName: '张三',
        patientGender: 'male',
        patientAge: 35,
        doctorId: '',
        doctorName: '李医生',
        doctorLicenseNumber: 'MD12345678',
        department: '内科',
        date: '',
        // diagnosis: '',
        status: '',
        medicines: [  ],
        instructions: ''
      }
    ])

    // 获取医生的处方列表
    const fetchDoctorPrescriptions = async (doctorId) => {
      loading.value = true
      try {
        const response = await fetch(`${BASE_API_URL}/api/diagnosis/prescription?doctorId=${doctorId}`);
        const data = await response.json();
        prescriptions.value = data || [];
        // iter all patientId and dockerId to get details
        // prescriptions.value.forEach(prescription => {
          // TODO
          // get petient details and docker details by id from api
          // just like follow
          // fetch(`/diagnosis/patient/${prescription.patientId}`)
          //   .then(response => response.json())
          //   .then(patientData => {
          //     prescription.patientName = patientData.name
          //     prescription.patientGender = patientData
        // })
        // console.log('处方列表:', prescriptions.value);
      } catch (error) {
        console.error('获取处方列表失败:', error);
        ElMessage.error('获取处方列表失败');
      } finally {
        loading.value = false;
      }
    };

    const currentPrescription = ref({
      patientId: '',
      patientName: '',
      patientGender: '',
      patientAge: '',
      // diagnosis: '',
      medicines: [],
      instructions: ''
    })
    const prescriptionFormVisible = ref(false)
    const prescriptionDetailVisible = ref(false)
    const searchQuery = ref('')
    const dateFilter = ref('all')
    const statusFilter = ref('all')
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalPrescriptions = ref(0)
    
    // 筛选处方列表
    const filteredPrescriptions = computed(() => {
      let result = [...prescriptions.value]
      
      // 关键词搜索
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(p => 
          p.id.toLowerCase().includes(query) || 
          p.patientName.toLowerCase().includes(query)
          // p.diagnosis.toLowerCase().includes(query)
        )
      }
      
      // 日期筛选
      if (dateFilter.value !== 'all') {
        const now = new Date()
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
        const weekStart = new Date(today)
        weekStart.setDate(today.getDate() - today.getDay())
        const monthStart = new Date(now.getFullYear(), now.getMonth(), 1)
        
        result = result.filter(p => {
          const prescriptionDate = new Date(p.date)
          
          switch (dateFilter.value) {
            case 'today':
              return prescriptionDate >= today
            case 'week':
              return prescriptionDate >= weekStart
            case 'month':
              return prescriptionDate >= monthStart
            default:
              return true
          }
        })
      }
      
      // 状态筛选
      if (statusFilter.value !== 'all') {
        result = result.filter(p => p.status === statusFilter.value)
      }
      
      // 分页
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      
      return result.slice(start, end)
    })
    
    // 计算处方总数，避免副作用
    const filteredTotalCount = computed(() => {
      let result = [...prescriptions.value]
      
      // 关键词搜索
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(p => 
          p.id.toLowerCase().includes(query) || 
          p.patientName.toLowerCase().includes(query)
          // p.diagnosis.toLowerCase().includes(query)
        )
      }
      
      // 日期筛选
      if (dateFilter.value !== 'all') {
        const now = new Date()
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
        const weekStart = new Date(today)
        weekStart.setDate(today.getDate() - today.getDay())
        const monthStart = new Date(now.getFullYear(), now.getMonth(), 1)
        
        result = result.filter(p => {
          const prescriptionDate = new Date(p.date)
          
          switch (dateFilter.value) {
            case 'today':
              return prescriptionDate >= today
            case 'week':
              return prescriptionDate >= weekStart
            case 'month':
              return prescriptionDate >= monthStart
            default:
              return true
          }
        })
      }
      
      // 状态筛选
      if (statusFilter.value !== 'all') {
        result = result.filter(p => p.status === statusFilter.value)
      }
      
      return result.length
    })
    
    // 监听过滤后的总数变化
    watch(filteredTotalCount, (newCount) => {
      totalPrescriptions.value = newCount
    })
    
    // 副作用操作
    const performSideEffect = () => {
      totalPrescriptions.value = filteredTotalCount.value
    }
    
    // 刷新处方列表
    const refreshPrescriptions = async () => {
      loading.value = true
      
      // 模拟API调用
      setTimeout(() => {
        loading.value = false
        ElMessage.success('处方列表已更新')
      }, 1000)
    }
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
    }
    
    // 获取状态类型
    const getStatusType = (status) => {
      switch (status) {
        case 'completed':
          return 'success'
        case 'draft':
          return 'warning'
        case 'cancelled':
          return 'danger'
        default:
          return 'info'
      }
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'completed':
          return '已完成'
        case 'draft':
          return '草稿'
        case 'cancelled':
          return '已作废'
        default:
          return '未知状态'
      }
    }
    
    // 表格行点击
    const handleRowClick = (row) => {
      viewPrescription(row)
    }
    
    // 查看处方
    const viewPrescription = (prescription) => {
      currentPrescription.value = { ...prescription }
      prescriptionDetailVisible.value = true
    }
    
    // 创建新处方
    const createNewPrescription = () => {
      currentPrescription.value = {
        patientId: '',
        patientName: '',
        patientGender: '',
        patientAge: '',
        // diagnosis: '',
        medicines: [],
        instructions: '',
        doctorId: '1',
        doctorName: '李医生',
        doctorLicenseNumber: 'MD12345678',
        department: '内科',
        date: new Date().toISOString(),
        status: 'draft'
      }
      
      if (route.query.patientId) {
        // TODO 实际项目中应该通过API获取患者信息
        const patientInfo = {
          id: route.query.patientId,
          name: '张三',
          gender: 'male',
          age: 35
        }
        
        currentPrescription.value.patientId = patientInfo.id
        currentPrescription.value.patientName = patientInfo.name
        currentPrescription.value.patientGender = patientInfo.gender
        currentPrescription.value.patientAge = patientInfo.age
      }
      
      prescriptionFormVisible.value = true
    }
    
    // 编辑处方
    const editPrescription = (prescription) => {
      currentPrescription.value = { ...prescription }
      prescriptionFormVisible.value = true
    }
    
    // 确认作废处方
    const confirmCancelPrescription = (prescription) => {
      ElMessageBox.confirm(
        '确认要作废该处方吗？此操作不可逆。',
        '确认作废',
        {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        cancelPrescription(prescription)
      }).catch(() => {
        // 用户取消操作
      })
    }
    
    // 作废处方
    /*
      const prescriptions = ref([
      {
        id: '',
        patientId: '',
        patientName: '张三',
        patientGender: 'male',
        patientAge: 35,
        doctorId: '',
        doctorName: '李医生',
        doctorLicenseNumber: 'MD12345678',
        department: '内科',
        date: '',
        // diagnosis: '',
        status: '',
        medicines: [  ],
        instructions: ''
      }
    ])
     */
    const cancelPrescription = async (prescription) => {
      try {
        loading.value = true
        
        // 调用实际API更新处方状态为已作废
        const response = await fetch(`${BASE_API_URL}/api/diagnosis/prescription/${prescription.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            patientId: prescription.patientId,
            dockerId: prescription.doctorId,
            date: prescription.date,
            medicines: prescription.medicines,
            instructions: prescription.instructions,
            status: 'cancelled'
          })
        })
        
        if (response.ok) {
          const index = prescriptions.value.findIndex(p => p.id === prescription.id)
          if (index !== -1) {
            prescriptions.value[index].status = 'cancelled'
            ElMessage.success('处方已成功作废')
          }
        } else {
          throw new Error('作废处方失败')
        }
      } catch (error) {
        console.error('作废处方失败:', error)
        ElMessage.error('作废处方失败')
      } finally {
        loading.value = false
      }
    }
    
    // 保存处方
    // 保存处方
    const savePrescription = async (prescription, submit = false) => {
      loading.value = true
      
      try {
        // 添加 data
        const prescriptionData = {
          patientId: prescription.patientId,
          doctorId: prescription.doctorId,
          date: prescription.date,
          medicines: prescription.medicines,
          instructions: prescription.instructions,
          status: submit ? 'completed' : 'draft'
        }
        
        let response
        let savedPrescription
        
        if (prescription.id) {
          // 先检查处方是否存在
          try {
            const checkResponse = await fetch(`${BASE_API_URL}/api/diagnosis/prescription/${prescription.id}`)
            
            if (checkResponse.ok) {
              // 处方存在，使用 PUT 更新
              response = await fetch(`${BASE_API_URL}/api/diagnosis/prescription/${prescription.id}`, {
                method: 'PUT',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify(prescriptionData)
              })
              
              if (response.ok) {
                savedPrescription = await response.json()
                
                const index = prescriptions.value.findIndex(p => p.id === prescription.id)
                if (index !== -1) {
                  prescriptions.value[index] = { 
                    ...prescription, 
                    status: submit ? 'completed' : 'draft'
                  }
                }
                
                ElMessage.success(`处方已${submit ? '提交' : '更新'}`)
              } else {
                throw new Error('更新处方失败')
              }
            } else {
              throw new Error('处方不存在')
            }
          } catch (error) {
            console.error('检查处方失败，尝试创建新处方:', error)
            // 处方不存在或检查失败，使用 POST 创建
            response = await fetch(`${BASE_API_URL}/api/diagnosis/prescription`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(prescriptionData)
            })
            
            if (response.ok) {
              savedPrescription = await response.json()
              
              // 将新处方添加到列表
              prescriptions.value.unshift({
                ...prescription,
                id: savedPrescription.id,
                status: submit ? 'completed' : 'draft'
              })
              
              ElMessage.success(`处方已${submit ? '提交' : '创建'}`)
            } else {
              throw new Error('创建处方失败')
            }
          }
        } else {
          // 没有ID，直接创建新处方
          response = await fetch(`${BASE_API_URL}/api/diagnosis/prescription`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(prescriptionData)
          })
          
          if (response.ok) {
            savedPrescription = await response.json()
            
            // 将新处方添加到列表
            prescriptions.value.unshift({
              ...prescription,
              id: savedPrescription.id,
              status: submit ? 'completed' : 'draft'
            })
            
            ElMessage.success(`处方已${submit ? '提交' : '创建'}`)
          } else {
            throw new Error('创建处方失败')
          }
        }
        
        // 关闭表单对话框
        prescriptionFormVisible.value = false
        
      } catch (error) {
        console.error('保存处方失败:', error)
        ElMessage.error('保存处方失败')
      } finally {
        loading.value = false
      }
    }
    
    // 打印处方
    const printPrescription = (prescription) => {
      ElMessage.success(`正在打印处方 ${prescription.id}`)
      
      // TODO 实际项目中应该调用浏览器打印功能或生成PDF
    }
    
    // 导出为Excel
    const exportToExcel = () => {
      ElMessage.success('正在导出处方列表到Excel')
      
      // TODO 实际项目中应该生成并下载Excel文件
    }
    
    // 处理搜索
    const handleSearch = () => {
      currentPage.value = 1
    }
    
    // 处理页面尺寸变化
    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
    }
    
    // 处理页码变化
    const handleCurrentChange = (page) => {
      currentPage.value = page
    }
    
    // 监听筛选器变化
    watch([dateFilter, statusFilter], () => {
      currentPage.value = 1
    })
    
    // 初始化
    onMounted(() => {
      refreshPrescriptions()
      
      // 如果路由中包含患者信息，则自动创建新处方
      if (route.query.patientId) {
        createNewPrescription()
      }
      
      performSideEffect()
    })

    // 导航函数
    const goToDashboard = () => {
      router.push('/doctor/dashboard')
    }

    const goToQueue = () => {
      router.push('/doctor/queue')
    }
    
    return {
      loading,
      prescriptions,
      filteredPrescriptions,
      filteredTotalCount,
      currentPrescription,
      prescriptionFormVisible,
      prescriptionDetailVisible,
      searchQuery,
      dateFilter,
      statusFilter,
      currentPage,
      pageSize,
      totalPrescriptions,
      refreshPrescriptions,
      formatDate,
      getStatusType,
      getStatusText,
      handleRowClick,
      viewPrescription,
      createNewPrescription,
      editPrescription,
      confirmCancelPrescription,
      savePrescription,
      printPrescription,
      exportToExcel,
      handleSearch,
      handleSizeChange,
      handleCurrentChange,
      goToDashboard,
      goToQueue,
      fetchDoctorPrescriptions
    }
  }
}
</script>

<style scoped>
.doctor-prescription-view {
  padding: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-box {
  display: flex;
  align-items: center;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.prescription-list-card {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.prescription-detail {
  padding: 20px;
}

.prescription-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.hospital-info {
  text-align: center;
}

.hospital-info h2 {
  margin-bottom: 5px;
  color: #303133;
}

.prescription-id {
  text-align: right;
}

.prescription-id p {
  margin: 5px 0;
  color: #606266;
}

.prescription-info {
  margin-bottom: 20px;
}

.info-row {
  display: flex;
  margin-bottom: 10px;
  flex-wrap: wrap;
}

.info-item {
  margin-right: 30px;
  margin-bottom: 5px;
}

.label {
  font-weight: bold;
  color: #303133;
  margin-right: 5px;
}

.medicine-list {
  margin-bottom: 20px;
}

.medicine-list h3, .instructions h3 {
  margin-bottom: 15px;
  color: #303133;
  font-weight: 600;
}

.instructions {
  margin: 20px 0;
}

.instructions-text {
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
  line-height: 1.6;
}

.prescription-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 40px;
}

.doctor-signature, .pharmacy-info {
  max-width: 50%;
}

.doctor-signature p, .pharmacy-info p {
  margin-bottom: 5px;
}

.loading-placeholder {
  padding: 20px;
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
  }
  
  .search-box {
    margin-top: 10px;
    width: 100%;
  }
}

.header-actions {
  display: flex;
  gap: 10px;
}
</style>