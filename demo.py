"""
股票数据分析应用演示脚本
用于测试 Supabase 连接和数据展示功能
"""

import os
from datetime import datetime
from supabase import create_client, Client

def test_supabase_connection():
    """测试 Supabase 连接"""
    print("🔌 测试 Supabase 连接...")
    
    # 从环境变量获取配置
    SUPABASE_URL = os.getenv("SUPABASE_URL", "https://jsnrbuzrtvxuysotstyh.supabase.co")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase 客户端创建成功")
        
        # 测试连接
        response = supabase.table('stocks').select('*').limit(1).execute()
        print("✅ 数据库连接成功")
        
        # 获取可用日期
        response = supabase.table('stocks').select('update_date').execute()
        dates = [row['update_date'] for row in response.data]
        unique_dates = sorted(list(set(dates)), reverse=True)
        
        print(f"📅 可用数据日期: {len(unique_dates)} 个")
        if unique_dates:
            print(f"   最新日期: {unique_dates[0]}")
            print(f"   最早日期: {unique_dates[-1]}")
            
            # 获取最新日期的数据统计
            latest_date = unique_dates[0]
            response = supabase.table('stocks').select('*').eq('update_date', latest_date).execute()
            stocks_data = response.data
            
            if stocks_data:
                print(f"\n📊 {latest_date} 数据统计:")
                print(f"   股票数量: {len(stocks_data)} 只")
                
                # 计算平均涨跌幅
                changes = [row.get('latest_change_pct', 0) for row in stocks_data if row.get('latest_change_pct') is not None]
                if changes:
                    avg_change = sum(changes) / len(changes)
                    print(f"   平均涨跌幅: {avg_change:.2f}%")
                
                # 显示前5只股票
                print(f"\n📋 前5只股票:")
                for i, stock in enumerate(stocks_data[:5]):
                    code = stock.get('code', 'N/A')
                    name = stock.get('stock_name', 'N/A')
                    price = stock.get('latest_price', 'N/A')
                    change = stock.get('latest_change_pct', 'N/A')
                    print(f"   {i+1}. {code} {name} {price} ({change}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

def main():
    """主函数"""
    print("🎯 股票数据分析应用演示")
    print("=" * 40)
    
    if test_supabase_connection():
        print("\n✅ 所有测试通过!")
        print("\n🚀 现在可以启动 Streamlit 应用:")
        print("   ./start_app.sh")
        print("   或")
        print("   streamlit run app.py")
    else:
        print("\n❌ 测试失败，请检查配置")
        print("   1. 确保 Supabase 配置正确")
        print("   2. 检查网络连接")
        print("   3. 验证 API 密钥权限")

if __name__ == "__main__":
    main()