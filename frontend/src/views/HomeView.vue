<template>
    <div class="home">
        <el-row :gutter="20">
            <el-col :span="12">
                <el-card>
                    <template #header>
                        <h2>📊 系统概览</h2>
                    </template>
                    <el-statistic title="测试用例总数" :value="stats.testCases">
                        <template #prefix>
                            <span>📝</span>
                        </template>
                    </el-statistic>
                    <el-statistic title="执行次数" :value="stats.executions">
                        <template #prefix>
                            <span>🔄</span>
                        </template>
                    </el-statistic>
                    <el-statistic title="成功率" :value="stats.successRate" suffix="%">
                        <template #prefix>
                            <span>✅</span>
                        </template>
                    </el-statistic>
                </el-card>
            </el-col>
            <el-col :span="12">
                <el-card>
                    <template #header>
                        <h2>⚡ 快速开始</h2>
                    </template>
                    <el-button type="primary" @click="$router.push('/test-cases')" size="large">
                        创建测试用例
                    </el-button>
                    <el-button @click="showQuickTest = true" size="large">
                        快速测试
                    </el-button>
                </el-card>
            </el-col>
        </el-row>

        <el-card style="margin-top: 20px;">
            <template #header>
                <h2>📋 最近执行记录</h2>
            </template>
            <el-table :data="recentExecutions" style="width: 100%">
                <el-table-column prop="test_case_name" label="测试用例" />
                <el-table-column prop="status" label="状态" width="100">
                    <template #default="scope">
                        <el-tag :type="scope.row.status === 'completed' ? 'success' : 'danger'">
                            {{ scope.row.status === 'completed' ? '成功' : '失败' }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="duration_seconds" label="耗时(秒)" width="100" />
                <el-table-column prop="created_at" label="执行时间" width="180" />
                <el-table-column label="操作" width="100">
                    <template #default="scope">
                        <el-button size="small" @click="$router.push(`/reports/${scope.row.id}`)">
                            查看报告
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>

        <el-dialog v-model="showQuickTest" title="快速测试" width="600px">
            <el-form :model="quickTestForm" label-width="100px">
                <el-form-item label="目标URL">
                    <el-input v-model="quickTestForm.url" placeholder="https://example.com" />
                </el-form-item>
                <el-form-item label="测试指令">
                    <el-input
                        v-model="quickTestForm.instruction"
                        type="textarea"
                        :rows="4"
                        placeholder="例如：点击登录按钮，输入用户名和密码，然后提交表单"
                    />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showQuickTest = false">取消</el-button>
                <el-button type="primary" @click="executeQuickTest">开始测试</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
    name: 'HomeView',
    setup() {
        const stats = ref({
            testCases: 0,
            executions: 0,
            successRate: 0
        })
        const recentExecutions = ref([])
        const showQuickTest = ref(false)
        const quickTestForm = ref({
            url: '',
            instruction: ''
        })

        const loadStats = async () => {
            try {
                const [testCasesRes, executionsRes] = await Promise.all([
                    axios.get('/api/test-cases'),
                    axios.get('/api/execution')
                ])

                stats.value.testCases = testCasesRes.data.length
                stats.value.executions = executionsRes.data.length

                const completed = executionsRes.data.filter(e => e.status === 'completed').length
                stats.value.successRate = executionsRes.data.length > 0
                    ? Math.round(completed / executionsRes.data.length * 100)
                    : 0

                recentExecutions.value = executionsRes.data.slice(0, 10)
            } catch (error) {
                console.error('加载统计失败:', error)
            }
        }

        const executeQuickTest = async () => {
            if (!quickTestForm.value.url || !quickTestForm.value.instruction) {
                alert('请填写完整信息')
                return
            }

            try {
                const testCase = await axios.post('/api/test-cases', {
                    name: `快速测试 - ${quickTestForm.value.url}`,
                    description: '快速测试',
                    instruction: quickTestForm.value.instruction,
                    start_url: quickTestForm.value.url
                })

                const execution = await axios.post('/api/execution/start', {
                    test_case_id: testCase.data.id
                })

                alert('测试已启动，请稍后查看报告')
                showQuickTest.value = false
                loadStats()
            } catch (error) {
                console.error('启动测试失败:', error)
                alert('启动测试失败，请检查后端服务')
            }
        }

        onMounted(() => {
            loadStats()
        })

        return {
            stats,
            recentExecutions,
            showQuickTest,
            quickTestForm,
            executeQuickTest
        }
    }
}
</script>
