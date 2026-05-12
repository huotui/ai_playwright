<template>
    <el-container>
        <el-header>
            <h1>🤖 AI Playwright MCP - 智能自动化测试平台</h1>
        </el-header>
        <el-container>
            <el-aside width="200px">
                <el-menu :default-active="activeMenu" router>
                    <el-menu-item index="/">
                        <span>首页</span>
                    </el-menu-item>
                    <el-menu-item index="/test-cases">
                        <span>测试用例</span>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main>
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

export default {
    name: 'App',
    setup() {
        const route = useRoute()
        const activeMenu = computed(() => route.path)
        return { activeMenu }
    }
}
</script>

<style>
body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.el-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    align-items: center;
}

.el-header h1 {
    font-size: 1.5rem;
    margin: 0;
}

.el-aside {
    background: #f5f7fa;
    border-right: 1px solid #e4e7ed;
    height: calc(100vh - 60px);
}

.el-main {
    padding: 20px;
}
</style>
