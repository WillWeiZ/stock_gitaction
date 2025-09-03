#!/bin/bash

# 环境变量配置脚本示例
# 复制此文件并修改为您的实际配置

echo "🔧 设置 Supabase 环境变量..."

# 请将以下值替换为您的实际 Supabase 配置
export SUPABASE_URL="https://jsnrbuzrtvxuysotstyh.supabase.co"
export SUPABASE_KEY="your-supabase-service-role-key-here"

# 验证环境变量是否设置
if [ "$SUPABASE_KEY" = "your-supabase-service-role-key-here" ]; then
    echo "⚠️  请编辑此脚本，替换为您的实际 Supabase 配置！"
    echo ""
    echo "📋 获取配置步骤:"
    echo "1. 登录 https://supabase.com"
    echo "2. 进入您的项目"
    echo "3. 导航到 Settings → API"
    echo "4. 复制 Project URL 和 service_role key"
    echo ""
    exit 1
fi

echo "✅ 环境变量已设置"
echo "📊 SUPABASE_URL: $SUPABASE_URL"
echo "🔑 SUPABASE_KEY: ${SUPABASE_KEY:0:20}..."
echo ""
echo "🚀 现在可以运行应用:"
echo "  ./start_app.sh"