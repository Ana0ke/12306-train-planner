# 12306实时查询说明

本项目支持内嵌12306实时查询，无需外部MCP服务。

## 目录

- [功能说明](#功能说明)
- [配置方式](#配置方式)
- [查询逻辑](#查询逻辑)
- [数据格式](#数据格式)
- [常见问题](#常见问题)

## 功能说明

启用实时查询后，项目将直接请求12306接口获取真实数据：

| 功能 | 说明 |
|------|------|
| 🔍 余票查询 | 直接从12306获取实时余票信息 |
| 🚉 车站代码 | 内置300+常用车站代码映射 |
| 🚄 中转方案 | 支持换乘方案查询 |

**查询策略**：
1. `USE_REALTIME=true` → 实时查询
2. `DEMO_MODE=true` → 模拟数据（默认）

## 配置方式

### 环境变量配置

在项目根目录创建 `.env` 文件：

```env
# 启用实时查询（默认关闭）
USE_REALTIME=true

# 备用：Demo模式开关
DEMO_MODE=false
```

### Streamlit Cloud 部署

在 **Settings → Secrets** 中添加：

```toml
# .streamlit/secrets.toml
USE_REALTIME = "true"
```

## 查询逻辑

### 1. 会话初始化
```
访问 https://kyfw.12306.cn/otn/leftTicket/init
获取JSESSIONID等Cookie
```

### 2. 余票查询
```
GET https://kyfw.12306.cn/otn/leftTicket/queryG
参数:
  - leftTicketDTO.train_date: 日期 (YYYY-MM-DD)
  - leftTicketDTO.from_station: 出发站三字码
  - leftTicketDTO.to_station: 到达站三字码
  - purpose_codes: ADULT
```

### 3. 中转查询
```
GET https://kyfw.12306.cn/lcquery/queryG
参数:
  - from_station_telecode: 出发站三字码
  - to_station_telecode: 到达站三字码
  - train_date: 日期
```

## 数据格式

### 余票响应示例
```json
{
  "train_no": "G1234",
  "train_code": "G1234",
  "from_station": "长沙南",
  "to_station": "广州南",
  "depart_time": "08:00",
  "arrive_time": "10:30",
  "duration": "02:30",
  "train_type": "高铁",
  "remaining": {
    "商务座": "有",
    "一等座": "5",
    "二等座": "10"
  },
  "prices": {
    "商务座": 999.0,
    "一等座": 499.0,
    "二等座": 314.5
  },
  "is_realtime": true
}
```

### 车站代码格式
```json
{
  "长沙南": "CWQ",
  "广州南": "IZQ",
  "深圳北": "IOQ"
}
```

文件位置：`data/station_codes.json`

## 防反爬机制

项目内置以下保护措施：

1. **请求限流**：最小1.5秒间隔
2. **Cookie管理**：自动获取并维持会话
3. **User-Agent**：使用真实浏览器标识
4. **Fallback机制**：查询失败自动切换到Demo模式

## 常见问题

### Q: 启用实时查询后查询失败？

**可能原因**：
1. 12306服务器维护 → 稍后重试
2. 触发反爬 → 自动降级到Demo模式
3. 网络问题 → 检查网络连接

**解决方案**：
```bash
# 临时禁用实时查询
USE_REALTIME=false
```

### Q: 如何验证实时查询是否工作？

**检查方法**：
1. 启动应用后查看日志
2. 查询结果显示"🟢 12306实时"标记
3. 票价与12306官网一致

### Q: Streamlit Cloud上能用吗？

**可以**，但需要注意：
- 默认使用Demo模式（安全）
- 如需实时查询，确保 `USE_REALTIME=true`
- 12306可能对Cloud IP有限制

### Q: 数据准确性如何？

- **余票信息**：实时同步12306
- **票价信息**：参考值，实际票价以购票时为准
- **时刻表**：按12306官方时刻运行

## 项目地址

- **12306省心小助手**: https://github.com/Ana0ke/12306-train-planner
- **12306官网**: https://www.12306.cn

## 免责声明

1. 本项目仅供学习交流使用
2. 请遵守12306使用条款，合理使用查询接口
3. 请勿高频请求或用于商业目的
4. 数据仅供参考，实际票价和余票请以12306官方为准
