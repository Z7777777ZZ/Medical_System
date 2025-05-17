<template>
    <el-scrollbar height="100%" style="width: 100%;">
        <!-- 标题 -->
        <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold; ">智慧问诊</div>   
        
        <!-- 症状描述区域 -->
        <div style="margin: 40px; padding: 20px; background: #f5f7fa; border-radius: 8px;">
            <el-input
                v-model="symptomDescription"
                type="textarea"
                :rows="5"
                placeholder="请详细描述您的症状（例如：头痛、发热、咳嗽等），包括持续时间、严重程度等信息"
                resize="none"
            ></el-input>
            <el-button 
                type="primary" 
                style="margin-top: 20px;"
                @click="submitSymptoms"
                :loading="isLoading"
            >
                <el-icon style="margin-right: 5px;"><Promotion /></el-icon>
                提交症状
            </el-button>
        </div>

        <!-- AI诊断结果 -->
        <div v-if="showResults" style="margin: 40px; padding: 20px; background: #f5f7fa; border-radius: 8px;">
            <div style="font-size: 1.5em; font-weight: bold; margin-bottom: 20px;">AI初步诊断</div>
            
            <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                <div style="font-weight: bold; color: #409EFF; margin-bottom: 10px;">可能疾病:</div>
                <div style="margin-left: 20px;">{{ aiDiagnosis.possibleDiseases.join('、') }}</div>
                
                <el-divider />
                
                <div style="font-weight: bold; color: #409EFF; margin-bottom: 10px;">建议:</div>
                <div style="margin-left: 20px;">{{ aiDiagnosis.suggestions }}</div>
                
                <el-divider />
                
                <div style="font-weight: bold; color: #409EFF; margin-bottom: 10px;">紧急程度:</div>
                <el-tag :type="urgencyTagType" size="large">{{ aiDiagnosis.urgencyLevel }}</el-tag>
            </div>

            <!-- 推荐医生 -->
            <div style="font-size: 1.5em; font-weight: bold; margin-bottom: 20px;">推荐医生</div>
            <div style="display: flex; flex-wrap: wrap; justify-content: start;">
                <div 
                    class="doctor-card" 
                    v-for="(doctor, index) in recommendedDoctors" 
                    :key="index"
                    @click="viewDoctorDetail(doctor)"
                >
                    <div style="font-weight: bold; font-size: 18px;">{{ doctor.name }}</div>
                    <div style="color: #666; margin: 5px 0;">{{ doctor.hospital }}</div>
                    <div style="color: #409EFF;">{{ doctor.department }}</div>
                    <div style="margin-top: 10px; font-size: 14px;">专长: {{ doctor.specialty }}</div>
                </div>
            </div>
        </div>
    </el-scrollbar>
</template>

<script>
import { Promotion } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
    name: 'AIDiagnosisView',
    components: {
        Promotion
    },
    data() {
        return {
            symptomDescription: '',
            isLoading: false,
            showResults: false,
            aiDiagnosis: {
                possibleDiseases: [],
                suggestions: '',
                urgencyLevel: ''
            },
            recommendedDoctors: [],
            // 模拟医生数据库
            doctorDatabase: [
                {
                    id: 1,
                    name: '张伟',
                    hospital: '北京协和医院',
                    department: '呼吸内科',
                    specialty: '呼吸系统疾病',
                    phone: '13800001111'
                },
                {
                    id: 2,
                    name: '王芳',
                    hospital: '北京协和医院',
                    department: '妇科',
                    specialty: '妇科肿瘤',
                    phone: '13800002222'
                },
                {
                    id: 3,
                    name: '李明',
                    hospital: '北京协和医院',
                    department: '胃肠外科',
                    specialty: '胃肠疾病',
                    phone: '13800003333'
                },
                {
                    id: 4,
                    name: '赵华',
                    hospital: '上海瑞金医院',
                    department: '骨科',
                    specialty: '骨折创伤',
                    phone: '13800004444'
                },
                {
                    id: 5,
                    name: '刘洋',
                    hospital: '上海瑞金医院',
                    department: '心内科',
                    specialty: '冠心病',
                    phone: '13800005555'
                }
            ]
        }
    },
    computed: {
        urgencyTagType() {
            const level = this.aiDiagnosis.urgencyLevel;
            if (level === '高') return 'danger';
            if (level === '中') return 'warning';
            return 'success';
        }
    },
    methods: {
        submitSymptoms() {
            if (!this.symptomDescription.trim()) {
                ElMessage.warning('请输入症状描述');
                return;
            }

            this.isLoading = true;
            
            // 模拟AI诊断延迟
            setTimeout(() => {
                this.generateAIDiagnosis();
                this.recommendDoctors();
                this.showResults = true;
                this.isLoading = false;
            }, 1500);
        },
        
        generateAIDiagnosis() {
            // 模拟AI诊断逻辑 - 实际项目中这里应该是API调用
            const symptoms = this.symptomDescription.toLowerCase();
            
            if (symptoms.includes('头痛') && symptoms.includes('发热')) {
                this.aiDiagnosis = {
                    possibleDiseases: ['感冒', '流感', '上呼吸道感染'],
                    suggestions: '建议多休息、多喝水，可服用退烧药。如症状持续3天以上或加重，请及时就医。',
                    urgencyLevel: '中'
                };
            } 
            else if (symptoms.includes('腹痛') && symptoms.includes('腹泻')) {
                this.aiDiagnosis = {
                    possibleDiseases: ['肠胃炎', '食物中毒'],
                    suggestions: '建议暂时禁食，补充电解质。如出现血便或持续呕吐，请立即就医。',
                    urgencyLevel: '中'
                };
            }
            else if (symptoms.includes('胸痛')) {
                this.aiDiagnosis = {
                    possibleDiseases: ['心绞痛', '心肌梗塞', '胃食管反流'],
                    suggestions: '请立即就医，这可能是严重心脏问题的征兆。',
                    urgencyLevel: '高'
                };
            }
            else {
                this.aiDiagnosis = {
                    possibleDiseases: ['需进一步检查'],
                    suggestions: '根据您的描述，建议预约专科医生进行详细检查。',
                    urgencyLevel: '低'
                };
            }
        },
        
        recommendDoctors() {
            // 根据诊断结果推荐相关科室医生 - 模拟逻辑
            const diagnosis = this.aiDiagnosis.possibleDiseases[0];
            let department = '';
            
            if (diagnosis.includes('感冒') || diagnosis.includes('流感') || diagnosis.includes('呼吸道')) {
                department = '呼吸内科';
            } 
            else if (diagnosis.includes('肠胃') || diagnosis.includes('食物中毒')) {
                department = '胃肠外科';
            }
            else if (diagnosis.includes('心') || diagnosis.includes('胸痛')) {
                department = '心内科';
            }
            else {
                department = ''; // 不特定科室
            }
            
            this.recommendedDoctors = department 
                ? this.doctorDatabase.filter(d => d.department === department)
                : this.doctorDatabase.slice(0, 3); // 默认推荐3位医生
        },
        
        viewDoctorDetail(doctor) {
            // 这里可以跳转到医生详情页或显示详情对话框
            ElMessage.success(`已选择医生: ${doctor.name} (${doctor.hospital} ${doctor.department})`);
            console.log('医生详情:', doctor);
        }
    }
}
</script>

<style scoped>
.doctor-card {
    width: 200px;
    padding: 15px;
    margin: 10px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s;
}

.doctor-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.el-divider {
    margin: 15px 0;
}
</style>