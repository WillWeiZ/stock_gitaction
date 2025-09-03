# 🎯 启动指南

## ✅ 配置已完成

您的 Supabase URL 和 API 密钥已经正确配置到所有必要的文件中。

## 🚀 立即启动应用

### 最简单的方式：

```bash
# 直接启动应用（配置已在 secrets.toml 中）
streamlit run app.py
```

应用将在浏览器中自动打开：http://localhost:8501

### 或使用启动脚本：

```bash
./start_app.sh
```

## 📊 应用功能

启动成功后，您可以：

1. **📅 选择日期**: 在侧边栏选择 2025-09-03（当前可用的日期）
2. **📈 查看汇总**: 顶部显示 30 只符合条件的股票统计
3. **📋 浏览详情**: 滚动查看完整的股票数据表格
4. **🔄 排序数据**: 按涨跌幅、市盈率等字段排序

## 🧪 测试连接

如果需要验证配置：

```bash
python test_connection.py
```

应该看到：
```
✅ Supabase 客户端创建成功
✅ 数据库连接成功
📊 数据库中共有 30 条股票记录
🎉 配置正确！
```

## ❓ 如果遇到问题

1. **端口占用**: 修改端口 `streamlit run app.py --server.port=8502`
2. **依赖缺失**: `pip install -r requirements.txt`
3. **查看详细文档**: 阅读 `USAGE.md` 或 `QUICKSTART.md`

## 🎉 享受使用！

您的股票数据分析系统已经完全就绪，包括：
- ✅ 自动化数据获取 (GitHub Actions)
- ✅ 云端数据存储 (Supabase)  
- ✅ 精美的 Web 界面 (Streamlit)
- ✅ 钉钉通知功能

现在就可以开始分析您的股票数据了！📈