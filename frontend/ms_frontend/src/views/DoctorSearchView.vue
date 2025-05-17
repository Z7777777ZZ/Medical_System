<template>
    <el-scrollbar height="100%" style="width: 100%;">
        <!-- 标题 -->
        <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold; ">医生查找</div>    

        <!-- 查询框 -->
        <div style="width:100%; margin-left: 50px; padding-top:5vh;">

            <el-input v-model="toSearch" :prefix-icon="Search" style="display:inline; " placeholder="输入查询关键字（医生姓名、科室、医院或专长）" @keyup.enter="searchDoctors"></el-input>
            <el-button style="margin-left: 10px;" type="primary" @click="searchDoctors" :loading="loading">查询</el-button>

            <!-- <el-select v-model="queryCond.sortBy" size="middle" style="width: 12.5vw; margin-left: 30px;">
                <el-option v-for="sortBy in sortBys" :key="sortBy.value" :label="sortBy.label" :value="sortBy.value" />
            </el-select>

            <el-select v-model="queryCond.sortOrder" size="middle" style="width: 12.5vw; margin-left: 30px;">
                <el-option v-for="sortOrder in sortOrders" :key="sortOrder.value" :label="sortOrder.label" :value="sortOrder.value" />
            </el-select> -->

        </div>

        <!-- 医生卡片显示区 -->
        <div style="display: flex;flex-wrap: wrap; justify-content: start;">

            <!-- 医生卡片 -->
            <div class="cardBox" v-for="(card, index) in filteredCards" :key="index">
                <div>
                    <!-- 卡片标题 -->
                    <div style="font-size: 24px; font-weight: bold;">No. {{ index + 1 }}</div>

                    <el-divider />

                    <!-- 卡片内容 -->
                    <div style="margin-left: 10px; text-align: start; font-size: 16px;">
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">姓名：</span>{{ card.name }}</p>
                        <p style="padding: 2.5px;overflow: hidden;text-overflow: ellipsis;white-space: nowrap;">
                            <span style="font-weight: bold;">电话：</span>{{ card.phone }}</p>
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">医院：</span>{{ card.hospital }}</p>
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">科室：</span>{{ card.department }}</p>
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">专长：</span>{{ card.specialty }}</p>
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">个人简介：</span>{{ card.bio }}</p>
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
    </el-scrollbar>
</template>

<script>
import { Search } from '@element-plus/icons-vue'
export default {
    name: 'doctor-search',
//   components: {

//   },
    data() {
        return {
            toSearch: '',
            Search,
            doctors: [
                {
                    name: '张医生',
                    phone: '13800138000',
                    hospital: '北京协和医院',
                    department: '心血管内科',
                    specialty: '冠心病、高血压',
                    bio: '从事心血管疾病诊疗20年，经验丰富'
                },
                {
                    name: '李医生',
                    phone: '13900139000',
                    hospital: '上海瑞金医院',
                    department: '神经外科',
                    specialty: '脑肿瘤、脑血管病',
                    bio: '神经外科主任医师，擅长微创手术'
                },
                {
                    name: '王医生',
                    phone: '13700137000',
                    hospital: '广州中山医院',
                    department: '儿科',
                    specialty: '儿童呼吸系统疾病',
                    bio: '儿科副主任医师，对儿童常见病有深入研究'
                },
                {
                    name: '赵医生',
                    phone: '13600136000',
                    hospital: '成都华西医院',
                    department: '骨科',
                    specialty: '关节置换、脊柱手术',
                    bio: '骨科主任医师，手术技术精湛'
                },
                {
                    name: '刘医生',
                    phone: '13500135000',
                    hospital: '武汉同济医院',
                    department: '眼科',
                    specialty: '白内障、青光眼',
                    bio: '眼科专家，已完成数千例眼科手术'
                }
            ],
            filteredCards: []
        }
    },
    created() {
        // 初始化时显示所有医生
        this.filteredCards = [...this.doctors];
    },
    methods: {
        searchDoctors() {
            if (!this.toSearch.trim()) {
                // 如果搜索框为空，显示所有医生
                this.filteredCards = [...this.doctors];
                return;
            }
            
            // 过滤医生数据，匹配姓名、医院、科室或专长
            this.filteredCards = this.doctors.filter(doctor => {
                const searchTerm = this.toSearch.toLowerCase();
                return (
                    doctor.name.toLowerCase().includes(searchTerm) ||
                    doctor.hospital.toLowerCase().includes(searchTerm) ||
                    doctor.department.toLowerCase().includes(searchTerm) ||
                    doctor.specialty.toLowerCase().includes(searchTerm)
                );
            });
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
</style>