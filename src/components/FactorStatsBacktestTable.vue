<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  backtestData: {
    type: Array,
    required: true
  },
  isDarkMode: {
    type: Boolean,
    default: false
  }
})

const stats = computed(() => {
  return props.backtestData.map(data => {
    if (!data || !data.values || !data.index) return null
    
    const excessReturns = data.values || []
    const dates = data.index
    const firstDate = new Date(dates[0])
    const lastDate = new Date(dates[dates.length - 1])
    const totalYears = (lastDate - firstDate) / (1000 * 60 * 60 * 24 * 365)
    
    // 添加数据校验
    const holdingNums = data.holding_num || []
    const turnovers = data.turnover || []
    const fees = data.transaction_fee || []

    const avgPosition = holdingNums.length > 0 ? 
      (holdingNums.reduce((a, b) => a + b, 0) / holdingNums.length).toFixed(0) : 'N/A'
      
    const annualTurnover = turnovers.length > 0 ? 
      (turnovers.reduce((a, b) => a + b, 0) / totalYears).toFixed(0) : 'N/A'
      
    const annualFee = fees.length > 0 ? 
      ((fees.reduce((a, b) => a + b, 0) / totalYears) * 100).toFixed(2) + '%' : 'N/A'

    const perfStats = calcPerf(excessReturns)
    
    return {
      name: data.name,
      startDate: dates[0],
      endDate: dates[dates.length - 1],
      totalYears: totalYears.toFixed(1),
      cumulativeReturn: (perfStats.cumulativeReturn * 100).toFixed(2) + '%',
      annualizedReturn: (perfStats.annualizedReturn * 100).toFixed(2) + '%',
      annualizedVolatility: (perfStats.annualizedVolatility * 100).toFixed(2) + '%',
      maxDrawdown: (perfStats.maxDrawdown * 100).toFixed(2) + '%',
      sharpeRatio: perfStats.sharpeRatio.toFixed(2),
      calmarRatio: perfStats.calmarRatio.toFixed(2),
      avgPosition,
      annualTurnover,
      annualFee
    }
  }).filter(Boolean) // 过滤掉null值
})

function calcPerf(returns) {
  if (!returns || returns.length === 0) {
    return {
      cumulativeReturn: 0,
      annualizedReturn: 0,
      annualizedVolatility: 0,
      maxDrawdown: 0,
      sharpeRatio: 0,
      calmarRatio: 0
    }
  }

  const nav = [1.0]
  for (let i = 0; i < returns.length; i++) {
    nav.push(nav[i] * (1 + returns[i]))
  }
  
  let currentMax = nav[0]
  const drawdowns = [0]
  for (let i = 1; i < nav.length; i++) {
    if (nav[i] > currentMax) {
      currentMax = nav[i]
    }
    drawdowns.push(nav[i] / currentMax - 1)
  }
  const maxDrawdown = Math.min(...drawdowns)

  const cumulativeReturn = nav[nav.length - 1] - 1
  const annualizedReturn = Math.pow(1 + cumulativeReturn, 252 / returns.length) - 1
  const annualizedVolatility = Math.sqrt(252) * Math.sqrt(returns.reduce((sum, r) => sum + Math.pow(r, 2), 0) / returns.length)
  
  const sharpeRatio = annualizedVolatility !== 0 ? annualizedReturn / annualizedVolatility : 0
  const calmarRatio = maxDrawdown !== 0 ? annualizedReturn / Math.abs(maxDrawdown) : 0

  return {
    cumulativeReturn,
    annualizedReturn,
    annualizedVolatility,
    maxDrawdown,
    sharpeRatio,
    calmarRatio
  }
}
</script>

<template>
  <div class="backtest-stats-table" :class="{ 'dark-mode': isDarkMode }">
    <h2>回测收益统计</h2>
    <table>
      <thead>
        <tr>
          <th>策略</th>
          <th>开始日期</th>
          <th>结束日期</th>
          <th>总年数</th>
          <th>累计收益</th>
          <th>年化收益</th>
          <th>年化波动</th>
          <th>最大回撤</th>
          <th>夏普比率</th>
          <th>卡玛比率</th>
          <th>平均持仓</th>
          <th>年换手率</th>
          <th>年交易费率</th>
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
          <td>{{ stat.totalYears }}</td>
          <td>{{ stat.cumulativeReturn }}</td>
          <td>{{ stat.annualizedReturn }}</td>
          <td>{{ stat.annualizedVolatility }}</td>
          <td>{{ stat.maxDrawdown }}</td>
          <td>{{ stat.sharpeRatio }}</td>
          <td>{{ stat.calmarRatio }}</td>
          <td>{{ stat.avgPosition }}</td>
          <td>{{ stat.annualTurnover }}</td>
          <td>{{ stat.annualFee }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.backtest-stats-table {
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
  .backtest-stats-table {
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