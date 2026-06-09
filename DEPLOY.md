# 🚀 部署指南

## 方案一：Streamlit Cloud（推荐 ⭐，免费5分钟上线）

### 步骤

1. **Fork 或 Clone 本仓库到你的 GitHub 账号**

2. **前往 [Streamlit Cloud](https://streamlit.io/cloud)**
   - 用 GitHub 账号登录
   - 点击 "New app"
   - 选择仓库：`你的用户名/12306-train-planner`
   - 分支：`main`
   - 主文件路径：`app/main.py`
   - 点击 "Deploy!"

3. **配置 Secrets（可选，启用AI功能）**
   - 在 App Settings → Secrets 中添加：
   ```toml
   LLM_API_KEY = "你的DeepSeek API Key"
   LLM_BASE_URL = "https://api.deepseek.com"
   LLM_MODEL = "deepseek-chat"
   DEMO_MODE = "true"
   ```

4. **访问你的应用**
   - 部署完成后会得到一个 `xxx.streamlit.app` 的链接
   - 分享给朋友就能直接使用！

### 注意事项
- Streamlit Cloud 免费版限制：1GB 内存、1 CPU
- 不配置 LLM_API_KEY 也能使用基础功能（路线查询、热门线路、Demo预览）
- 每次推送到 main 分支会自动重新部署

---

## 方案二：HuggingFace Spaces

1. **创建 Space**
   - 前往 https://huggingface.co/new-space
   - SDK 选择 `Streamlit`
   - 命名你的 Space

2. **上传代码**
   ```bash
   git clone https://huggingface.co/spaces/你的用户名/你的space名
   cd 你的space名
   # 复制项目文件到此处
   git add .
   git commit -m "init"
   git push
   ```

3. **配置环境变量**
   - 在 Space Settings → Repository secrets 中添加 `LLM_API_KEY` 等

---

## 方案三：Docker 自托管

```bash
# 构建镜像
docker build -t 12306-train-planner .

# 运行容器
docker run -d \
  -p 8501:8501 \
  -e LLM_API_KEY=你的key \
  -e LLM_BASE_URL=https://api.deepseek.com \
  -e LLM_MODEL=deepseek-chat \
  --name train-planner \
  12306-train-planner
```

访问 `http://你的服务器IP:8501`

---

## 方案四：VPS / 云服务器部署

```bash
# 1. 安装依赖
git clone https://github.com/Ana0ke/12306-train-planner.git
cd 12306-train-planner
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 API Key

# 3. 使用 systemd 守护进程
sudo tee /etc/systemd/system/train-planner.service << 'EOF'
[Unit]
Description=12306 Train Planner
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/12306-train-planner
ExecStart=/usr/local/bin/streamlit run app/main.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable train-planner
sudo systemctl start train-planner
```

---

## 🔒 安全提醒

- ⚠️ **永远不要**将 `.env` 或 `secrets.toml` 提交到代码仓库
- API Key 通过 Streamlit Cloud Secrets 或环境变量注入
- `.gitignore` 已配置忽略敏感文件
- 建议为不同环境使用不同的 API Key

---

## 📊 性能优化

| 优化项 | 方法 |
|--------|------|
| 缓存 | Streamlit `@st.cache_data` 缓存查询结果 |
| 并发 | 使用 `@st.cache_resource` 复用 LLM 客户端 |
| 降级 | LLM 不可用时自动回退到静态数据方案 |
| Demo模式 | 设 `DEMO_MODE=true` 不依赖外部接口即可运行 |
