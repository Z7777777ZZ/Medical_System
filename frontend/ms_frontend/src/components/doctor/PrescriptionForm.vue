<template>
  <div class="prescription-form">
    <el-form ref="formRef" :model="prescriptionForm" label-width="100px">
      <el-row :gutter="20">
        <!-- 基础信息 -->
        <el-col :span="24">
          <div class="info-section">
            <h3>患者信息</h3>
            <div class="patient-info">
              <p><span class="label">姓名:</span> {{ patient.name }}</p>
              <p><span class="label">性别:</span> {{ patient.gender === 'male' ? '男' : '女' }}</p>
              <p><span class="label">年龄:</span> {{ patient.age }}岁</p>
              <p><span class="label">就诊原因:</span> {{ patient.visitReason }}</p>
            </div>
          </div>
        </el-col>
        
        <!-- 药品列表 -->
        <el-col :span="24">
          <div class="medicine-section">
            <div class="section-header">
              <h3>处方药品</h3>
              <el-button type="primary" size="small" @click="showMedicineDialog">
                添加药品
              </el-button>
            </div>
            
            <el-table 
              v-if="prescriptionStore.currentPrescription.medicines.length > 0"
              :data="prescriptionStore.currentPrescription.medicines"
              style="width: 100%"
              border>
              <el-table-column prop="name" label="药品名称" />
              <el-table-column prop="specification" label="规格" width="150" />
              <el-table-column label="数量" width="150">
                <template #default="scope">
                  <el-input-number 
                    v-model="scope.row.quantity" 
                    :min="1" 
                    :max="99"
                    size="small"
                    @change="(val) => updateMedicineQuantity(scope.row.id, val)"
                  />
                </template>
              </el-table-column>
              <el-table-column label="用法用量" width="220">
                <template #default="scope">
                  <el-input 
                    v-model="scope.row.usage" 
                    placeholder="请输入用法用量"
                    size="small"
                    @change="(val) => updateMedicineUsage(scope.row.id, val)"
                  />
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120">
                <template #default="scope">
                  <el-button 
                    type="danger" 
                    size="small" 
                    @click="removeMedicine(scope.row.id)"
                  >
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <el-empty v-else description="暂未添加药品" />
          </div>
        </el-col>
        
        <!-- 处方说明 -->
        <el-col :span="24">
          <div class="instruction-section">
            <h3>处方说明</h3>
            <el-form-item>
              <el-input
                v-model="prescriptionStore.currentPrescription.instructions"
                type="textarea"
                rows="4"
                placeholder="请输入处方总体用药说明和注意事项"
                @change="updateInstructions"
              />
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      
      <el-form-item class="form-actions">
        <el-button type="primary" @click="submitForm">保存处方</el-button>
        <el-button @click="cancelForm">取消</el-button>
      </el-form-item>
    </el-form>
    
    <!-- 药品选择对话框 -->
    <el-dialog v-model="medicineDialogVisible" title="选择药品" width="60%">
      <div class="medicine-search">
        <el-input
          v-model="medicineSearch"
          placeholder="请输入药品名称搜索"
          clearable
          @clear="fetchMedicines"
        >
          <template #append>
            <el-button :icon="Search" @click="searchMedicines" />
          </template>
        </el-input>
      </div>
      
      <el-table
        :data="availableMedicines"
        style="width: 100%"
        height="400px"
        @row-click="selectMedicine">
        <el-table-column prop="name" label="药品名称" />
        <el-table-column prop="specification" label="规格" width="150" />
        <el-table-column prop="type" label="类型" width="150" />
        <el-table-column prop="manufacturer" label="生产厂家" width="200" />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button 
              type="primary" 
              size="small" 
              @click.stop="addMedicine(scope.row)"
            >
              添加
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, reactive } from 'vue'
import { usePrescriptionStore } from '../../stores/prescriptionStore'
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'PrescriptionForm',
  props: {
    patient: {
      type: Object,
      required: true
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const prescriptionStore = usePrescriptionStore()
    
    // 表单引用
    const formRef = ref(null)
    
    // 药品对话框
    const medicineDialogVisible = ref(false)
    const medicineSearch = ref('')
    
    // 表单数据
    const prescriptionForm = reactive({
      medicines: [],
      instructions: ''
    })
    
    // 可用药品列表
    const availableMedicines = ref([
      // 模拟药品数据，实际应该从API获取
      { id: 1, name: '阿莫西林胶囊', specification: '0.25g*24粒/盒', type: '抗生素类', manufacturer: '哈药集团' },
      { id: 2, name: '布洛芬缓释胶囊', specification: '0.3g*12粒/盒', type: '解热镇痛类', manufacturer: '上海医药集团' },
      { id: 3, name: '感冒灵颗粒', specification: '10g*9包/盒', type: '感冒用药', manufacturer: '云南白药集团' },
      { id: 4, name: '银黄颗粒', specification: '4g*10袋/盒', type: '清热解毒类', manufacturer: '太极集团' },
      { id: 5, name: '维生素C片', specification: '0.1g*100片/瓶', type: '维生素类', manufacturer: '修正药业' }
    ])
    
    // 初始化
    onMounted(() => {
      fetchMedicines()
    })
    
    // 获取药品列表
    const fetchMedicines = async () => {
      // 实际项目中应该调用API获取药品列表
      // await prescriptionStore.fetchAvailableMedicines()
    }
    
    // 搜索药品
    const searchMedicines = () => {
      // 实现药品搜索逻辑
      if (medicineSearch.value) {
        availableMedicines.value = availableMedicines.value.filter(
          medicine => medicine.name.includes(medicineSearch.value)
        );
      } else {
        fetchMedicines();
      }
    }
    
    // 显示药品对话框
    const showMedicineDialog = () => {
      medicineDialogVisible.value = true
      medicineSearch.value = ''
      fetchMedicines()
    }
    
    // 选择药品 - 使用药品行数据添加到处方
    const selectMedicine = (medicine) => {
      addMedicine(medicine)
    }
    
    // 添加药品到处方
    const addMedicine = (medicine) => {
      prescriptionStore.addMedicineToPrescription(medicine)
      ElMessage.success(`已添加 ${medicine.name} 到处方`)
    }
    
    // 移除药品
    const removeMedicine = (medicineId) => {
      prescriptionStore.removeMedicineFromPrescription(medicineId)
    }
    
    // 更新药品数量
    const updateMedicineQuantity = (medicineId, quantity) => {
      prescriptionStore.updateMedicineQuantity(medicineId, quantity)
    }
    
    // 更新药品用法说明
    const updateMedicineUsage = (medicineId, usage) => {
      prescriptionStore.updateMedicineUsage(medicineId, usage)
    }
    
    // 更新处方整体说明
    const updateInstructions = (instructions) => {
      prescriptionStore.updateInstructions(instructions)
    }
    
    // 提交表单
    const submitForm = async () => {
      if (prescriptionStore.currentPrescription.medicines.length === 0) {
        ElMessage.warning('请至少添加一种药品')
        return
      }
      
      emit('submit', prescriptionStore.currentPrescription)
    }
    
    // 取消表单
    const cancelForm = () => {
      emit('cancel')
    }
    
    return {
      formRef,
      prescriptionForm,
      prescriptionStore,
      medicineDialogVisible,
      medicineSearch,
      availableMedicines,
      Search,
      fetchMedicines,
      searchMedicines,
      showMedicineDialog,
      selectMedicine,
      addMedicine,
      removeMedicine,
      updateMedicineQuantity,
      updateMedicineUsage,
      updateInstructions,
      submitForm,
      cancelForm
    }
  }
}
</script>

<style scoped>
.prescription-form {
  padding: 20px 0;
}

.info-section, 
.medicine-section, 
.instruction-section {
  margin-bottom: 30px;
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 15px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.patient-info {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.patient-info p {
  margin: 0;
}

.label {
  font-weight: bold;
  margin-right: 5px;
}

.medicine-search {
  margin-bottom: 20px;
}

h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
  font-size: 16px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>