# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an automated stock data collection system that runs on GitHub Actions. It fetches stock data from TongHuaShun (同花顺) financial platform, stores it in Supabase database, and sends notifications via DingTalk.

## Architecture

The system consists of three main components:

1. **Data Collection (`fetch_stock_data.py`)**: Core Python script that uses `pywencai` library to query TongHuaShun API with specific stock screening criteria
2. **Database Storage**: Supabase PostgreSQL database with a `stocks` table containing comprehensive stock information
3. **Automation**: GitHub Actions workflow that runs on weekdays at 9:27 AM Beijing time

## Key Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the main script locally (requires environment variables)
python fetch_stock_data.py

# Test GitHub Actions workflow manually
gh workflow run "股票数据获取定时任务"

# View recent workflow runs
gh run list --limit 5

# Check workflow logs
gh run view <run-id> --log
```

## Environment Variables

Required for operation:
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase service role key (not anon key)
- `THS_COOKIE`: Authentication cookie from TongHuaShun website
- `DINGTALK_WEBHOOK`: DingTalk robot webhook URL (optional)

## Database Setup

Execute `supabase_setup.sql` in Supabase SQL Editor to create the database schema. The script creates:
- `stocks` table with comprehensive stock data fields
- Unique constraints on `(code, update_date)`
- Proper indexes for performance
- Row Level Security policies

## Stock Screening Criteria

The system queries stocks matching these conditions:
- Non-ST stocks, non-STAR market
- Auction price change between 1%-6%
- TTM PE ratio (not loss-making)
- Large order net volume > 0
- Auction volume ratio > 1
- 10-day gain ≥ 10%, 5-day gain ≥ 10%
- Listed for more than 100 days

## Field Mapping Challenges

TongHuaShun API returns field names with date suffixes (e.g., `竞价涨幅[20250903]`). The code uses:
- `get_value_fuzzy()` for partial string matching
- `get_interval_change()` for handling multiple time interval fields
- Data cleaning before database insertion

## GitHub Actions Workflow

The workflow (`.github/workflows/stock-data.yml`):
- Runs on weekdays at 9:27 AM Beijing time (`cron: '27 1 * * 1-5'`)
- Supports manual triggering via `workflow_dispatch`
- Uploads Excel files as artifacts for 7 days
- Uses Python 3.9 environment

## Troubleshooting

Common issues:
- **Cookie expiration**: THS_COOKIE needs periodic renewal from browser
- **Duplicate key errors**: The script handles this by deleting existing daily data before insertion
- **Field mapping failures**: Field names from TongHuaShun API may change, requiring updates to mapping logic

## Testing

Manual testing workflow:
1. Trigger workflow manually via GitHub Actions UI
2. Monitor execution logs for data collection success
3. Verify data insertion in Supabase database
4. Check DingTalk notifications if configured