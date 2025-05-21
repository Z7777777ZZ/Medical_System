<template>
    <el-scrollbar height="100%" style="width: 100%;">
        <!-- 标题 -->
        <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold; ">医生查找</div>    

        <!-- 查询框 -->
        <div style="width:100%; margin-left: 50px; padding-top:5vh;">

            <el-input v-model="toSearch" :prefix-icon="Search" style="display:inline;" placeholder="输入姓名、专长、科室等" @keyup.enter="searchDoctors"></el-input>
            
            <el-select v-model="selectedHospital" clearable placeholder="选择医院" style="width: 200px; margin-left: 10px;">
                <el-option v-for="hospital in hospitals" :key="hospital.hospital_id" 
                    :label="hospital.name" :value="hospital.name" />
            </el-select>

            <el-select v-model="selectedDepartment" clearable placeholder="选择科室" style="width: 200px; margin-left: 10px;">
                <el-option v-for="dept in departments" :key="dept.department_id" 
                    :label="dept.name" :value="dept.name" />
            </el-select>
            
            <el-button style="margin-left: 10px;" type="primary" @click="searchDoctors" :loading="loading">查询</el-button>

            <!-- <el-select v-model="queryCond.sortBy" size="middle" style="width: 12.5vw; margin-left: 30px;">
                <el-option v-for="sortBy in sortBys" :key="sortBy.value" :label="sortBy.label" :value="sortBy.value" />
            </el-select>

            <el-select v-model="queryCond.sortOrder" size="middle" style="width: 12.5vw; margin-left: 30px;">
                <el-option v-for="sortOrder in sortOrders" :key="sortOrder.value" :label="sortOrder.label" :value="sortOrder.value" />
            </el-select> -->

        </div>

        <!-- 医生卡片显示区 -->
        <div style="display: flex; flex-wrap: wrap; justify-content: start; margin-bottom: 30px;">

            <!-- 医生卡片 -->
            <div class="cardBox" v-for="(card, index) in filteredCards" :key="index">
                <div>
                    <!-- 卡片标题 -->
                    <div class="card-title" style="font-size: 24px; font-weight: bold;">No. {{ index + 1 }}</div>

                    <el-divider style="margin: 15px 0;" />

                    <!-- 卡片内容 -->
                    <div style="margin-left: 10px; text-align: start; font-size: 16px;">
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">姓名：</span>{{ card.name }}</p>
                        <p style="padding: 2.5px;overflow: hidden;text-overflow: ellipsis;white-space: nowrap;">
                            <span style="font-weight: bold;">电话：</span>{{ card.phone }}</p>
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">医院：</span>{{ card.hospital }}</p>
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">科室：</span>{{ card.department }}</p>

                        <p style="padding: 2.5px;"><span style="font-weight: bold;">专长：</span>{{ card.specialty }}</p>
                        <!-- <p style="padding: 2.5px;"><span style="font-weight: bold;">个人简介：</span>{{ card.bio }}</p> -->

                        <!-- 添加评分展示 -->
                        <div style="padding: 2.5px; display: flex; align-items: center;">
                            <span style="font-weight: bold;">评分：</span>
                            <el-rate 
                                v-model="card.average_rating" 
                                disabled 
                                show-score 
                                text-color="#ff9900"
                                :score-template="`${card.average_rating.toFixed(1)} 分`"
                                style="margin-left: 0px;"
                            />
                            <!-- <span style="margin-left: 5px; color: #999; font-size: 14px;">
                                ({{ card.review_count || 0 }}条评价)
                            </span> -->
                        </div>
                    </div>

                    <!-- <el-divider style="margin: 15px 0;" /> -->
                    <el-divider style="margin-top: 15px; margin-bottom: 10px;" />

                    <!-- 卡片操作 -->
                    <div style="margin-left: 10px; display: flex; justify-content: space-between;">
                        <el-button 
                            type="primary" 
                            size="small"
                            @click="showDoctorDetail(card)"
                        >
                            <el-icon><View /></el-icon>
                            详情
                        </el-button>

                        <!-- 预约按钮 -->
                        <el-button 
                            type="success" 
                            size="small"
                            @click="bookAppointment(card)"
                        >
                            <el-icon><Calendar /></el-icon>
                            预约
                        </el-button>
                    </div>

                    <!-- <el-divider /> -->

                    <!-- 卡片操作 -->
                    <!-- <div style="margin-top: 5px;">
                        <el-button type="danger" :icon="Delete" round
                            @click="this.toRemove = card.cardId, this.removeCardVisible = true" >删除</el-button>
                    </div> -->

                </div>
            </div>

            <!-- 新建借书证卡片 -->
            <!-- <el-button class="newCardBox"
                @click="newCardInfo.name = '', newCardInfo.department = '', newCardInfo.type = '学生', newCardVisible = true">
                <el-icon style="height: 50px; width: 50px;">
                    <Plus style="height: 100%; width: 100%;" />
                </el-icon>
            </el-button> -->

        </div>

        <!-- 使用医生详情子组件 -->
        <DoctorDetail 
            ref="doctorDetail" 
        />

        <!-- 医生详情对话框 改用子组件 v-model="detailDialogVisible" 设置为false -->
        <el-dialog v-model="detailDialogVisible" title="医生详情" width="50%">
            <div v-if="selectedDoctor">
                <div style="display: flex; margin-bottom: 20px;">
                    <div style="flex: 1;">
                        <h3>{{ selectedDoctor.name }}</h3>
                        <p><strong>医院:</strong> {{ selectedDoctor.hospital }}</p>
                        <p><strong>科室:</strong> {{ selectedDoctor.department }}</p>
                        <p><strong>专长:</strong> {{ selectedDoctor.specialty }}</p>
                        <p><strong>电话:</strong> {{ selectedDoctor.phone }}</p>
                        
                        <!-- 评分展示 -->
                        <div style="margin-top: 10px;">
                            <el-rate 
                                v-model="selectedDoctor.average_rating" 
                                disabled 
                                show-score 
                                text-color="#ff9900" 
                                score-template="{value} 分"
                            />
                            <span style="margin-left: 10px; color: #999;">
                                ({{ selectedDoctor.review_count || 0 }}条评价)
                            </span>
                        </div>
                    </div>
                    <div style="flex: 1;">
                        <p><strong>简介:</strong></p>
                        <p>{{ selectedDoctor.bio || '暂无详细介绍' }}</p>
                    </div>
                </div>
                
                <!-- 评价区域 -->
                <el-tabs type="border-card">
                    <el-tab-pane label="患者评价">
                        <div v-if="doctorReviews.length > 0">
                            <div v-for="review in doctorReviews" :key="review.review_id" style="margin-bottom: 15px; padding: 10px; border-bottom: 1px solid #eee;">
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
                    
                    <el-tab-pane label="添加评价">
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

        <!-- 新增预约对话框 -->
        <el-dialog v-model="appointmentDialogVisible" title="预约医生" width="30%" :destroy-on-close="true">
            <div v-if="appointment_selectedDoctor">
                <p>您正在预约: <strong>{{ appointment_selectedDoctor.name }}</strong></p>
                <p>科室: {{ appointment_selectedDoctor.department }}</p>
                <p>医院: {{ appointment_selectedDoctor.hospital }}</p>
                
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
    </el-scrollbar>
</template>

<script>
import { Search, View, Calendar } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import DoctorDetail from '../components/DoctorDetailDialog.vue'

export default {
    name: 'doctor-search',
    components: {
        View,
        Calendar,
        DoctorDetail
    },
    data() {
        return {
            toSearch: '',
            Search,
            doctors: [
                {
                    name: '张三',
                    phone: '13800138000',
                    hospital: '北京协和医院',
                    department: '心血管内科',
                    specialty: '冠心病、高血压',
                    bio: '从事心血管疾病诊疗20年，经验丰富'
                },
                {
                    name: '李四',
                    phone: '13900139000',
                    hospital: '上海瑞金医院',
                    department: '神经外科',
                    specialty: '脑肿瘤、脑血管病',
                    bio: '神经外科主任医师，擅长微创手术'
                },
                {
                    name: '王五',
                    phone: '13700137000',
                    hospital: '广州中山医院',
                    department: '儿科',
                    specialty: '儿童呼吸系统疾病',
                    bio: '儿科副主任医师，对儿童常见病有深入研究'
                },
                {
                    name: '赵云',
                    phone: '13600136000',
                    hospital: '成都华西医院',
                    department: '骨科',
                    specialty: '关节置换、脊柱手术',
                    bio: '骨科主任医师，手术技术精湛'
                },
                {
                    name: '刘备',
                    phone: '13500135000',
                    hospital: '武汉同济医院',
                    department: '眼科',
                    specialty: '白内障、青光眼',
                    bio: '眼科专家，已完成数千例眼科手术'
                },
                {
                    name: '张伟',
                    phone: '13800001111',
                    hospital: '北京协和医院',
                    department: '内科',
                    specialty: '呼吸系统疾病',
                    bio: '毕业于北京医科大学，从事呼吸系统疾病研究20年'
                },
                {
                    name: '王芳',
                    phone: '13800002222',
                    hospital: '北京协和医院',
                    department: '妇产科',
                    specialty: '妇科肿瘤',
                    bio: '妇科肿瘤专家，擅长妇科恶性肿瘤的诊断与治疗'
                },
                {
                    name: '李明',
                    phone: '13800003333',
                    hospital: '北京协和医院',
                    department: '外科',
                    specialty: '胃肠外科',
                    bio: '擅长微创手术和胃肠道肿瘤手术'
                },
                {
                    name: '赵华',
                    phone: '13800004444',
                    hospital: '上海瑞金医院',
                    department: '骨科',
                    specialty: '骨折创伤',
                    bio: '专注于复杂骨折和创伤修复'
                },
                {
                    name: '刘洋',
                    phone: '13800005555',
                    hospital: '上海瑞金医院',
                    department: '心脏内科',
                    specialty: '冠心病',
                    bio: '心脏介入治疗专家'
                },
                {
                    name: '陈晓',
                    phone: '13800006666',
                    hospital: '广州南方医院',
                    department: '肿瘤科',
                    specialty: '肺癌治疗',
                    bio: '肺癌靶向治疗和免疫治疗专家'
                },
                {
                    name: '杨红',
                    phone: '13800007777',
                    hospital: '广州南方医院',
                    department: '眼科',
                    specialty: '白内障手术',
                    bio: '高级眼科医师，擅长各类眼科疾病诊疗'
                },
            ],
            filteredCards: [],
            loading: false,

            selectedHospital: null,
            selectedDepartment: null,
            hospitals: [],
            departments: [],

            // 医生详情相关
            detailDialogVisible: false,
            selectedDoctor: null,
            doctorReviews: [],
            reviewForm: {
                rating: 5,
                comment: ''
            },

            // 预约相关数据
            appointmentDialogVisible: false,
            appointment_selectedDoctor: null,
            appointmentForm: {
                date: '',
                timeSlot: '',
                symptoms: ''
            },
        }
    },
    async created() {
        // 初始化时加载医院和科室数据
        await this.fetchHospitals();
        await this.fetchDepartments();
        // 初始化时加载所有医生
        // this.filteredCards = [...this.doctors];
        this.searchDoctors();
    },
    methods: {
        async fetchHospitals() {
            try {
                const response = await axios.get('/hospitals');
                this.hospitals = response.data;
            } catch (error) {
                console.error('获取医院列表失败:', error);
                ElMessage.error('获取医院列表失败');
            }
        },
        async fetchDepartments() {
            try {
                const response = await axios.get('/departments');
                this.departments = response.data;
            } catch (error) {
                console.error('获取科室列表失败:', error);
                ElMessage.error('获取科室列表失败');
            }
        },
        async searchDoctors() {
            // 前端模拟数据
            // if (!this.toSearch.trim()) {
            //     // 如果搜索框为空，显示所有医生
            //     this.filteredCards = [...this.doctors];
            //     return;
            // }
            
            // // 过滤医生数据，匹配姓名、医院、科室或专长
            // this.filteredCards = this.doctors.filter(doctor => {
            //     const searchTerm = this.toSearch.toLowerCase();
            //     return (
            //         doctor.name.toLowerCase().includes(searchTerm) ||
            //         doctor.hospital.toLowerCase().includes(searchTerm) ||
            //         doctor.department.toLowerCase().includes(searchTerm) ||
            //         doctor.specialty.toLowerCase().includes(searchTerm)
            //     );
            // });

            // if (this.filteredCards.length === 0) {
            //     ElMessage.warning('没有找到匹配的医生');
            // }

            // 前后端集成
            this.loading = true;
            try {
                // const response = await axios.get('/doctors/search',{
                //     params: {
                //         query: this.toSearch,
                //     }
                // });

                const params = {
                    query: this.toSearch,
                };
                
                if (this.selectedHospital) {
                    params.hospital = this.selectedHospital;
                }
                
                if (this.selectedDepartment) {
                    params.department = this.selectedDepartment;
                }

                const response = await axios.get('/doctors/search', { params });

                this.filteredCards = response.data;
                // this.filteredCards = response.data.map(doctor => ({
                //     ...doctor,
                //     average_rating: doctor.average_rating || 0,
                //     review_count: doctor.review_count || 0
                // }));

                if (this.filteredCards.length === 0) {
                    ElMessage.warning('没有找到匹配的医生');
                }
            } catch (error) {
                console.error('搜索医生失败：', error);
                ElMessage.error('搜索医生失败，请稍后再试');
            } finally {
                this.loading = false;
            }
        },

        // 显示医生详情
        async showDoctorDetail(doctor) {
            // 改用子组件
            this.$refs.doctorDetail.show(doctor.doctor_id);

            // this.selectedDoctor = doctor;
            // try {
            //     // 重新获取医生详情数据（包括最新评分和评论数量）
            //     const doctorResponse = await axios.get(`/doctors/${doctor.doctor_id}`);
            //     this.selectedDoctor = doctorResponse.data;

            //     // 获取医生评价
            //     const response = await axios.get(`/doctors/${doctor.doctor_id}/reviews`);
            //     this.doctorReviews = response.data;
                
            //     // 重置评价表单
            //     this.reviewForm = {
            //         rating: 5,
            //         comment: ''
            //     };
                
            //     this.detailDialogVisible = true;
            // } catch (error) {
            //     console.error('获取医生评价失败:', error);
            //     ElMessage.error('获取医生详情失败');
            // }
        },

        // 处理评价提交事件
        handleReviewSubmitted() {
            // 刷新医生列表
            this.searchDoctors();
        },
        
        // 提交评价
        async submitReview() {
            if (!this.reviewForm.rating) {
                ElMessage.warning('请选择评分');
                return;
            }
            
            try {
                await axios.post('/reviews', {
                    doctor_id: this.selectedDoctor.doctor_id,
                    patient_id: 1, // 这里应该是当前登录患者的ID，暂时用1代替
                    rating: this.reviewForm.rating,
                    comment: this.reviewForm.comment
                });
                
                ElMessage.success('评价提交成功');
                // 刷新医生列表
                await this.searchDoctors();

                // // 重新获取医生详情数据（包括最新评分和评论数量）
                // const doctorResponse = await axios.get(`/doctors/${this.selectedDoctor.doctor_id}`);
                // this.selectedDoctor = doctorResponse.data;
                
                // // 重新获取评论列表
                // const reviewsResponse = await axios.get(`/doctors/${this.selectedDoctor.doctor_id}/reviews`);
                // this.doctorReviews = reviewsResponse.data;
                
                // // 重置评价表单
                // this.reviewForm = {
                //     rating: 5,
                //     comment: ''
                // };

                // 刷新评价列表
                await this.showDoctorDetail(this.selectedDoctor);
            } catch (error) {
                console.error('提交评价失败:', error);
                ElMessage.error('提交评价失败');
            }
        },

        // 预约医生
        bookAppointment(doctor) {
            // 请接入实际的预约挂号接口
            ElMessage.warning('未接入实际的预约挂号接口');

            // 以下为模拟挂号
            this.appointment_selectedDoctor = doctor;
            this.appointmentForm = {
                date: '',
                timeSlot: '',
                symptoms: ''
            };
            this.appointmentDialogVisible = true;
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
                doctor: this.appointment_selectedDoctor,
                appointment: this.appointmentForm
            });
            
            ElMessage.success(`已成功预约${this.appointment_selectedDoctor.name}医生`);
            this.appointmentDialogVisible = false;
        },
    },
}
</script>

<style scoped>
.cardBox {
    height: 350px;
    width: 240px;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    text-align: center;
    margin-top: 40px;
    margin-left: 27.5px;
    margin-right: 10px;
    padding: 7.5px;
    padding-right: 10px;
    padding-top: 15px;
}

.cardBox:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.el-button {
    margin-top: 10px;
}
</style>