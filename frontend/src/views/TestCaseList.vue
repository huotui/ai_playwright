<template>
    <div class="test-cases">
        <el-card>
            <template #header>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2>📝 测试用例管理</h2>
                    <el-button type="primary" @click="showCreateDialog = true">
                        创建测试用例
                    </el-button>
                </div>
            </template>

            <el-table :data="testCases" style="width: 100%">
                <el-table-column prop="name" label="名称" />
                <el-table-column prop="instruction" label="测试指令" show-overflow-tooltip />
                <el-table-column prop="start_url" label="目标URL" show-overflow-tooltip width="200" />
                <el-table-column prop="tags" label="标签" width="150">
                    <template #default="scope">
                        <el-tag v-for="tag in scope.row.tags" :key="tag" size="small" style="margin-right: 5px;">
                            {{ tag }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="created_at" label="创建时间" width="180" />
                <el-table-column label="操作" width="250">
                    <template #default="scope">
                        <el-button size="small" type="primary" @click="executeTest(scope.row.id)">
                            执行
                        </el-button>
                        <el-button size="small" @click="editTestCase(scope.row)">
                            编辑
                        </el-button>
                        <el-button size="small" type="danger" @click="deleteTestCase(scope.row.id)">
                            删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>

        <el-dialog v-model="showCreateDialog" :title="editingId ? '编辑测试用例' : '创建测试用例'" width="600px">
            <el-form :model="form" label-width="100px">
                <el-form-item label="名称">
                    <el-input v-model="form.name" placeholder="输入测试用例名称" />
                </el-form-item>
                <el-form-item label="描述">
                    <el-input v-model="form.description" type="textarea" :rows="2" placeholder="简要描述测试内容" />
                </el-form-item>
                <el-form-item label="测试指令">
                    <el-input v-model="form.instruction" type="textarea" :rows="4" placeholder="用自然语言描述测试步骤" />
                </el-form-item>
                <el-form-item label="目标URL">
                    <el-input v-model="form.start_url" placeholder="https://example.com" />
                </el-form-item>
                <el-form-item label="标签">
                    <el-input v-model="form.tags" placeholder="逗号分隔，如：登录, 冒烟测试" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showCreateDialog = false; editingId = null">取消</el-button>
                <el-button type="primary" @click="saveTestCase">保存</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
    name: 'TestCaseList',
    setup() {
        const router = useRouter()
        const testCases = ref([])
        const showCreateDialog = ref(false)
        const editingId = ref(null)
        const form = ref({
            name: '',
            description: '',
            instruction: '',
            start_url: '',
            tags: ''
        })

        const loadTestCases = async () => {
            try {
                const response = await axios.get('/api/test-cases')
                testCases.value = response.data
            } catch (error) {
                console.error('加载测试用例失败:', error)
            }
        }

        const saveTestCase = async () => {
            try {
                const data = {
                    name: form.value.name,
                    description: form.value.description,
                    instruction: form.value.instruction,
                    start_url: form.value.start_url,
                    tags: form.value.tags.split(',').map(t => t.trim()).filter(t => t)
                }

                if (editingId.value) {
                    await axios.put(`/api/test-cases/${editingId.value}`, data)
                    ElMessage.success('测试用例已更新')
                } else {
                    await axios.post('/api/test-cases', data)
                    ElMessage.success('测试用例已创建')
                }

                showCreateDialog.value = false
                editingId.value = null
                loadTestCases()
            } catch (error) {
                console.error('保存测试用例失败:', error)
                ElMessage.error('保存失败')
            }
        }

        const editTestCase = (testCase) => {
            editingId.value = testCase.id
            form.value = {
                name: testCase.name,
                description: testCase.description,
                instruction: testCase.instruction,
                start_url: testCase.start_url,
                tags: testCase.tags ? testCase.tags.join(', ') : ''
            }
            showCreateDialog.value = true
        }

        const deleteTestCase = async (id) => {
            try {
                await ElMessageBox.confirm('确定要删除此测试用例吗？', '确认删除')
                await axios.delete(`/api/test-cases/${id}`)
                ElMessage.success('测试用例已删除')
                loadTestCases()
            } catch (error) {
                if (error !== 'cancel') {
                    console.error('删除测试用例失败:', error)
                }
            }
        }

        const executeTest = async (testCaseId) => {
            try {
                const response = await axios.post('/api/execution/start', {
                    test_case_id: testCaseId,
                    headless: false
                })
                ElMessage.success('测试已启动，请稍候...')
                setTimeout(() => {
                    router.push(`/reports/${response.data.id}`)
                }, 1000)
            } catch (error) {
                console.error('启动测试失败:', error)
                ElMessage.error('启动测试失败，请检查后端服务和OpenAI API Key配置')
            }
        }

        onMounted(() => {
            loadTestCases()
        })

        return {
            testCases,
            showCreateDialog,
            editingId,
            form,
            saveTestCase,
            editTestCase,
            deleteTestCase,
            executeTest
        }
    }
}
</script>
