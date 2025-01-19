<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  icData: {
    type: Object,
    required: true
  },
  isDarkMode: {
    type: Boolean,
    default: false
  }
})

const stats = computed(() => {
  return Object.entries(props.icData).map(([name, data]) => {
    if (!data || !data.values || !data.values.corr) return null
    
    const corrValues = data.values.corr
    const dates = data.index
    
    // Calculate IC statistics
    const meanIC = corrValues.reduce((sum, val) => sum + val, 0) / corrValues.length
    const stdDev = Math.sqrt(corrValues.reduce((sum, val) => sum + Math.pow(val - meanIC, 2), 0) / corrValues.length)
    const icir = stdDev !== 0 ? meanIC / stdDev : 0
    const tValue = stdDev !== 0 ? meanIC / (stdDev / Math.sqrt(corrValues.length)) : 0
    const positiveRatio = corrValues.filter(val => val > 0).length / corrValues.length
    
    return {
      name,
      meanIC: meanIC.toFixed(4),
      icir: icir.toFixed(4),
      tValue: tValue.toFixed(2),
      positiveRatio: (positiveRatio * 100).toFixed(2) + '%',
      startDate: dates[0],
      endDate: dates[dates.length - 1],
      period: dates.length
    }
  }).filter(Boolean)
})
</script>

<template>
  <div class="ic-stats-table" :class="{ 'dark-mode': isDarkMode }">
    <h2>IC 统计</h2>
    <table>
      <thead>
        <tr>
          <th>因子</th>
          <th>开始日期</th>
          <th>结束日期</th>
          <th>IC</th>
          <th>ICIR</th>
          <th>T值</th>
          <th>正IC比率</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stat in stats" :key="stat.name">
          <td>
            <RouterLink :to="`/factor/${stat.name}`">
              {{ stat.name }}
            </RouterLink>
          </td>
          <td>{{ stat.startDate }}</td>
          <td>{{ stat.endDate }}</td>
          <td>{{ stat.meanIC }}</td>
          <td>{{ stat.icir }}</td>
          <td>{{ stat.tValue }}</td>
          <td>{{ stat.positiveRatio }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.ic-stats-table {
  @extend .data-table;
  margin-top: 2rem;
  border-radius: 12px;
  overflow-x: auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 1rem;

  h2 {
    margin-bottom: 1rem;
    color: #2c3e50;
    font-size: 1.5rem;
    font-weight: 600;
  }

  table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;

    th,
    td {
      padding: 1rem;
      text-align: center;
      border-bottom: 1px solid #e2e8f0;
      font-size: 1rem;
      transition: all 0.2s ease;
    }
    
    td:first-child {
      text-align: left;
    }

    th {
      background: white;
      color: #2c3e50;
      font-weight: 600;
      position: sticky;
      top: 0;
      z-index: 2;
      border-bottom: 2px solid #e2e8f0;
      white-space: nowrap;

      &:hover {
        background: #f1f5f9;
      }
    }

    tr {
      transition: all 0.2s ease;
      transform-origin: center;

      &:nth-child(even) {
        background: #f8f9fa;
      }

      &:hover {
        background: #e2e8f0;
        transform: scale(1.01);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      }

      &:last-child td {
        border-bottom: none;
      }
    }
  }
}

.dark-mode {
  .ic-stats-table {
    h2 {
      color: #ffffff;
    }

    table {
      th {
        background: #2d2d2d;
        color: #ffffff;
      }

      tr {
        &:nth-child(even) {
          background: #3d3d3d;
        }

        &:hover {
          background: #4d4d4d;
        }
      }
    }
  }
}
</style>
