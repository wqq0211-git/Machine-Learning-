import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PredictView from '../views/PredictView.vue'
import BatchPredictView from '../views/BatchPredictView.vue'
import CompareView from '../views/CompareView.vue'
import DatasetView from '../views/DatasetView.vue'
import AboutView from '../views/AboutView.vue'

const routes = [
  { path: '/', component: HomeView, meta: { title: '首页' } },
  { path: '/predict', component: PredictView, meta: { title: '单图识别' } },
  { path: '/batch-predict', component: BatchPredictView, meta: { title: '批量预测' } },
  { path: '/compare', component: CompareView, meta: { title: '模型对比' } },
  { path: '/dataset', component: DatasetView, meta: { title: '数据集分析' } },
  { path: '/about', component: AboutView, meta: { title: '项目说明' } }
]

export default createRouter({
  history: createWebHistory(),
  routes
})

