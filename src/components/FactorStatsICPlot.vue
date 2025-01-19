<template>
  <div class="ic-plot-container" :class="{ 'dark-mode': isDarkMode }">
    <div class="chart-container">
      <div ref="chart" class="chart"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import { onMounted, ref, computed } from 'vue';

export default {
  name: 'FactorStatsICPlot',
  props: {
    icData: {
      type: Object,
      required: true
    },
    isDarkMode: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const chart = ref(null);
    let myChart = null;

    const chartOptions = computed(() => {
      const series = [];
      const xAxisData = [];
      const legendData = [];

      // Process data for each factor
      Object.entries(props.icData).forEach(([factorName, factorData]) => {
        if (factorData.values && factorData.index) {
          // Add corr_roll series
          series.push({
            name: factorName,
            type: 'line',
            data: factorData.values.corr_roll,
            smooth: true,
            showSymbol: false
          });

          // Add to legend
          legendData.push(factorName);

          // Set xAxis data (use first factor's dates)
          if (xAxisData.length === 0) {
            xAxisData.push(...factorData.index);
          }
        }
      });

      return {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: legendData,
          textStyle: {
            color: props.isDarkMode ? '#fff' : '#333'
          }
        },
        xAxis: {
          type: 'category',
          data: xAxisData,
          axisLabel: {
            color: props.isDarkMode ? '#fff' : '#333'
          }
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            color: props.isDarkMode ? '#fff' : '#333'
          }
        },
        series,
        backgroundColor: props.isDarkMode ? '#1e1e1e' : '#fff'
      };
    });

    const initChart = () => {
      if (chart.value) {
        myChart = echarts.init(chart.value);
        myChart.setOption(chartOptions.value);
      }
    };

    const resizeChart = () => {
      if (myChart) {
        myChart.resize();
      }
    };

    onMounted(() => {
      initChart();
      window.addEventListener('resize', resizeChart);
    });

    return {
      chart
    };
  }
};
</script>

<style scoped lang="scss">
.ic-plot-container {
  margin: 20px 0;
  padding: 20px;
  background: var(--background-color);
  border-radius: 8px;

  .chart-container {
    width: 100%;
    height: 400px;

    .chart {
      width: 100%;
      height: 100%;
    }
  }
}
</style>
