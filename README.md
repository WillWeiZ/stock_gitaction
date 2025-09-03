# 股票数据获取自动化脚本

这是一个使用 GitHub Actions 定时获取股票数据并存储到 Supabase 数据库的自动化脚本。

## 功能特性

- 🔄 **定时自动执行**: 使用 GitHub Actions 在工作日上午自动运行
- 📊 **数据获取**: 从同花顺获取符合特定条件的股票数据
- 🗄️ **云端存储**: 将数据存储到 Supabase PostgreSQL 数据库
- 📱 **钉钉通知**: 自动发送执行结果通知到钉钉群

## 部署步骤

### 1. 创建 Supabase 项目

1. 访问 [Supabase.com](https://supabase.com)
2. 创建新项目
3. 在 SQL Editor 中执行 `supabase_setup.sql` 文件创建数据表
4. 获取项目的 URL 和 API Key (service_role key)

### 2. 配置 GitHub Secrets

在 GitHub 仓库的 Settings > Secrets and variables > Actions 中添加以下环境变量：

| 变量名 | 描述 | 示例 | 必需 |
|--------|------|------|------|
| `SUPABASE_URL` | Supabase 项目 URL | `https://xxx.supabase.co` | ✅ |
| `SUPABASE_KEY` | Supabase API 密钥 | `eyJhbGci...` | ✅ |
| `THS_COOKIE` | 同花顺网站 Cookie | `other_uid=...` | ✅ |
| `DINGTALK_WEBHOOK` | 钉钉机器人 Webhook | `https://oapi.dingtalk.com/...` | ❌ |

### 3. 获取同花顺 Cookie

1. 打开同花顺问财网站 (iwencai.com)
2. 登录账户
3. 打开浏览器开发者工具 (F12)
4. 在网络请求中找到包含完整 Cookie 的请求
5. 复制完整的 Cookie 字符串到 `THS_COOKIE`

### 4. 设置钉钉通知 (可选)

1. 在钉钉群中添加自定义机器人
2. 获取 Webhook 地址
3. 将地址配置到 `DINGTALK_WEBHOOK`

## 工作流程说明

### 触发条件
- **定时触发**: 每个工作日上午9:00 (北京时间)
- **手动触发**: 在 Actions 页面可以手动运行

### 筛选条件
脚本会获取符合以下条件的股票：
- 非ST股票
- 非科创板
- 竞价涨跌幅在1%-6%之间
- TTM市盈率不为亏损
- 主力净量大于0
- 集合竞价量比大于1
- 10日涨幅≥10%
- 5日涨幅≥10%
- 上市时间>100天

### 数据字段
主要包含以下数据字段：
- 基础信息：股票代码、股票名称、上市板块
- 价格信息：最新价、涨跌幅、竞价涨幅
- 财务指标：市盈率、每股收益、毛利率、净利率
- 交易指标：主力净量、量比、区间涨跌幅
- 预测数据：1-3年预测市盈率

## 文件说明

| 文件 | 描述 |
|------|------|
| `fetch_stock_data.py` | 主要的数据获取脚本 |
| `app.py` | Streamlit Web 应用主文件 |
| `run_app.py` | Streamlit 应用启动脚本 |
| `.github/workflows/stock-data.yml` | GitHub Actions 工作流配置 |
| `requirements.txt` | Python 依赖包列表 |
| `supabase_setup.sql` | Supabase 数据库表结构创建脚本 |
| `.streamlit/config.toml` | Streamlit 应用配置 |
| `README.md` | 项目说明文档 |

## 本地使用

### 数据获取脚本
```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export SUPABASE_URL="your-supabase-url"
export SUPABASE_KEY="your-supabase-key"
export THS_COOKIE="your-ths-cookie"
export DINGTALK_WEBHOOK="your-dingtalk-webhook"  # 可选

# 运行数据获取脚本
python fetch_stock_data.py
```

### Streamlit Web 应用
```bash
# 1. 配置 Supabase 连接
# 编辑 .streamlit/secrets.toml 文件，填入你的 Supabase 配置

# 2. 启动 Web 应用
python run_app.py
# 或直接使用 streamlit 命令
streamlit run app.py

# 3. 打开浏览器访问 http://localhost:8501
```

### Web 应用功能
- 📅 **日期选择**: 选择不同日期查看历史数据
- 📊 **汇总统计**: 显示当天符合条件的股票数量、平均涨跌幅等
- 📋 **数据表格**: 详细的股票信息展示，支持排序
- 🎨 **美观界面**: 响应式设计，支持多列布局

## 注意事项

1. **Cookie 有效期**: 同花顺 Cookie 可能会过期，需要定期更新
2. **请求频率**: 避免过于频繁的请求，以免被限制访问
3. **数据准确性**: 脚本仅用于数据收集，不构成投资建议
4. **成本控制**: Supabase 免费额度有限，注意使用量

## 故障排除

### 常见问题

1. **Cookie 过期**: 重新获取并更新 `THS_COOKIE`
2. **Supabase 连接失败**: 检查 URL 和 API Key 是否正确
3. **无数据**: 可能是筛选条件过于严格，当日无符合条件的股票

### 查看日志

在 GitHub Actions 的运行记录中可以查看详细的执行日志和错误信息。

## 许可证

本项目仅供学习和研究使用，请遵守相关网站的使用条款。