import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from supabase import create_client, Client
import os

# 页面配置
st.set_page_config(
    page_title="股票数据分析面板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 样式配置
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .positive {
        color: #28a745;
    }
    .negative {
        color: #dc3545;
    }
    .stock-table {
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_supabase():
    """初始化 Supabase 连接"""
    SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY"))
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("❌ Supabase 配置未找到")
        st.info("""
        请按以下步骤配置 Supabase 连接:
        
        1. **配置环境变量** (推荐):
        ```bash
        export SUPABASE_URL="your-supabase-url"
        export SUPABASE_KEY="your-supabase-service-role-key"
        ```
        
        2. **或编辑 .streamlit/secrets.toml** 文件:
        ```toml
        SUPABASE_URL = "your-supabase-url"
        SUPABASE_KEY = "your-supabase-service-role-key"
        ```
        
        3. **获取 Supabase 配置信息**:
        - 登录 [Supabase.com](https://supabase.com)
        - 进入您的项目
        - 在 Settings → API 中找到 URL 和 service_role key
        """)
        st.stop()
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        # 测试连接
        supabase.table('stocks').select('update_date').limit(1).execute()
        return supabase
    except Exception as e:
        st.error(f"❌ Supabase 连接失败: {e}")
        st.warning("""
        常见问题解决方案:
        - 检查 API 密钥是否正确 (应使用 service_role key，不是 anon key)
        - 确认项目 URL 格式正确 (https://your-project.supabase.co)
        - 检查网络连接是否正常
        - 验证数据库中是否存在 'stocks' 表
        """)
        st.stop()

@st.cache_data(ttl=300)  # 缓存5分钟
def get_available_dates(_supabase):
    """获取可用的数据日期"""
    try:
        response = _supabase.table('stocks').select('update_date').execute()
        dates = [row['update_date'] for row in response.data]
        unique_dates = sorted(list(set(dates)), reverse=True)
        return unique_dates
    except Exception as e:
        st.error(f"❌ 获取日期列表失败: {e}")
        return []

@st.cache_data(ttl=300)
def get_stocks_by_date(_supabase, selected_date):
    """根据日期获取股票数据"""
    try:
        response = _supabase.table('stocks').select('*').eq('update_date', selected_date).execute()
        if response.data:
            df = pd.DataFrame(response.data)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ 获取股票数据失败: {e}")
        return pd.DataFrame()

def format_number(value, decimals=2):
    """格式化数字显示"""
    if pd.isna(value) or value is None:
        return "N/A"
    try:
        return f"{float(value):.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)

def format_percentage(value):
    """格式化百分比显示"""
    if pd.isna(value) or value is None:
        return "N/A"
    try:
        formatted = f"{float(value):.2f}%"
        return formatted if float(value) >= 0 else formatted
    except (ValueError, TypeError):
        return str(value)

def main():
    """主应用程序"""
    # 应用标题
    st.title("📊 股票数据分析面板")
    st.markdown("---")
    
    # 初始化 Supabase 连接
    supabase = init_supabase()
    
    # 侧边栏 - 日期选择
    st.sidebar.header("📅 数据筛选")
    
    # 获取可用日期
    available_dates = get_available_dates(supabase)
    
    if not available_dates:
        st.warning("⚠️ 暂无数据，请先运行数据获取脚本")
        st.stop()
    
    # 日期选择器
    selected_date = st.sidebar.selectbox(
        "选择日期",
        available_dates,
        format_func=lambda x: f"{x} ({'今天' if x == datetime.now().strftime('%Y-%m-%d') else ''})"
    )
    
    # 获取选定日期的数据
    df = get_stocks_by_date(supabase, selected_date)
    
    if df.empty:
        st.warning(f"⚠️ {selected_date} 无股票数据")
        return
    
    # 计算汇总统计
    total_stocks = len(df)
    avg_change = df['latest_change_pct'].mean() if 'latest_change_pct' in df.columns else 0
    avg_auction_change = df['auction_change_pct'].mean() if 'auction_change_pct' in df.columns else 0
    
    # 顶部汇总展示
    st.header(f"📈 {selected_date} 数据概览")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="符合条件股票数量",
            value=f"{total_stocks} 只",
            delta=None
        )
    
    with col2:
        change_color = "positive" if avg_change >= 0 else "negative"
        st.metric(
            label="平均涨跌幅",
            value=format_percentage(avg_change),
            delta=None
        )
    
    with col3:
        auction_color = "positive" if avg_auction_change >= 0 else "negative"
        st.metric(
            label="平均竞价涨幅",
            value=format_percentage(avg_auction_change),
            delta=None
        )
    
    with col4:
        positive_count = len(df[df['latest_change_pct'] > 0]) if 'latest_change_pct' in df.columns else 0
        positive_ratio = (positive_count / total_stocks * 100) if total_stocks > 0 else 0
        st.metric(
            label="上涨股票占比",
            value=f"{positive_ratio:.1f}%",
            delta=f"{positive_count}/{total_stocks}"
        )
    
    st.markdown("---")
    
    # 数据表格展示
    st.header("📋 股票详细数据")
    
    # 筛选和排序选项
    col1, col2 = st.columns(2)
    
    with col1:
        sort_by = st.selectbox(
            "排序字段",
            ["latest_change_pct", "auction_change_pct", "pe_ttm", "market_cap", "volume_ratio"],
            format_func=lambda x: {
                "latest_change_pct": "最新涨跌幅",
                "auction_change_pct": "竞价涨幅", 
                "pe_ttm": "市盈率TTM",
                "market_cap": "总市值",
                "volume_ratio": "量比"
            }.get(x, x)
        )
    
    with col2:
        sort_order = st.selectbox("排序方式", ["降序", "升序"])
        ascending = sort_order == "升序"
    
    # 处理数据显示
    display_df = df.copy()
    
    # 选择要显示的列
    display_columns = [
        'code', 'stock_name', 'latest_price', 'latest_change_pct',
        'auction_change_pct', 'pe_ttm', 'market_cap', 'volume_ratio',
        'listing_board', 'auction_type', 'auction_rating'
    ]
    
    # 过滤存在的列
    display_columns = [col for col in display_columns if col in display_df.columns]
    display_df = display_df[display_columns]
    
    # 重命名列
    column_names = {
        'code': '股票代码',
        'stock_name': '股票名称',
        'latest_price': '最新价',
        'latest_change_pct': '最新涨跌幅(%)',
        'auction_change_pct': '竞价涨幅(%)',
        'pe_ttm': '市盈率TTM',
        'market_cap': '总市值',
        'volume_ratio': '量比',
        'listing_board': '上市板块',
        'auction_type': '竞价异动类型',
        'auction_rating': '竞价评级'
    }
    display_df = display_df.rename(columns=column_names)
    
    # 排序
    if sort_by in df.columns:
        display_df = display_df.sort_values(
            by=column_names.get(sort_by, sort_by), 
            ascending=ascending
        )
    
    # 格式化数值列
    if '最新价' in display_df.columns:
        display_df['最新价'] = display_df['最新价'].apply(lambda x: format_number(x))
    if '最新涨跌幅(%)' in display_df.columns:
        display_df['最新涨跌幅(%)'] = display_df['最新涨跌幅(%)'].apply(format_percentage)
    if '竞价涨幅(%)' in display_df.columns:
        display_df['竞价涨幅(%)'] = display_df['竞价涨幅(%)'].apply(format_percentage)
    if '市盈率TTM' in display_df.columns:
        display_df['市盈率TTM'] = display_df['市盈率TTM'].apply(lambda x: format_number(x))
    if '总市值' in display_df.columns:
        display_df['总市值'] = display_df['总市值'].apply(lambda x: f"{float(x)/100000000:.2f}亿" if pd.notna(x) and x != 'N/A' else 'N/A')
    if '量比' in display_df.columns:
        display_df['量比'] = display_df['量比'].apply(lambda x: format_number(x))
    
    # 显示表格
    st.dataframe(
        display_df,
        use_container_width=True,
        height=600,
        column_config={
            "股票代码": st.column_config.TextColumn("股票代码", width="small"),
            "股票名称": st.column_config.TextColumn("股票名称", width="medium"),
            "最新涨跌幅(%)": st.column_config.NumberColumn(
                "最新涨跌幅(%)",
                help="股票最新涨跌幅百分比",
                width="small"
            ),
        }
    )
    
    # 底部信息
    st.markdown("---")
    st.info(f"📊 数据更新时间: {selected_date} | 数据来源: 1000%的男人")

if __name__ == "__main__":
    main()