<script setup>
import { ref, watch, onMounted } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  backtestData: {
    type: Array,
    required: true
  }
})

const chart = ref(null)
let myChart = null

function initChart() {
  myChart = echarts.init(chart.value)

  const option = {
    title: {
      text: '多因子超额收益',
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
      name: '超额收益',
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
  if (!props.backtestData || props.backtestData.length === 0) return

  const dates = props.backtestData[0].index
  console.log('Backtest data:', props.backtestData);
  // 获取第一个因子的index收益
  const indexValues = props.backtestData[0]?.index_ret || [];
  console.log('Index values:', indexValues);

  const series = [
    // 添加index曲线

    // 添加各因子超额收益曲线
    ...props.backtestData.map((factor, index) => {
      const values = Array.isArray(factor.values) ? factor.values : [];
      return {
        name: factor.name,
        type: 'line',
        data: calcNav(values),
        lineStyle: {
          width: 2,
        },
        symbol: 'none',
        showSymbol: false,
        smooth: true,
        animation: true
      }
    },
    ), {
      name: '指数收益',
      type: 'line',
      data: calcNav(indexValues),
      lineStyle: {
        width: 2,
        type: 'dashed', // 虚线
        opacity: 0.7
      },
      symbol: 'none',
      showSymbol: false,
      smooth: true,
      animation: true
    },
  ]

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

watch(() => props.backtestData, () => {
  updateChart()
}, { deep: true })
</script>

<template>
  <div ref="chart" class="factor-stats-backtest-chart"></div>
</template>

<style scoped>
.factor-stats-backtest-chart {
  width: 100%;
  height: 700px;
  margin-top: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.dark-mode .factor-stats-backtest-chart {
  background: #2d2d2d;
}
</style>