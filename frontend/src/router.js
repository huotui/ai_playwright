import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import TestCaseList from './views/TestCaseList.vue'
import ExecutionReport from './views/ExecutionReport.vue'

const routes = [
    { path: '/', name: 'home', component: HomeView },
    { path: '/test-cases', name: 'test-cases', component: TestCaseList },
    { path: '/reports/:id', name: 'report', component: ExecutionReport }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
