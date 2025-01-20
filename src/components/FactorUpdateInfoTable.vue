<template>
  <div class="data-table">
    <table>
      <thead>
        <tr>
          <th v-for="column in columns" :key="column.key" @click="sortTable(column.key)">
            {{ column.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(factor, name) in sortedFactors" :key="name">
          <td>
            <router-link :to="`/factor/${factor.name}`" class="factor-link">
              {{ factor.name }}
            </router-link>
          </td>
          <td>
            <span :class="['status', { 'completed': factor.miss_num === 0 }]">
              {{ factor.miss_num === 0 ? '已完成' : '未完成' }}
            </span>
          </td>
          <td>{{ formatDate(factor.start_date) }}</td>
          <td>{{ formatDate(factor.end_date) }}</td>
          <td>{{ factor.date_num }}</td>
          <td>{{ factor.miss_num }}</td>
          <td :title="factor.miss_dates">{{ formatMissDates(factor.miss_dates) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { computed, ref } from 'vue'

export default {
  props: {
    factorData: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const columns = [
      { key: 'name', label: '因子名称' },
      { key: 'update_status', label: '更新状态' },
      { key: 'start_date', label: '开始日期' },
      { key: 'end_date', label: '结束日期' },
      { key: 'date_num', label: '总日期数' },
      { key: 'miss_num', label: '缺失日期数' },
      { key: 'miss_dates', label: '缺失日期列表' }
    ]

    const sortColumn = ref('name')
    const sortOrder = ref('asc')

    const sortedFactors = computed(() => {
      return Object.entries(props.factorData).map(([name, factor]) => ({
        name,
        ...factor
      })).sort((a, b) => {
        let valueA = a[sortColumn.value] || a.name
        let valueB = b[sortColumn.value] || b.name

        if (sortColumn.value === 'update_status') {
          valueA = a.miss_num === 0 ? 1 : 0
          valueB = b.miss_num === 0 ? 1 : 0
        }

        if (typeof valueA === 'number' && typeof valueB === 'number') {
          return sortOrder.value === 'asc' ? valueA - valueB : valueB - valueA
        }

        if (valueA < valueB) return sortOrder.value === 'asc' ? -1 : 1
        if (valueA > valueB) return sortOrder.value === 'asc' ? 1 : -1
        return 0
      })
    })

    const sortTable = (column) => {
      if (sortColumn.value === column) {
        sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
      } else {
        sortColumn.value = column
        sortOrder.value = 'asc'
      }
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString()
    }

    const formatMissDates = (dates) => {
      if (!dates) return ''
      const dateList = dates.split(',')
      if (dateList.length <= 3) {
        return dates
      }
      return `${dateList.slice(0, 3).join(', ')}...`
    }

    return {
      columns,
      sortColumn,
      sortOrder,
      sortedFactors,
      sortTable,
      formatDate,
      formatMissDates
    }
  }
}
</script>

<style scoped lang="scss">
@use '../assets/styles/base-factor';
.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
  font-weight: 500;
  color: #fff;
  background-color: #f44336;
}

.status.completed {
  background-color: #4caf50;
}
</style>