-- Supabase 数据表创建 SQL
-- 在 Supabase SQL Editor 中执行此脚本来创建 stocks 表

CREATE TABLE IF NOT EXISTS public.stocks (
    id SERIAL PRIMARY KEY,
    code INTEGER NOT NULL,
    stock_name TEXT NOT NULL,
    latest_price DECIMAL(10,4),
    latest_change_pct DECIMAL(8,4),
    listing_board TEXT,
    auction_change_pct DECIMAL(8,4),
    pe_ttm DECIMAL(10,4),
    pe DECIMAL(10,4),
    dde_large_order DECIMAL(15,4),
    volume_ratio DECIMAL(10,4),
    interval_change_13d DECIMAL(8,4),
    interval_change_5d DECIMAL(8,4),
    listing_days INTEGER,
    forecast_pe_1y DECIMAL(10,4),
    forecast_pe_2y DECIMAL(10,4),
    forecast_pe_3y DECIMAL(10,4),
    market_cap DECIMAL(20,4),
    eps DECIMAL(10,6),
    gross_margin DECIMAL(8,4),
    net_margin DECIMAL(8,4),
    auction_price DECIMAL(10,4),
    auction_type TEXT,
    auction_desc TEXT,
    auction_rating TEXT,
    auction_volume BIGINT,
    auction_amount BIGINT,
    market_code INTEGER,
    update_date DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_stocks_code ON public.stocks(code);
CREATE INDEX IF NOT EXISTS idx_stocks_update_date ON public.stocks(update_date);
CREATE INDEX IF NOT EXISTS idx_stocks_latest_price ON public.stocks(latest_price);
CREATE INDEX IF NOT EXISTS idx_stocks_change_pct ON public.stocks(latest_change_pct);
CREATE INDEX IF NOT EXISTS idx_stocks_code_date ON public.stocks(code, update_date);

-- 创建唯一约束，防止同一股票同一日期重复数据
CREATE UNIQUE INDEX IF NOT EXISTS idx_stocks_code_date_unique 
ON public.stocks(code, update_date);

-- 启用行级安全策略（RLS）
ALTER TABLE public.stocks ENABLE ROW LEVEL SECURITY;

-- 创建策略：允许所有用户读取数据
CREATE POLICY "Enable read access for all users" ON public.stocks
FOR SELECT USING (true);

-- 创建策略：允许服务角色插入和更新数据
CREATE POLICY "Enable insert for service role" ON public.stocks
FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update for service role" ON public.stocks
FOR UPDATE USING (true);

-- 添加自动更新时间戳的触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_stocks_updated_at 
    BEFORE UPDATE ON public.stocks 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();