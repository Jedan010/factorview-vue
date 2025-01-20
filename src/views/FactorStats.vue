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

      <div v-if="isLoading" class="loading-indicator">
        <div class="loader"></div>
        数据加载中
      </div>
      <div v-else>
        <FactorStatsTable ref="factorStatsTable" :factorData="response" />
      </div>

      <div class="button-controls">
        <div class="compare-buttons">
          <button class="compare-btn" @click="toggleBacktest">
            {{ showBacktest ? '隐藏回测收益对比' : '显示回测收益对比' }}
          </button>
          <button class="compare-btn" @click="toggleGroup">
            {{ showGroup ? '隐藏分组收益对比' : '显示分组收益对比' }}
          </button>
          <button class="compare-btn" @click="toggleIC">
            {{ showIC ? '隐藏IC对比' : '显示IC对比' }}
          </button>
        </div>
      </div>

      <div v-if="showBacktest && backtestLoading" class="loading-indicator">
        <div class="loader"></div>
        回测数据加载中...
      </div>

      <template v-if="showBacktest && !backtestLoading">
        <FactorStatsBacktest :backtestData="backtestData" />
        <FactorStatsBacktestTable :backtestData="backtestData" :isDarkMode="isDarkMode" />
      </template>

      <div v-if="showGroup && groupLoading" class="loading-indicator">
        <div class="loader"></div>
        分组数据加载中...
      </div>

      <template v-if="showGroup && !groupLoading && Object.keys(groupData).length > 0">
        <FactorStatsGroupPlot :groupData="groupData" />
        <FactorStatsGroupTable :groupData="groupData" :isDarkMode="isDarkMode" />
      </template>

      <div v-if="showIC && icLoading" class="loading-indicator">
        <div class="loader"></div>
        IC数据加载中...
      </div>

      <template v-if="showIC && !icLoading && Object.keys(icData).length > 0">
        <FactorStatsICPlot :icData="icData" :isDarkMode="isDarkMode" />
        <FactorStatsICTable :icData="icData" :isDarkMode="isDarkMode" />
      </template>

    </div>
  </div>
</template>

<script>
import { getFactorStats, getFactorStatsBacktest, getFactorStatsGroup, getFactorStatsIC } from '@/api/factor';
import moment from 'moment';
import FactorFilter from '@/components/Filter.vue';
import FactorStatsTable from '@/components/FactorStatsTable.vue';
import FactorStatsBacktest from '@/components/FactorStatsBacktest.vue';
import FactorStatsBacktestTable from '@/components/FactorStatsBacktestTable.vue';
import FactorStatsGroupPlot from '@/components/FactorStatsGroupPlot.vue';
import FactorStatsGroupTable from '@/components/FactorStatsGroupTable.vue';
import FactorStatsICPlot from '@/components/FactorStatsICPlot.vue';
import FactorStatsICTable from '@/components/FactorStatsICTable.vue';

export default {
  components: {
    FactorFilter,
    FactorStatsTable,
    FactorStatsBacktest,
    FactorStatsBacktestTable,
    FactorStatsGroupPlot,
    FactorStatsGroupTable,
    FactorStatsICPlot,
    FactorStatsICTable
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
      showBacktest: false,
      groupData: {},
      groupLoading: false,
      showGroup: false,
      icData: {},
      icLoading: false,
      showIC: false,
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
  methods: {
    async handleFiltersChange(filters) {
      this.currentFilters = filters;
      await this.fetchFactorStats();
      if (this.showBacktest) {
        await this.fetchBacktestData();
      }
      if (this.showGroup) {
        await this.fetchGroupData();
      }
      if (this.showIC) {
        await this.fetchICData();
      }
    },

    async fetchFactorStats() {
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
          factor_names: this.$route.query.factor_names
        };

        this.response = await getFactorStats(params);
      } catch (error) {
        console.error('Error fetching factor stats:', error);
        this.error = '因子统计数据加载失败，请稍后重试';
      } finally {
        this.isLoading = false;
      }
    },

    async fetchBacktestData() {
      this.backtestLoading = true;
      this.error = null;

      try {
        // 获取所有factor names
        const allFactorNames = this.$route.query.factor_names;

        // 优先使用勾选的factor names，如果没有勾选则使用所有factor names
        const selectedFactorNames = this.$refs.factorStatsTable?.selectedFactors.length > 0 ?
          this.$refs.factorStatsTable?.selectedFactors : allFactorNames;

        const params = {
          pool: this.currentFilters.pool,
          benchmark_index: this.currentFilters.benchmark,
          optimizer_index: this.currentFilters.optimizer,
          start_date: this.currentFilters.startDate ? moment(this.currentFilters.startDate).format('YYYY-MM-DD') : null,
          end_date: this.currentFilters.endDate ? moment(this.currentFilters.endDate).format('YYYY-MM-DD') : null,
          factor_names: selectedFactorNames
        };

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
      } catch (error) {
        console.error('Error fetching backtest data:', error);
        this.error = '回测数据加载失败，请稍后重试';
      } finally {
        this.backtestLoading = false;
      }
    },


    async fetchGroupData() {
      this.groupLoading = true;
      this.error = null;

      try {
        const params = {
          pool: this.currentFilters.pool,
          benchmark_index: this.currentFilters.benchmark,
          optimizer_index: this.currentFilters.optimizer,
          start_date: this.currentFilters.startDate ? moment(this.currentFilters.startDate).format('YYYY-MM-DD') : null,
          end_date: this.currentFilters.endDate ? moment(this.currentFilters.endDate).format('YYYY-MM-DD') : null,
          factor_names: this.$refs.factorStatsTable?.selectedFactors.length > 0 ?
            this.$refs.factorStatsTable?.selectedFactors : this.$route.query.factor_names || ["NoData"]
        };

        this.groupData = await getFactorStatsGroup(params);
      } catch (error) {
        console.error('Error fetching group data:', error);
        this.error = '分组数据加载失败，请稍后重试';
      } finally {
        this.groupLoading = false;
      }
    },
    async fetchICData() {
      this.icLoading = true;
      this.error = null;

      try {
        const params = {
          pool: this.currentFilters.pool,
          benchmark_index: this.currentFilters.benchmark,
          optimizer_index: this.currentFilters.optimizer,
          start_date: this.currentFilters.startDate ? moment(this.currentFilters.startDate).format('YYYY-MM-DD') : null,
          end_date: this.currentFilters.endDate ? moment(this.currentFilters.endDate).format('YYYY-MM-DD') : null,
          factor_names: this.$refs.factorStatsTable?.selectedFactors.length > 0 ?
            this.$refs.factorStatsTable?.selectedFactors : this.$route.query.factor_names || ["NoData"]
        };

        this.icData = await getFactorStatsIC(params);
      } catch (error) {
        console.error('Error fetching IC data:', error);
        this.error = 'IC数据加载失败，请稍后重试';
      } finally {
        this.icLoading = false;
      }
    },

    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      document.documentElement.classList.toggle('dark', this.isDarkMode);
    },

    async toggleBacktest() {
      this.showBacktest = !this.showBacktest;
      if (this.showBacktest) {
        this.backtestLoading = true;
        try {
          await this.fetchBacktestData();
        } catch (error) {
          console.error('Error fetching backtest data:', error);
          this.error = '回测数据加载失败，请稍后重试';
        } finally {
          this.backtestLoading = false;
        }
      }
    },

    async toggleGroup() {
      this.showGroup = !this.showGroup;
      if (this.showGroup) {
        this.groupLoading = true;
        try {
          await this.fetchGroupData();
        } catch (error) {
          console.error('Error fetching group data:', error);
          this.error = '分组数据加载失败，请稍后重试';
        } finally {
          this.groupLoading = false;
        }
      }
    },
    async toggleIC() {
      this.showIC = !this.showIC;
      if (this.showIC) {
        this.icLoading = true;
        try {
          await this.fetchICData();
        } catch (error) {
          console.error('Error fetching IC data:', error);
          this.error = 'IC数据加载失败，请稍后重试';
        } finally {
          this.icLoading = false;
        }
      }
    },

  },
  async mounted() {
    await this.fetchFactorStats();
    if (this.showBacktest) {
      await this.fetchBacktestData();
    }
    if (this.showGroup) {
      await this.fetchGroupData();
    }
    if (this.showIC) {
      await this.fetchICData();
    }
  }
};
</script>

<style scoped lang="scss">
@use '../assets/styles/base-factor';

.button-controls {
  display: flex;
  justify-content: flex-start;
  margin: 20px 0;
  padding: 10px;
  background: var(--background-color);
  border-radius: 8px;
}

.compare-buttons {
  display: flex;
  gap: 1rem;
}

.compare-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(145deg, #3498db, #2980b9);
  color: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 4px rgba(52, 152, 219, 0.2);
  cursor: pointer;
  font-weight: 500;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
    background: linear-gradient(145deg, #2980b9, #3498db);
  }

  &:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(52, 152, 219, 0.2);
  }
}

.dark-mode {
  .compare-btn {
    background: linear-gradient(145deg, #4a5568, #2d3748);
    border-color: #444444;

    &:hover {
      background: linear-gradient(145deg, #556677, #3a4758);
    }
  }
}

.factor-info-container {
  @extend .base-container;
}
</style>
