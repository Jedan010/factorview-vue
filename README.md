# FactorView - 因子分析与策略研究平台

## 项目概况
FactorView 是一个基于 Vue 3 和 Python 的因子分析与策略研究平台，主要用于金融量化研究。平台提供了因子分析、策略回测、绩效评估等功能模块。

## 功能特性
- 因子信息展示与筛选
- 因子绩效分析
- 策略信息管理
- 回测结果可视化
- 绩效指标计算与展示
- 分组统计与IC分析

## 项目结构
```
factorview/
  ├── __init__.py          # Python包初始化
  ├── data_loader.py       # 数据加载模块
  ├── main.py              # 主程序入口
src/
  ├── api/                 # API接口
  │   ├── factor.js        # 因子相关接口
  │   └── strategy.js      # 策略相关接口
  ├── assets/              # 静态资源
  │   └── styles/          # 样式文件
  ├── components/          # Vue组件
  │   ├── BacktestChart.vue      # 回测图表
  │   ├── BacktestStatsTable.vue # 回测统计表
  │   ├── FactorInfoFilter.vue   # 因子筛选
  │   ├── FactorInfoTable.vue    # 因子信息表
  │   ├── FactorStats.vue        # 因子统计
  │   ├── FactorStatsTable.vue   # 因子统计表
  │   ├── Filter.vue             # 通用筛选组件
  │   ├── GroupChart.vue         # 分组图表
  │   ├── GroupStatsTable.vue    # 分组统计表
  │   ├── ICChart.vue            # IC分析图表
  │   └── ICTables.vue           # IC分析表格
  ├── router/              # 路由配置
  ├── views/               # 页面视图
  │   ├── FactorInfo.vue         # 因子信息页
  │   ├── FactorPerformance.vue  # 因子绩效页
  │   ├── FactorStats.vue        # 因子统计页
  │   ├── IndexPage.vue          # 首页
  │   ├── NotFound.vue           # 404页面
  │   ├── StrategyInfo.vue       # 策略信息页
  │   └── StrategyPerformance.vue# 策略绩效页
```

## 快速开始

### 环境要求
- Node.js v16+
- Python 3.8+
- MySQL 5.7+ (可选)

### 安装步骤
1. 克隆项目
```bash
git clone https://github.com/your-repo/factorview.git
cd factorview
```

2. 安装前端依赖
```bash
npm install
```

3. 安装Python依赖
```bash
pip install -r requirements.txt
```

## 使用

### 启动开发环境
```bash
# 启动前端开发服务器
npm run dev

# 启动后端服务
npm run backend
```

### 代码规范
- 前端遵循[Vue风格指南](https://v3.cn.vuejs.org/style-guide/)
- 后端遵循[PEP 8](https://www.python.org/dev/peps/pep-0008/)


## API文档
访问 [API文档](http://localhost:8000/docs) 查看完整API说明

## 贡献指南
欢迎提交Pull Request，请遵循以下步骤：
1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

## 许可证
本项目采用 [MIT License](LICENSE)