#!/bin/bash

# 股票数据分析 Streamlit 应用启动脚本

echo "🚀 启动股票数据分析面板..."
echo "📊 确保您的 Supabase 配置正确..."
echo ""

# 检查必要的文件
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "❌ 未找到 .streamlit/secrets.toml 配置文件"
    echo "请确保正确配置了 Supabase 连接信息"
    exit 1
fi

# 检查 Python 依赖
python -c "import streamlit, supabase" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少必要的 Python 依赖"
    echo "请运行: pip install -r requirements.txt"
    exit 1
fi

echo "✅ 环境检查通过"
echo "🌐 启动 Web 应用..."
echo ""
echo "📱 访问地址: http://localhost:8501"
echo "⏹️  按 Ctrl+C 停止应用"
echo ""

# 启动 Streamlit 应用
streamlit run app.py \
    --server.port=8501 \
    --server.address=localhost \
    --browser.gatherUsageStats=false \
    --theme.primaryColor="#1f77b4" \
    --theme.backgroundColor="#ffffff"