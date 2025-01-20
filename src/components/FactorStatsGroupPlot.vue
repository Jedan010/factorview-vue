<script setup>
import { ref, watch, onMounted } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  groupData: {
    type: Object,
    required: true
  }
})

const chart = ref(null)
let myChart = null

function initChart() {
  myChart = echarts.init(chart.value)

  const option = {
    title: {
      text: '分组多空收益',
      left: 'center',
      textStyle: {
        fontSize: 20,
        fontWeight: 'bold',
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      formatter: (params) => {
        let res = `${params[0].axisValue}<br>`
        params.forEach(item => {
          res += `${item.seriesName}: ${item.value.toFixed(4)}<br>`
        })
        return res
      }
    },
    legend: {
      bottom: 10,
      data: []
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: []
    },
    yAxis: {
      type: 'value',
      name: '累计收益',
      scale: true,
      axisLabel: {
        formatter: (value) => value.toFixed(2)
      }
    },
    series: []
  }

  myChart.setOption(option)
}

function calcNav(returns) {
  let nav = 1
  return returns.map(ret => {
    nav *= (1 + ret)
    return nav
  })
}

function updateChart() {
  if (!props.groupData || Object.keys(props.groupData).length === 0) return

  // Get first factor's dates
  const firstFactor = Object.values(props.groupData)[0]
  const dates = firstFactor.index

  const series = []
  
  // Add LS_Hedge returns
  Object.entries(props.groupData).forEach(([factorName, factorData]) => {
    const lsHedgeReturns = factorData.values.LS_Hedge
    if (lsHedgeReturns) {
      series.push({
        name: `${factorName}`,
        type: 'line',
        data: calcNav(lsHedgeReturns),
        lineStyle: {
          width: 2,
          // type: 'dashed'
        },
        symbol: 'none',
        showSymbol: false,
        smooth: true,
        animation: true
      })
    }
  })

  const option = {
    xAxis: {
      data: dates
    },
    legend: {
      data: series.map(s => s.name)
    },
    series
  }

  myChart.setOption(option)
}

onMounted(() => {
  initChart()
  updateChart()
})

watch(() => props.groupData, () => {
  updateChart()
}, { deep: true })
</script>

<template>
  <div ref="chart" class="factor-stats-group-chart"></div>
</template>

<style scoped>
.factor-stats-group-chart {
  width: 100%;
  height: 700px;
  margin-top: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.dark-mode .factor-stats-group-chart {
  background: #2d2d2d;
}
</style>
