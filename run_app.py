"""
股票数据分析 Streamlit 应用启动脚本
运行此脚本来启动 Web 应用
"""

import subprocess
import sys
import os

def main():
    """启动 Streamlit 应用"""
    print("🚀 启动股票数据分析面板...")
    
    # 检查环境变量
    if not os.getenv('SUPABASE_URL'):
        print("⚠️  注意: 未检测到 SUPABASE_URL 环境变量")
        print("   请确保在 .streamlit/secrets.toml 中配置了正确的 Supabase 连接信息")
    
    try:
        # 启动 Streamlit 应用
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
        return 0

if __name__ == "__main__":
    exit(main())