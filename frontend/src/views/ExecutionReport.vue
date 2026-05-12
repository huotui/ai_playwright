<template>
    <div class="report">
        <el-card v-loading="loading">
            <template #header>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2>📊 测试报告 - {{ report.test_case_name }}</h2>
                    <el-tag :type="report.status === 'completed' ? 'success' : 'danger'" size="large">
                        {{ report.status === 'completed' ? '✅ 测试通过' : '❌ 测试失败' }}
                    </el-tag>
                </div>
            </template>

            <el-descriptions :column="2" border>
                <el-descriptions-item label="测试状态">
                    <el-tag :type="report.status === 'completed' ? 'success' : 'danger'">
                        {{ report.status === 'completed' ? '通过' : '失败' }}
                    </el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="执行耗时">
                    {{ report.duration_seconds.toFixed(2) }} 秒
                </el-descriptions-item>
                <el-descriptions-item label="执行时间" :span="2">
                    {{ report.created_at }}
                </el-descriptions-item>
                <el-descriptions-item label="测试结果" :span="2">
                    {{ report.result || '无' }}
                </el-descriptions-item>
            </el-descriptions>

            <el-divider>执行日志</el-divider>
            <div class="logs">
                <div v-for="(log, index) in report.logs" :key="index" class="log-item">
                    <el-tag size="small" type="info" style="margin-right: 10px;">
                        {{ index + 1 }}
                    </el-tag>
                    {{ log }}
                </div>
            </div>

            <el-divider v-if="report.screenshots.length > 0">截图</el-divider>
            <div v-if="report.screenshots.length > 0" class="screenshots">
                <div v-for="(screenshot, index) in report.screenshots" :key="index" class="screenshot-item">
                    <img :src="`data:image/png;base64,${screenshot}`" alt="截图" />
                    <p>截图 {{ index + 1 }}</p>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default {
    name: 'ExecutionReport',
    setup() {
        const route = useRoute()
        const report = ref({
            test_case_name: '',
            status: '',
            result: '',
            duration_seconds: 0,
            logs: [],
            screenshots: [],
            created_at: ''
        })
        const loading = ref(true)

        const loadReport = async () => {
            try {
                const response = await axios.get(`/api/reports/${route.params.id}`)
                report.value = response.data
            } catch (error) {
                console.error('加载报告失败:', error)
            } finally {
                loading.value = false
            }
        }

        onMounted(() => {
            loadReport()
            setInterval(loadReport, 3000)
        })

        return {
            report,
            loading
        }
    }
}
</script>

<style scoped>
.logs {
    max-height: 500px;
    overflow-y: auto;
    background: #f5f7fa;
    padding: 15px;
    border-radius: 4px;
}

.log-item {
    margin-bottom: 8px;
    font-family: monospace;
    font-size: 13px;
}

.screenshots {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.screenshot-item {
    text-align: center;
}

.screenshot-item img {
    max-width: 100%;
    max-height: 400px;
    border: 1px solid #ddd;
    border-radius: 4px;
}
</style>
