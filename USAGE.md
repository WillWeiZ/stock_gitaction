# 股票数据分析 Web 应用使用指南

## 📋 快速开始

### 1. 环境准备

```bash
# 克隆或下载项目代码
cd stock_gitaction

# 安装 Python 依赖
pip install -r requirements.txt
```

### 2. 配置 Supabase 连接

您需要有一个正在运行的 Supabase 项目，并且已经通过 `fetch_stock_data.py` 脚本获取了股票数据。

#### 方法一：使用环境变量 (推荐)

```bash
export SUPABASE_URL="https://your-project-id.supabase.co"
export SUPABASE_KEY="your-service-role-key"
```

#### 方法二：配置 secrets 文件

编辑 `.streamlit/secrets.toml` 文件：

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-service-role-key"
```

### 3. 获取 Supabase 配置信息

1. 登录 [Supabase.com](https://supabase.com)
2. 进入您的项目
3. 导航到 **Settings → API**
4. 复制以下信息：
   - **Project URL** (格式: https://xxxxx.supabase.co)
   - **service_role** 密钥 (⚠️ 不是 anon 密钥!)

### 4. 启动应用

```bash
# 方法一：使用启动脚本
./start_app.sh

# 方法二：使用 Python 启动脚本
python run_app.py

# 方法三：直接使用 Streamlit
streamlit run app.py
```

### 5. 访问应用

在浏览器中打开: http://localhost:8501

## 🎯 应用功能

### 主要特性

- **📅 日期选择**: 在侧边栏选择不同日期查看历史数据
- **📊 数据概览**: 顶部显示当日统计信息
- **📋 详细表格**: 完整的股票数据展示，支持排序
- **🎨 美观界面**: 响应式设计，适配各种屏幕

### 统计指标

- **符合条件股票数量**: 当天筛选出的股票总数
- **平均涨跌幅**: 所有股票的平均涨跌幅百分比
- **平均竞价涨幅**: 集合竞价阶段的平均涨幅
- **上涨股票占比**: 上涨股票数量占总数的比例

### 数据字段

表格显示以下股票信息：
- 股票代码和名称
- 最新价格和涨跌幅
- 竞价相关数据
- 市盈率和市值
- 量比和其他技术指标

## 🔧 故障排除

### 常见问题

#### 1. "Supabase 配置未找到"
- 检查环境变量是否设置正确
- 验证 `.streamlit/secrets.toml` 文件配置
- 确保配置值没有多余的空格或引号

#### 2. "Supabase 连接失败"
- 确认使用的是 **service_role** 密钥，不是 anon 密钥
- 检查项目 URL 格式是否正确
- 验证网络连接正常
- 确认 Supabase 项目处于活跃状态

#### 3. "暂无数据"
- 确认已经运行过 `fetch_stock_data.py` 脚本
- 检查 Supabase 中的 `stocks` 表是否存在数据
- 验证数据库表结构是否正确

#### 4. 数据显示异常
- 清除浏览器缓存
- 重启 Streamlit 应用
- 检查数据类型是否匹配

### 调试步骤

1. **测试数据库连接**:
   ```bash
   python demo.py
   ```

2. **检查日志**:
   启动应用时观察控制台输出的错误信息

3. **验证数据**:
   直接在 Supabase 控制台查询 `stocks` 表数据

## 📚 技术细节

### 依赖包
- `streamlit`: Web 应用框架
- `supabase`: Supabase Python 客户端
- `pandas`: 数据处理
- `datetime`: 日期时间处理

### 缓存机制
- 数据库连接缓存
- API 查询结果缓存 (5分钟)
- 提高应用响应速度

### 安全考虑
- 敏感配置通过环境变量或 secrets 文件管理
- `.gitignore` 排除 secrets 文件
- 使用 service_role 密钥进行数据库访问

## 🚀 生产部署

### Streamlit Cloud 部署

1. 将代码推送到 GitHub 仓库
2. 在 [Streamlit Cloud](https://streamlit.io/cloud) 创建应用
3. 在 Streamlit Cloud 中配置 secrets:
   ```toml
   SUPABASE_URL = "your-url"
   SUPABASE_KEY = "your-key"
   ```

### 本地生产运行

```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

## 📞 支持

如果遇到问题，请检查：
1. 所有依赖是否正确安装
2. Supabase 配置是否正确
3. 数据库中是否有数据
4. 网络连接是否正常

更多技术细节请参考项目中的 `CLAUDE.md` 文档。