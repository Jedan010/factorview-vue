<template>
  <div class="factor-info-container" :class="{ 'dark-mode': isDarkMode }">

    <div class="header">
      <h1>因子表现统计</h1>

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
      <FactorFilter @apply-filters="handleFiltersChange" />

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <FactorStatsTable :factorData="response" />
      
      <div class="backtest-toggle">
        <button
          class="compare-btn"
          @click="toggleBacktest"
        >
          {{ showBacktest ? '隐藏回测收益对比' : '显示回测收益对比' }}
        </button>
        
        <div v-if="showBacktest && backtestLoading" class="loading-indicator">
          <div class="loader"></div>
          回测数据加载中...
        </div>
      </div>

      <template v-if="showBacktest && !backtestLoading">
        <FactorStatsBacktest v-if="backtestData.length > 0" :backtestData="backtestData" />
        <FactorStatsBacktestTable v-if="backtestData.length > 0" :backtestData="backtestData" :isDarkMode="isDarkMode" />
      </template>

    </div>
  </div>
</template>

<script>
import { getFactorStats, getFactorStatsBacktest } from '@/api/factor';
import moment from 'moment';
import FactorFilter from '@/components/Filter.vue';
import FactorStatsTable from '@/components/FactorStatsTable.vue';
import FactorStatsBacktest from '@/components/FactorStatsBacktest.vue';
import FactorStatsBacktestTable from '@/components/FactorStatsBacktestTable.vue';

export default {
  components: {
    FactorFilter,
    FactorStatsTable,
    FactorStatsBacktest,
    FactorStatsBacktestTable
  },
  name: 'FactorStats',
  data() {
    return {
      response: [],
      backtestData: [],
      backtestLoading: false,
      isLoading: false,
      error: null,
      isDarkMode: false,
      currentFilters: {
        pool: 'all',
        period: 'all',
        benchmark: '000905.SH',
        optimizer: '000905.SH',
        startDate: null,
        endDate: null
      }
    };
  },
  computed: {},
  methods: {

    handleFiltersChange(filters) {
      this.currentFilters = filters;
      this.fetchFactors();
    },

    async fetchFactors(fetchBacktest = false) {
      this.isLoading = true;
      this.error = null;

      try {
        const dateRange = this.currentFilters;
        const params = {
          pool: this.currentFilters.pool,
          benchmark_index: this.currentFilters.benchmark,
          optimizer_index: this.currentFilters.optimizer,
          start_date: this.currentFilters.period === 'all'
            ? (this.currentFilters.startDate ? moment(this.currentFilters.startDate).format('YYYY-MM-DD') : null)
            : (dateRange.startDate ? moment(dateRange.startDate).format('YYYY-MM-DD') : null),
          end_date: this.currentFilters.period === 'all'
            ? (this.currentFilters.endDate ? moment(this.currentFilters.endDate).format('YYYY-MM-DD') : null)
            : (dateRange.endDate ? moment(dateRange.endDate).format('YYYY-MM-DD') : null),

          factor_names: this.$route.query.factor_names ? (Array.isArray(this.$route.query.factor_names)
            ? this.$route.query.factor_names.join(',')
            : this.$route.query.factor_names) : null
        };

        this.response = await getFactorStats(params);
        if (fetchBacktest || this.showBacktest) {
          const backtestResponse = await getFactorStatsBacktest(params);
          this.backtestData = Object.entries(backtestResponse).map(([name, data]) => {
            const dates = data.index.map(date => moment(date).format('YYYY-MM-DD'));
            return {
              name,
              values: data.values.excess_ret,
              index: dates,
              index_ret: data.values.index_ret,
              holding_num: data.values.holding_num,
              turnover: data.values.turnover,
              transaction_fee: data.values.transaction_fee,
            };
          });
        }
      } catch (error) {
        console.error('Error fetching factors:', error);
        this.error = '数据加载失败，请稍后重试';
      } finally {
        this.isLoading = false;
      }
    },
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      document.documentElement.classList.toggle('dark', this.isDarkMode);
    },
    
    async toggleBacktest() {
      this.showBacktest = !this.showBacktest;
      if (this.showBacktest && this.backtestData.length === 0) {
        this.backtestLoading = true;
        try {
          await this.fetchFactors(true);
        } catch (error) {
          console.error('Error fetching backtest data:', error);
          this.error = '回测数据加载失败，请稍后重试';
        } finally {
          this.backtestLoading = false;
        }
      }
    }
  },
  mounted() {
    this.fetchFactors();
  }
};
</script>

<style scoped lang="scss">
@use '../assets/styles/base-factor';

.backtest-toggle {
  margin: 20px 0;
  text-align: center;
}

.compare-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(145deg, #3498db, #2980b9);
  color: white;
  border: none;
  border-radius: 8px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 4px rgba(52, 152, 219, 0.2);
  cursor: pointer;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
  }

  &:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(52, 152, 219, 0.2);
  }
}

.factor-info-container {
  @extend .base-container;
}
</style>
