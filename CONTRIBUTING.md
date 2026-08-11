# 贡献指南

感谢你愿意为 Hot News Daily 贡献代码！

## 如何贡献

### 报告 Bug

1. 在 [Issues](https://github.com/oneyesok/hot-news-daily/issues) 中搜索是否已有相同问题
2. 使用 Bug Report 模板提交，附上错误日志和环境信息

### 提新功能

1. 先在 Issues 中讨论想法
2. 获得认可后提 PR

### 提 PR

```bash
# Fork 并克隆
git clone https://github.com/YOUR_USERNAME/hot-news-daily.git
cd hot-news-daily

# 创建分支
git checkout -b feat/my-feature

# 开发 & 测试
pip install -r requirements.txt pytest
pytest tests/ -v

# 提交（使用约定式提交格式）
git commit -m "feat: 添加 GitHub Trending 数据源"

# 推送并开 PR
git push origin feat/my-feature
```

### 代码规范

- Python 3.10+
- 类型标注（函数签名）
- 抓取器返回 `list[str]`
- 测试覆盖新增代码
- 提交信息使用 [约定式提交](https://www.conventionalcommits.org/zh-hans/) 格式

## 添加新数据源

1. 在 `hot_news_daily/fetchers/` 下新建 `.py` 文件
2. 实现 `fetch_xxx() -> list[str]`
3. 在 `hot_news_daily/fetchers/__init__.py` 中导出
4. 在 `hot_news_daily/main.py` 中注册
5. 添加测试 `tests/test_fetchers.py`
