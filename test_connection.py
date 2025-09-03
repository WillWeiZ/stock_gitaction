#!/usr/bin/env python3
"""
快速测试 Supabase 连接
使用您提供的配置信息
"""

import os
from supabase import create_client

def test_connection():
    """测试 Supabase 连接"""
    print("🔌 测试 Supabase 连接...")
    
    # 使用您提供的配置
    SUPABASE_URL = "https://jsnrbuzrtvxuysotstyh.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpzbnJidXpydHZ4dXlzb3RzdHloIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njg3NDYwMiwiZXhwIjoyMDcyNDUwNjAyfQ.qv7P5VfYFX0pZPfs7QVcVwlxIgbU3APVdEAKM2QBCV0"
    
    try:
        # 创建客户端
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase 客户端创建成功")
        
        # 测试数据库连接
        response = supabase.table('stocks').select('update_date').limit(1).execute()
        print("✅ 数据库连接成功")
        
        # 获取数据统计
        response = supabase.table('stocks').select('*').execute()
        total_records = len(response.data)
        print(f"📊 数据库中共有 {total_records} 条股票记录")
        
        if total_records > 0:
            # 获取可用日期
            dates = list(set([row['update_date'] for row in response.data]))
            dates.sort(reverse=True)
            print(f"📅 可用数据日期 ({len(dates)} 个):")
            for date in dates[:5]:  # 只显示前5个
                count = len([r for r in response.data if r['update_date'] == date])
                print(f"   - {date}: {count} 条记录")
            
            if len(dates) > 5:
                print(f"   ... 还有 {len(dates) - 5} 个日期")
        
        print("\n🎉 配置正确！现在可以启动 Streamlit 应用了:")
        print("   ./start_app.sh")
        return True
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("\n🔧 建议检查:")
        print("   1. 网络连接是否正常")
        print("   2. API 密钥是否有效")
        print("   3. 数据库中是否已有 stocks 表")
        return False

if __name__ == "__main__":
    test_connection()