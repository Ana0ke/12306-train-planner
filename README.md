# 12306省心小助手 🚂

> 一站式火车出行规划 + 旅游攻略助手

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ 功能特色

### 🔍 智能路线规划
- 输入出发地+目的地，一键获取多方案对比
- 5种筛选维度：💰最便宜 / ⚡最快速 / 🔄最少换乘 / ⚖️性价比最高 / 🛋️最舒适
- 自动计算换乘方案，含等待时间和换乘指引

### 🏔️ 热门旅游线路
预置8条经典火车旅游线路，带沿途攻略：
- 🏔️ 青藏线 — 世界屋脊天路
- 🌊 沿海线 — 一路看海
- 🏜️ 丝路线 — 大漠孤烟
- 🌄 川藏线 — 最美进藏路
- 🍜 美食线 — 吃货天堂
- ❄️ 东北线 — 冰雪奇缘
- 🌿 桂林线 — 山水画卷
- 🌺 云南线 — 风花雪月

### 🎫 傻瓜式订票助手
- 票价图解（硬座/硬卧/软卧区别一看就懂）
- 换乘步骤详解（哪站换、等多久、怎么走）
- 方案适合人群标注（学生/家庭/商务）

### 📊 可视化界面
- 路线地图（交互式中国铁路网）
- 方案对比图表（价格/时间/换乘）
- 行程时间轴

## 🚀 快速开始

### 安装依赖

```bash
git clone https://github.com/Ana0ke/12306-train-planner.git
cd 12306-train-planner
pip install -r requirements.txt
```

### 启动应用

```bash
streamlit run app/main.py
```

浏览器自动打开 `http://localhost:8501`

### Docker 部署

```bash
docker build -t train-planner .
docker run -p 8501:8501 train-planner
```

## 📁 项目结构

```
12306省心小助手/
├── app/                      # Streamlit 前端
│   ├── main.py               # 入口页面
│   ├── pages/                # 多页面
│   │   ├── 1_🔍_路线规划.py
│   │   ├── 2_🏔️_热门线路.py
│   │   └── 3_🎫_订票助手.py
│   └── components/           # 可复用UI组件
│
├── core/                     # 核心业务逻辑
│   ├── planner.py            # 路线规划引擎
│   ├── filter.py             # 多维筛选器
│   ├── transfer.py           # 换乘计算
│   └── scorer.py             # 方案评分系统
│
├── api/                      # 数据获取层
│   ├── client_12306.py       # 12306查询接口
│   └── cache.py              # 查询缓存
│
├── data/                     # 数据文件
│   ├── routes/               # 热门线路数据
│   ├── stations.json         # 全国站点信息
│   └── city_guide.json       # 城市攻略数据
│
├── tests/                    # 单元测试
├── docs/                     # 项目文档
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🎯 目标用户

| 人群 | 核心需求 |
|------|----------|
| 🏔️ 火车旅行爱好者 | 路线风景、沿途体验、慢旅行攻略 |
| 🎫 怕麻烦的出行者 | 一键方案、不用自己查、省心省力 |

## 🛠️ 技术栈

| 用途 | 技术 |
|------|------|
| 前端 | Streamlit |
| 后端 | FastAPI |
| 地图 | folium |
| 图表 | plotly |
| 数据处理 | pandas |
| 缓存 | SQLite |
| 部署 | Docker |

## 📝 开发计划

- [x] 项目骨架搭建
- [ ] 12306查询接口封装
- [ ] 路线规划引擎（直达+换乘）
- [ ] 多维筛选器
- [ ] 热门线路数据（8条）
- [ ] 城市攻略卡片
- [ ] 路线地图可视化
- [ ] Docker部署

## 📜 License

MIT License

## 🤝 贡献

欢迎提 Issue 和 PR！

---

⭐ 如果这个项目对你有帮助，欢迎点个 Star！
