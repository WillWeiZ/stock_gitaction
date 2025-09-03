#!/bin/bash

# 股票数据分析 Streamlit 应用启动脚本

echo "🚀 启动股票数据分析面板..."
echo "📊 检查 Supabase 配置..."
echo ""

# 检查环境变量配置
if [ -z "$SUPABASE_URL" ] && [ -z "$SUPABASE_KEY" ]; then
    echo "⚠️  未检测到环境变量配置"
    echo "请设置以下环境变量:"
    echo "  export SUPABASE_URL='https://jsnrbuzrtvxuysotstyh.supabase.co‘"
    echo "  export SUPABASE_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpzbnJidXpydHZ4dXlzb3RzdHloIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njg3NDYwMiwiZXhwIjoyMDcyNDUwNjAyfQ.qv7P5VfYFX0pZPfs7QVcVwlxIgbU3APVdEAKM2QBCV0'"
    echo ""
    echo "或者配置 .streamlit/secrets.toml 文件"
    echo ""
fi

# 检查 Python 依赖
python -c "import streamlit, supabase" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少必要的 Python 依赖"
    echo "请运行: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Python 依赖检查通过"
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