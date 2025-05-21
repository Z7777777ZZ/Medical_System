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

            <!-- 添加AI生成提示 -->
            <div style="color: #999; font-size: 14px; margin-bottom: 15px; font-style: italic;">
                <el-icon><InfoFilled /></el-icon> 本回答由 AI 生成，内容仅供参考，请仔细甄别。
            </div>
            
            <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                <div style="font-weight: bold; color: #409EFF; margin-bottom: 10px;">可能疾病:</div>
                <div style="margin-left: 20px;">{{ aiDiagnosis.possibleDiseases.join('、') }}</div>
                
                <el-divider />
                
                <div style="font-weight: bold; color: #409EFF; margin-bottom: 10px;">建议:</div>
                <!-- <div style="margin-left: 20px;">{{ aiDiagnosis.suggestions }}</div> -->
                <div style="margin-left: 20px;">
                    <ul style="margin: 0; padding-left: 20px;">
                        <li v-for="(suggestion, index) in aiDiagnosis.suggestions" :key="index">
                            {{ suggestion }}
                        </li>
                    </ul>
                </div>
                
                <el-divider />
                
                <div style="font-weight: bold; color: #409EFF; margin-bottom: 10px;">紧急程度:</div>
                <el-tag :type="urgencyTagType" size="large">{{ aiDiagnosis.urgencyLevel }}</el-tag>

                <!-- 添加紧急程度备注显示 -->
                <div v-if="aiDiagnosis.urgencyNote" style="font-weight: bold; margin-top: 10px; color: #666; font-size: 15px;">
                    备注：{{ aiDiagnosis.urgencyNote }}
                </div>
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

                    <!-- 添加按钮区域 -->
                    <div style="margin-top: 15px; display: flex; justify-content: space-between;">
                        <el-button 
                            type="primary" 
                            size="small"
                            @click.stop="viewDoctorDetail(doctor)"
                        >
                            <el-icon><View /></el-icon>
                            详情
                        </el-button>
                        <el-button 
                            type="success" 
                            size="small"
                            @click.stop="bookAppointment(doctor)"
                        >
                            <el-icon><Calendar /></el-icon>
                            预约
                        </el-button>
                        <!-- <el-button 
                            type="info" 
                            size="small"
                            @click.stop="viewDoctorDetail(doctor)"
                        >
                            <el-icon><View /></el-icon>
                            详情
                        </el-button> -->
                    </div>
                </div>
            </div>
        </div>

        <!-- 预约对话框 -->
        <el-dialog v-model="appointmentDialogVisible" title="预约医生" width="30%" :destroy-on-close="true">
            <div v-if="selectedDoctor">
                <p>您正在预约: <strong>{{ selectedDoctor.name }}</strong></p>
                <p>科室: {{ selectedDoctor.department }}</p>
                <p>医院: {{ selectedDoctor.hospital }}</p>
                
                <el-form :model="appointmentForm" label-width="80px" style="margin-top: 20px;">
                    <el-form-item label="预约时间">
                        <el-date-picker
                            v-model="appointmentForm.date"
                            type="date"
                            placeholder="选择日期"
                            style="width: 100%"
                        />
                    </el-form-item>
                    <el-form-item label="时间段">
                        <el-select v-model="appointmentForm.timeSlot" placeholder="选择时间段" style="width: 100%">
                            <el-option label="上午 9:00-11:00" value="morning" />
                            <el-option label="下午 2:00-4:00" value="afternoon" />
                            <el-option label="晚上 6:00-8:00" value="evening" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="症状描述">
                        <el-input
                            v-model="appointmentForm.symptoms"
                            type="textarea"
                            :rows="3"
                            placeholder="请描述您的症状"
                        />
                    </el-form-item>
                </el-form>
            </div>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="appointmentDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="confirmAppointment">确认预约</el-button>
                </span>
            </template>
        </el-dialog>

        <!-- 使用医生详情子组件 -->
        <DoctorDetail 
            ref="doctorDetail" 
            @review-submitted="handleReviewSubmitted"
        />

        <!-- 医生详情对话框 改用子组件 v-model="detailDialogVisible" 设置为false -->
        <el-dialog v-model="detailDialogVisible" title="医生详情" width="40%" :destroy-on-close="true">
            <div v-if="selectedDoctor">
                <div style="display: flex; margin-bottom: 20px;">
                    <div style="flex: 1;">
                        <h3>{{ selectedDoctor.name }}</h3>
                        <p><strong>医院:</strong> {{ selectedDoctor.hospital }}</p>
                        <p><strong>科室:</strong> {{ selectedDoctor.department }}</p>
                        <p><strong>专长:</strong> {{ selectedDoctor.specialty }}</p>
                    </div>
                    <div style="flex: 1;">
                        <p><strong>简介:</strong></p>
                        <p>{{ selectedDoctor.bio || '暂无详细介绍' }}</p>
                    </div>
                </div>
                
                <div v-if="selectedDoctor.schedule" style="margin-top: 20px;">
                    <h4>出诊时间</h4>
                    <el-table :data="selectedDoctor.schedule" border style="width: 100%">
                        <el-table-column prop="day" label="星期" width="120" />
                        <el-table-column prop="time" label="时间段" />
                        <el-table-column prop="location" label="地点" />
                    </el-table>
                </div>
            </div>
        </el-dialog>
    </el-scrollbar>
</template>

<script>
import { Promotion, Calendar, View, InfoFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import DoctorDetail from '../components/DoctorDetailDialog.vue'

export default {
    name: 'AIDiagnosisView',
    components: {
        Promotion,
        Calendar,
        View,
        InfoFilled,
        DoctorDetail,
    },
    data() {
        return {
            symptomDescription: '',
            isLoading: false,
            showResults: false,
            aiDiagnosis: {
                possibleDiseases: [],
                suggestions: [],
                urgencyLevel: '',
                urgencyNote: '' // 添加备注字段
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
            ],

            // 预约相关数据
            appointmentDialogVisible: false,
            selectedDoctor: null,
            appointmentForm: {
                date: '',
                timeSlot: '',
                symptoms: ''
            },
            
            // 详情对话框
            detailDialogVisible: false,
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
        // submitSymptoms() {
        //     if (!this.symptomDescription.trim()) {
        //         ElMessage.warning('请输入症状描述');
        //         return;
        //     }

        //     this.isLoading = true;
            
        //     // 模拟AI诊断延迟
        //     setTimeout(() => {
        //         this.generateAIDiagnosis();
        //         this.recommendDoctors();
        //         this.showResults = true;
        //         this.isLoading = false;
        //     }, 1500);
        // },

        async submitSymptoms() {
            if (!this.symptomDescription.trim()) {
                ElMessage.warning('请输入症状描述');
                return;
            }

            this.isLoading = true;
            
            try {
                // 调用后端API
                const response = await axios.post('/aidiagnosis', {
                    prompt: this.symptomDescription
                });
                
                // 处理API响应
                this.aiDiagnosis = {
                    possibleDiseases: response.data.possibleDiseases || [],
                    suggestions: response.data.suggestions || [],
                    urgencyLevel: response.data.urgencyLevel || '低',
                    urgencyNote: response.data.urgencyNote || ''
                };
                
                // 根据诊断结果推荐医生
                // this.recommendDoctors();
                // 直接从响应中获取推荐的医生
                this.recommendedDoctors = response.data.recommendedDoctors || [];

                this.showResults = true;
                
            } catch (error) {
                console.error('API调用失败:', error);
                ElMessage.error('获取诊断结果失败，请稍后重试');
            } finally {
                this.isLoading = false;
            }
        },

        // 预约医生
        bookAppointment(doctor) {
            // 请接入实际的预约挂号接口
            ElMessage.warning('未接入实际的预约挂号接口');

            // 以下为模拟挂号
            this.selectedDoctor = doctor;
            // this.selectedDoctor = { ...doctor }; // 使用对象展开避免引用问题
            this.appointmentForm = {
                date: '',
                timeSlot: '',
                symptoms: this.symptomDescription
            };
            this.appointmentDialogVisible = true;
            // this.$nextTick(() => {
            //     this.appointmentDialogVisible = true;
            // });
        },
        
        // 确认预约
        confirmAppointment() {
            if (!this.appointmentForm.date) {
                ElMessage.warning('请选择预约日期');
                return;
            }
            if (!this.appointmentForm.timeSlot) {
                ElMessage.warning('请选择时间段');
                return;
            }
            
            // 这里应该调用预约API
            console.log('预约信息:', {
                doctor: this.selectedDoctor,
                appointment: this.appointmentForm
            });
            
            ElMessage.success(`已成功预约${this.selectedDoctor.name}医生`);
            this.appointmentDialogVisible = false;
        },
        
        // 查看医生详情 - 使用DoctorDetail组件
        viewDoctorDetail(doctor) {
            console.log('查看医生详情:', doctor);
            this.$refs.doctorDetail.show(doctor.doctor_id);
            
            // this.selectedDoctor = doctor;
            
            // // 模拟医生详情数据
            // this.selectedDoctor.bio = "资深医学专家，从事临床工作20余年，在相关领域有丰富经验。";
            // this.selectedDoctor.schedule = [
            //     { day: '周一', time: '上午 9:00-12:00', location: '门诊部3楼302室' },
            //     { day: '周三', time: '下午 2:00-5:00', location: '门诊部3楼302室' },
            //     { day: '周五', time: '上午 9:00-12:00', location: '门诊部3楼302室' }
            // ];
            
            // this.detailDialogVisible = true;
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
        
        // viewDoctorDetail(doctor) {
        //     // 这里可以跳转到医生详情页或显示详情对话框
        //     ElMessage.success(`已选择医生: ${doctor.name} (${doctor.hospital} ${doctor.department})`);
        //     console.log('医生详情:', doctor);
        // }
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

/* 按钮样式调整 */
.el-button {
    padding: 8px 12px;
}
</style>