# 🚀 快速开始指南

## 问题解决

如果您遇到了 `StreamlitSecretNotFoundError: Unbalanced quotes` 错误，这是因为 secrets.toml 文件中的 JWT token 包含特殊字符导致解析失败。

## 解决方案

### 方法一：使用环境变量 (推荐)

```bash
# 1. 设置环境变量
export SUPABASE_URL="https://your-project-id.supabase.co"
export SUPABASE_KEY="your-service-role-key-here"

# 2. 启动应用
./start_app.sh
```

### 方法二：使用配置脚本

```bash
# 1. 复制配置脚本
cp setup_env.sh my_config.sh

# 2. 编辑配置脚本，填入您的实际配置
nano my_config.sh

# 3. 运行配置脚本
source my_config.sh

# 4. 启动应用
./start_app.sh
```

### 方法三：修复 secrets.toml 文件

如果您坚持使用 secrets.toml，请确保：

1. JWT token 使用双引号包围
2. 没有换行符在 token 中间
3. 文件编码为 UTF-8

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.very-long-jwt-token-here"
```

## 获取正确的 Supabase 配置

1. 登录 [Supabase.com](https://supabase.com)
2. 选择您的项目
3. 进入 **Settings** → **API**
4. 复制以下信息：
   - **Project URL**: `https://xxxxx.supabase.co`
   - **service_role key**: 长的 JWT token (不是 anon key!)

## 验证配置

运行测试脚本验证配置：

```bash
python demo.py
```

如果看到以下输出，说明配置成功：
```
✅ Supabase 客户端创建成功
✅ 数据库连接成功
📅 可用数据日期: X 个
```

## 启动应用

```bash
# 使用启动脚本
./start_app.sh

# 或直接使用 streamlit
streamlit run app.py
```

然后在浏览器中访问：http://localhost:8501

## 常见问题

1. **端口占用**: 如果 8501 端口被占用，修改启动脚本中的端口号
2. **依赖缺失**: 运行 `pip install -r requirements.txt`
3. **数据为空**: 确保先运行 `fetch_stock_data.py` 获取数据
4. **权限错误**: 确保使用 `service_role` key，不是 `anon` key

## 成功标志

当您看到应用正常启动并显示股票数据时，说明一切配置正确！🎉