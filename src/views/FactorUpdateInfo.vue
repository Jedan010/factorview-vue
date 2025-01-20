<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getFactorUpdate } from '@/api/factor'
import FactorUpdateInfoTable from '@/components/FactorUpdateInfoTable.vue'
import DatePicker from 'vue-datepicker-next'
import 'vue-datepicker-next/index.css'
import moment from 'moment'

onMounted(() => {
  fetchData()
})

const route = useRoute()
const factorNames = ref(
  route.query.factor_names
    ? (Array.isArray(route.query.factor_names)
      ? route.query.factor_names
      : [route.query.factor_names])
    : route.params.factorName
      ? [route.params.factorName]
      : []
)

const isDarkMode = ref(false)
function toggleDarkMode() {
  isDarkMode.value = !isDarkMode.value
  document.documentElement.classList.toggle('dark', isDarkMode.value)
}

const filters = ref({
  period: 'all',
  startDate: new Date('2024-01-01'),
  endDate: null
})

const loading = ref(false)
const error = ref(null)
const updateData = ref({})

function getDateRange(period) {
  const today = new Date()
  switch (period) {
    case 'ytd':
      return {
        startDate: new Date(today.getFullYear(), 0, 1).toISOString().split('T')[0],
        endDate: today.toISOString().split('T')[0]
      }
    case '3m':
      return {
        startDate: new Date(today.setMonth(today.getMonth() - 3)).toISOString().split('T')[0],
        endDate: new Date().toISOString().split('T')[0]
      }
    case '1y':
      return {
        startDate: new Date(today.setFullYear(today.getFullYear() - 1)).toISOString().split('T')[0],
        endDate: new Date().toISOString().split('T')[0]
      }
    case '3y':
      return {
        startDate: new Date(today.setFullYear(today.getFullYear() - 3)).toISOString().split('T')[0],
        endDate: new Date().toISOString().split('T')[0]
      }
    case '5y':
      return {
        startDate: new Date(today.setFullYear(today.getFullYear() - 5)).toISOString().split('T')[0],
        endDate: new Date().toISOString().split('T')[0]
      }
    default:
      return {
        startDate: '',
        endDate: ''
      }
  }
}

async function fetchData() {
  try {
    loading.value = true
    error.value = null

    const dateRange = getDateRange(filters.value.period)
    const params = {
      start_date: filters.value.period === 'all'
        ? (filters.value.startDate ? moment(filters.value.startDate).format('YYYY-MM-DD') : null)
        : (dateRange.startDate ? moment(dateRange.startDate).format('YYYY-MM-DD') : null),
      end_date: filters.value.period === 'all'
        ? (filters.value.endDate ? moment(filters.value.endDate).format('YYYY-MM-DD') : null)
        : (dateRange.endDate ? moment(dateRange.endDate).format('YYYY-MM-DD') : null),
      factor_names: factorNames.value.join(',')
    }

    const data = await getFactorUpdate(params)
    if (!data || typeof data !== 'object') {
      throw new Error('Invalid data format from API')
    }
    updateData.value = data
  } catch (err) {
    error.value = err
    console.error('Error fetching factor update data:', err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="factor-update-info" :class="{ 'dark-mode': isDarkMode }">
    <div class="header">
      <h1>因子更新日期统计</h1>
      <div class="header-controls">
        <button class="theme-toggle" @click="toggleDarkMode">
          <span class="theme-icon">
            {{ isDarkMode ? 'Dark Mode' : 'Light Mode' }}
          </span>
        </button>
        <router-link to="/factor" class="back-btn">返回因子列表</router-link>
      </div>
    </div>

    <div class="content">
      <div class="filters">
        <div class="filter-group">
          <label>时间周期</label>
          <select v-model="filters.period">
            <option value="all">自定义</option>
            <option value="ytd">年初至今</option>
            <option value="3m">近3个月</option>
            <option value="1y">近1年</option>
            <option value="3y">近3年</option>
            <option value="5y">近5年</option>
          </select>
        </div>

        <div class="filter-group">
          <label>日期范围</label>
          <div class="date-range-picker">
            <DatePicker v-model:value="filters.startDate" type="date" placeholder="开始日期" class="date-picker" />
            <span class="date-separator"> 至 </span>
            <DatePicker v-model:value="filters.endDate" type="date" placeholder="结束日期" class="date-picker" />
          </div>
        </div>

        <button class="apply-btn" @click="fetchData">应用筛选</button>
      </div>

      <div v-if="loading" class="loading-indicator">
        <div class="loader"></div>
        数据加载中...
      </div>

      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-else>
        <FactorUpdateInfoTable :factorData="updateData" />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '../assets/styles/base-factor';

.factor-update-info {
  @extend .base-container;
}
</style>