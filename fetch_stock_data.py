import pywencai
import pandas as pd
import os
import sys
from datetime import datetime
import requests
import json
from supabase import create_client, Client

# 钉钉机器人配置（可选）
DINGTALK_WEBHOOK = os.getenv('DINGTALK_WEBHOOK', '')

# 同花顺Cookie配置
COOKIE = os.getenv('THS_COOKIE', '')

# Supabase配置
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')

# 初始化Supabase客户端
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def dingtalk_robot(message):
    """发送钉钉通知"""
    if not DINGTALK_WEBHOOK:
        print("钉钉Webhook未配置，跳过通知")
        return
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    
    try:
        response = requests.post(DINGTALK_WEBHOOK, headers=headers, json=data)
        response.raise_for_status()
        print("✅ 钉钉通知发送成功")
    except Exception as e:
        print(f"❌ 钉钉通知发送失败: {e}")

def clean_stock_code(code):
    """清理股票代码，去除 .SH, .SZ 等后缀"""
    if isinstance(code, str):
        return code.replace('.SH', '').replace('.SZ', '').replace('.BJ', '')
    return str(code)

def init_database():
    """初始化数据库表结构 - Supabase版本"""
    if not supabase:
        print("❌ Supabase 客户端未初始化")
        return False
    
    # 在Supabase中，表结构需要在Web界面或通过SQL创建
    # 这里只是检查连接
    try:
        # 测试连接
        result = supabase.table('stocks').select('*').limit(1).execute()
        print("✅ Supabase 数据库连接成功")
        return True
    except Exception as e:
        print(f"❌ Supabase 数据库连接失败: {e}")
        return False

def insert_stock_data(df, update_date):
    """插入股票数据到Supabase数据库"""
    if not supabase:
        print("❌ Supabase 客户端未初始化")
        return 0
    
    try:
        # 清理和映射数据列
        data_to_insert = []
        
        for _, row in df.iterrows():
            # 获取股票代码
            stock_code = None
            for col in ['代码', '股票代码', '证券代码', 'code']:
                if col in df.columns and pd.notna(row[col]):
                    stock_code = clean_stock_code(str(row[col]))
                    break
            
            if not stock_code:
                continue
                
            try:
                stock_code = int(stock_code)
            except:
                continue
            
            # 获取股票名称
            stock_name = ""
            for col in ['股票简称', '证券简称', 'name']:
                if col in df.columns and pd.notna(row[col]):
                    stock_name = str(row[col])
                    break
            
            if not stock_name:
                continue
            
            # 映射其他字段 - 使用模糊匹配来处理包含日期的字段名
            data_row = {
                'code': stock_code,
                'stock_name': stock_name,
                'latest_price': get_value(row, df.columns, ['最新价', '现价', 'price']),
                'latest_change_pct': get_value(row, df.columns, ['最新涨跌幅', '涨跌幅', '涨跌幅(%)']),
                'listing_board': get_value(row, df.columns, ['上市板块', '板块']),
                'auction_change_pct': get_value_fuzzy(row, df.columns, ['竞价涨幅']),
                'pe_ttm': get_value_fuzzy(row, df.columns, ['市盈率(pe,ttm)']),
                'pe': get_value_fuzzy(row, df.columns, ['市盈率(pe)']),
                'dde_large_order': get_value_fuzzy(row, df.columns, ['dde大单净量']),
                'volume_ratio': get_value_fuzzy(row, df.columns, ['分时量比']),
                'interval_change_13d': get_interval_change(row, df.columns, longer=True),   # 取较长区间
                'interval_change_5d': get_interval_change(row, df.columns, longer=False),  # 取较短区间
                'listing_days': get_value_fuzzy(row, df.columns, ['上市天数']),
                'forecast_pe_1y': get_value_fuzzy(row, df.columns, ['预测市盈率(pe,最新预测)[2025']),
                'forecast_pe_2y': get_value_fuzzy(row, df.columns, ['预测市盈率(pe,最新预测)[2026']),
                'forecast_pe_3y': get_value_fuzzy(row, df.columns, ['预测市盈率(pe,最新预测)[2027']),
                'market_cap': get_value_fuzzy(row, df.columns, ['总市值']),
                'eps': get_value(row, df.columns, ['基本每股收益', 'EPS']),
                'gross_margin': get_value(row, df.columns, ['销售毛利率', '毛利率']),
                'net_margin': get_value(row, df.columns, ['销售净利率', '净利率']),
                'auction_price': get_value_fuzzy(row, df.columns, ['竞价匹配价']),
                'auction_type': get_value_fuzzy(row, df.columns, ['竞价异动类型']),
                'auction_desc': get_value_fuzzy(row, df.columns, ['竞价异动说明']),
                'auction_rating': get_value_fuzzy(row, df.columns, ['集合竞价评级']),
                'auction_volume': get_value_fuzzy(row, df.columns, ['竞价量']),
                'auction_amount': get_value(row, df.columns, ['竞价金额', '竞价成交额']),
                'market_code': get_value(row, df.columns, ['market_code']),
                'update_date': update_date
            }
            
            data_to_insert.append(data_row)
        
        if data_to_insert:
            # 先删除当天的数据，避免重复
            try:
                supabase.table('stocks').delete().eq('update_date', update_date).execute()
                print(f"🗑️ 已清理当天的旧数据")
            except Exception as e:
                print(f"⚠️ 清理旧数据时出现警告: {e}")
            
            # 批量插入数据到Supabase
            result = supabase.table('stocks').insert(data_to_insert).execute()
            
            print(f"✅ 成功插入 {len(data_to_insert)} 条股票数据到Supabase数据库")
            return len(data_to_insert)
        else:
            print("❌ 没有有效的数据可插入")
            return 0
            
    except Exception as e:
        print(f"❌ 插入数据到Supabase数据库时出错: {e}")
        return 0

def get_value(row, columns, possible_names, default=None):
    """从行数据中获取值"""
    for name in possible_names:
        if name in columns and pd.notna(row[name]):
            return row[name]
    return default

def get_value_fuzzy(row, columns, possible_names, default=None):
    """使用模糊匹配从行数据中获取值"""
    for pattern in possible_names:
        for col in columns:
            if pattern in col and pd.notna(row[col]):
                return row[col]
    return default

def get_interval_change(row, columns, longer=True, default=None):
    """获取区间涨跌幅，longer=True取较长区间，False取较短区间"""
    interval_cols = [col for col in columns if '区间涨跌幅:前复权' in col]
    if not interval_cols:
        return default
    
    if longer:
        # 取较长区间（日期范围较大的）
        col = max(interval_cols, key=len, default=None)
    else:
        # 取较短区间（日期范围较小的）  
        col = min(interval_cols, key=len, default=None)
    
    if col and pd.notna(row[col]):
        return row[col]
    return default

def fetch_stock_data():
    """获取股票数据"""
    try:
        print("🔄 开始从同花顺获取股票数据...")
        
        # 同花顺查询条件
        query = '''今天非st，非科创板，竞价涨跌幅大于1%且小于6%，
                   TTM 市盈率不为亏损，主力净量大于0，集合竞价量比大于1，
                   10日涨幅大于等于10%，5日涨幅大于等于10%，上市时间大于100天'''
        
        # 获取数据
        res = pywencai.get(query=query, cookie=COOKIE)
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        if res is not None:
            # 确保数据是DataFrame格式
            if not isinstance(res, pd.DataFrame):
                res = pd.DataFrame(res)
            
            print(f"📊 获取到 {len(res)} 条股票数据")
            
            # 清理股票代码
            for col in ['代码', '股票代码', '证券代码']:
                if col in res.columns:
                    res[col] = res[col].astype(str).str.replace(r'\.(SH|SZ|BJ)', '', regex=True)
            
            # 保存到Excel文件（可选）
            excel_path = os.path.join(os.path.dirname(__file__), f'stock_data_{current_date}.xlsx')
            res.to_excel(excel_path, index=False)
            print(f"📄 数据已保存到Excel: {excel_path}")
            
            # 插入数据库
            data_count = insert_stock_data(res, current_date)
            
            # 准备钉钉通知消息
            message = f"📊 **股票数据更新通知** ({current_date})\n\n"
            message += f"📈 **符合条件股票数量**: {data_count} 只\n\n"
            
            if data_count > 0:
                message += f"📋 **部分股票列表**:\n"
                
                # 显示前10只股票
                display_count = min(10, len(res))
                for i in range(display_count):
                    row = res.iloc[i]
                    
                    # 获取股票基本信息
                    stock_code = ""
                    if '代码' in res.columns:
                        stock_code = str(row['代码'])
                    elif '股票代码' in res.columns:
                        stock_code = str(row['股票代码'])
                    
                    stock_name = ""
                    if '股票简称' in res.columns:
                        stock_name = str(row['股票简称'])
                    
                    # 获取竞价涨幅
                    price_change = ""
                    for col in ['竞价涨跌幅', '涨跌幅', '最新涨跌幅']:
                        if col in res.columns and pd.notna(row[col]):
                            if isinstance(row[col], (int, float)):
                                price_change = f"{row[col]:.2f}%"
                            break
                    
                    message += f"{i+1}. {stock_code} {stock_name} {price_change}\n"
                
                if len(res) > 10:
                    message += f"... 还有 {len(res) - 10} 只股票\n"
            else:
                message += f"📝 **提示**: 今日无符合条件的股票\n"
            
            message += f"\n💾 **数据已更新到数据库**"
            
            # 发送钉钉通知
            try:
                dingtalk_robot(message)
            except Exception as e:
                print(f"❌ 钉钉通知发送失败: {e}")
            
            return True, data_count
            
        else:
            print("❌ 未获取到数据")
            
            # 发送无数据通知
            message = f"📊 **股票数据更新通知** ({current_date})\n\n"
            message += f"📈 **符合条件股票数量**: 0 只\n\n"
            message += f"📝 **提示**: 今日无符合条件的股票"
            
            try:
                dingtalk_robot(message)
            except Exception as e:
                print(f"❌ 钉钉通知发送失败: {e}")
            
            return False, 0
    
    except Exception as e:
        print(f"❌ 获取股票数据时出错: {e}")
        
        # 发送错误通知
        error_message = f"❌ **股票数据获取失败**\n\n"
        error_message += f"🕒 **时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        error_message += f"💻 **错误信息**: {str(e)}"
        
        try:
            dingtalk_robot(error_message)
        except:
            pass
        
        return False, 0

def main():
    """主函数"""
    print("🚀 启动股票数据获取脚本...")
    print(f"📅 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查必要的环境变量
    if not COOKIE:
        print("❌ 未设置 THS_COOKIE 环境变量")
        return False
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ 未设置 Supabase 配置环境变量")
        return False
    
    # 初始化数据库连接
    if not init_database():
        print("❌ 数据库初始化失败")
        return False
    
    # 获取股票数据
    success, count = fetch_stock_data()
    
    if success:
        print(f"✅ 任务完成！共处理 {count} 条股票数据")
    else:
        print("❌ 任务失败")
    
    return success

if __name__ == "__main__":
    main()