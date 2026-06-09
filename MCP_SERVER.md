# 12306 MCP 服务部署指南

本项目支持通过 `mcp-server-12306` (by drfccv) 接入真实12306数据查询。

## 目录

- [功能说明](#功能说明)
- [快速开始](#快速开始)
- [部署方式](#部署方式)
- [配置项目](#配置项目)
- [常见问题](#常见问题)

## 功能说明

启用MCP服务后，项目将使用真实12306数据进行查询：

| 功能 | 说明 |
|------|------|
| 🔍 余票查询 | 实时查询12306余票信息 |
| 🚉 车站搜索 | 支持中文、拼音、简拼搜索 |
| 🚄 中转方案 | 查询换乘方案 |

**查询策略**：
1. MCP模式 → 真实数据
2. Demo模式 → 模拟数据（默认）

## 快速开始

### 1. 安装依赖

```bash
# 安装 MCP 服务
pip install mcp-server-12306
```

### 2. 启动服务

```bash
# 启动 MCP 服务（默认端口 8000）
mcp-server-12306

# 或指定端口
mcp-server-12306 --port 8080
```

### 3. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 预期返回: {"status": "ok"}
```

### 4. 配置项目

```bash
# 设置环境变量
export MCP_SERVER_URL=http://localhost:8000

# 或在 .env 文件中添加
echo "MCP_SERVER_URL=http://localhost:8000" >> .env
```

### 5. 启动项目

```bash
streamlit run app/main.py
```

## 部署方式

### 方式一：pip 安装（推荐）

```bash
# 安装
pip install mcp-server-12306

# 启动
mcp-server-12306

# 后台运行
nohup mcp-server-12306 > mcp.log 2>&1 &
```

### 方式二：Docker 部署

```bash
# 构建镜像
docker build -t 12306-mcp .

# 运行容器
docker run -d -p 8000:8000 --name 12306-mcp 12306-mcp

# 查看日志
docker logs -f 12306-mcp
```

Dockerfile 示例：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装依赖
RUN pip install --no-cache-dir mcp-server-12306

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["mcp-server-12306", "--host", "0.0.0.0"]
```

### 方式三：Docker Compose 部署

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  mcp-server:
    image: 12306-mcp  # 或使用公网镜像
    container_name: 12306-mcp
    ports:
      - "8000:8000"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  12306-assistant:
    image: your-12306-assistant-image
    container_name: 12306-assistant
    ports:
      - "8501:8501"
    environment:
      - MCP_SERVER_URL=http://mcp-server:8000
    depends_on:
      - mcp-server
    restart: unless-stopped
```

启动：

```bash
docker-compose up -d
```

## 配置项目

### 本地开发配置

1. **环境变量方式**

```bash
export MCP_SERVER_URL=http://localhost:8000
```

2. **.env 文件方式**

在项目根目录创建 `.env` 文件：

```env
# MCP 服务地址
MCP_SERVER_URL=http://localhost:8000

# 其他配置
DEMO_MODE=false
```

3. **直接修改代码**

在 `api/client_12306.py` 中，MCP客户端会自动从环境变量读取 `MCP_SERVER_URL`。

### Streamlit Cloud 部署

在 Streamlit Cloud 的 **Settings → Secrets** 中添加：

```toml
# .streamlit/secrets.toml
MCP_SERVER_URL = "https://your-mcp-service.example.com"
```

**注意**：Streamlit Cloud 无法访问本地服务，需要将 MCP 服务部署到公网可访问的服务器。

### 远程 MCP 服务示例

如果你有公网服务器，可以按以下方式部署：

```bash
# 在服务器上安装并启动
ssh your-server
pip install mcp-server-12306
nohup mcp-server-12306 --host 0.0.0.0 --port 8000 > mcp.log 2>&1 &

# 配置 HTTPS（推荐使用 Nginx 反向代理）
# 添加域名解析 your-mcp.example.com -> 服务器IP

# 在 Streamlit Cloud Secrets 中配置
MCP_SERVER_URL = "https://your-mcp.example.com"
```

## API 接口说明

MCP 服务提供以下 REST API：

### 健康检查

```
GET /health
```

返回：
```json
{"status": "ok"}
```

### 搜索车站

```
GET /search_stations?keyword=北京南
```

返回：
```json
[
  {
    "name": "北京南",
    "code": "VNP",
    "pinyin": "beijingnan",
    "spell": "BJN"
  }
]
```

### 查询余票

```
GET /query_tickets?from=VNP&to=AOH&date=2025-07-17
```

返回：
```json
{
  "tickets": [
    {
      "train_code": "G1",
      "from_station": "北京南",
      "to_station": "上海虹桥",
      "depart_time": "09:00",
      "arrive_time": "13:28",
      "duration": "04:28",
      "prices": {
        "二等座": 553,
        "一等座": 933,
        "商务座": 1748
      },
      "remaining": {
        "二等座": "有",
        "一等座": "5"
      }
    }
  ]
}
```

### 查询中转

```
GET /query_transfer?from=起点&to=终点&date=2025-07-17
```

### 查询经停站

```
GET /get_train_route_stations?trainCode=G101&departDate=2025-07-17
```

## 常见问题

### Q: MCP 服务启动失败？

**A**: 检查端口占用和依赖安装：

```bash
# 检查端口
lsof -i :8000

# 重新安装依赖
pip uninstall mcp-server-12306 -y
pip install mcp-server-12306
```

### Q: 查询返回空？

**A**: 可能原因：
1. MCP服务未启动 → 重启服务
2. 日期超出12306预售期 → 调整查询日期
3. 站点代码错误 → 使用 `/search_stations` 验证

### Q: 如何调试 MCP 请求？

**A**: 在代码中添加日志或使用 curl：

```bash
# 查看实时日志
tail -f mcp.log

# 手动测试请求
curl "http://localhost:8000/search_stations?keyword=上海"
curl "http://localhost:8000/query_tickets?from=SHH&to=AOH&date=2025-07-17"
```

### Q: MCP 和 Demo 模式如何切换？

**A**: 
- 只设置 `MCP_SERVER_URL` → 优先MCP，失败fallback Demo
- 只设置 `DEMO_MODE=false` → 使用12306官方API（有反爬风险）
- 都不设置 → Demo模式

### Q: Streamlit Cloud 如何使用 MCP？

**A**: 需要将 MCP 服务部署到公网：
1. 在云服务器上部署 `mcp-server-12306`
2. 配置 HTTPS 域名
3. 在 Streamlit Cloud Secrets 中配置 `MCP_SERVER_URL`

## 项目地址

- **MCP Server**: https://github.com/drfccv/mcp-server-12306
- **12306省心小助手**: https://github.com/Ana0ke/12306-train-planner

## 免责声明

1. 本项目仅供学习交流使用
2. 请遵守12306使用条款，合理使用查询接口
3. 请勿高频请求或用于商业目的
4. 数据仅供参考，实际票价和余票请以12306官方为准
