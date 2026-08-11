# 📊 Hot News Daily

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![CI](https://github.com/oneyesok/hot-news-daily/actions/workflows/hot_news.yml/badge.svg)](https://github.com/oneyesok/hot-news-daily/actions/workflows/hot_news.yml)

**每日科技热点自动抓取 & 邮箱推送** — 零成本部署在 GitHub Actions，每天 5 次自动推送 IT之家 / 36氪 / 掘金 / 百度热搜到你的邮箱。

> 🇬🇧 Automated daily tech news aggregator — fetches headlines from IT之家, 36Kr, Juejin, Baidu Hot Search, and delivers them to your inbox via GitHub Actions. Zero server cost.

---

## ✨ 功能

- 🔄 **多源聚合** — IT之家、36氪、掘金、百度热搜
- ⏰ **定时推送** — 每天 5 次（北京时间 08:00 / 12:00 / 15:00 / 18:00 / 21:00）
- 📧 **QQ 邮箱投递** — 纯文本邮件，任何设备都能看
- 🆓 **零成本运行** — 依托 GitHub Actions 免费额度
- 🧩 **模块化设计** — 抓取器独立，方便扩展新数据源

---

## 📸 效果预览

<!-- TODO: 添加邮件截图 -->
> 收到邮件示例 — 多来源热点一目了然

```
📊 今日科技热点
时间: 2025-08-12 08:00

=== IT之家 ===
• Apple 正式发布 iOS 19 开发者预览版
• 特斯拉 FSD v14 在中国获批测试
• ...

=== 36氪 ===
• 字节跳动旗下 AI 产品全球月活突破 2 亿
• ...

=== 掘金热门 🔥 ===
• 2025 年前端工具链全景图
• ...

=== 百度热搜 🔥 ===
• 某某事件 🔥
• ...
```

---

## 🚀 快速开始

### 1. Fork 本仓库

点击右上角 **Fork** 按钮。

### 2. 配置 Secrets

在 Fork 后的仓库 → **Settings** → **Secrets and variables** → **Actions** 中添加三个 Secret：

| Name | 说明 |
|------|------|
| `SENDER_EMAIL` | 发件 QQ 邮箱（如 `123456@qq.com`） |
| `SMTP_PASSWORD` | QQ 邮箱 SMTP 授权码 |
| `RECEIVER_EMAIL` | 收件邮箱 |

> 获取 QQ 邮箱 SMTP 授权码：QQ 邮箱 → 设置 → 账户 → POP3/SMTP 服务 → 开启并生成授权码

### 3. 启用 Actions

进入 **Actions** 标签页，点击「I understand my workflows, go ahead and enable them」。

### 4. 测试运行

在 Actions 页面选择 `每日热点推送` → **Run workflow** 手动触发一次，检查邮箱是否收到。

---

## 🏗️ 项目结构

```
hot-news-daily/
├── .github/workflows/hot_news.yml   # GitHub Actions 定时任务
├── hot_news_daily/                  # 主包
│   ├── __init__.py
│   ├── config.py                    # 配置加载（环境变量）
│   ├── email.py                     # 邮件排版与发送
│   ├── main.py                      # 主流程编排
│   └── fetchers/                    # 数据源抓取器
│       ├── __init__.py
│       ├── ithome.py                # IT之家
│       ├── kr36.py                  # 36氪
│       ├── juejin.py                # 掘金
│       └── baidu.py                 # 百度热搜
├── tests/                           # 测试
│   └── test_fetchers.py
├── run.py                           # 便捷入口
├── requirements.txt
├── .env.example                     # 本地运行环境变量模板
├── LICENSE
└── README.md
```

---

## 💻 本地开发

```bash
# 克隆
git clone https://github.com/oneyesok/hot-news-daily.git
cd hot-news-daily

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入真实邮箱和授权码

# 运行
python run.py

# 运行测试
pip install pytest
pytest tests/ -v
```

---

## 🔧 扩展数据源

想添加新的数据源？在 `hot_news_daily/fetchers/` 下新建一个文件，实现 `fetch_xxx() -> list[str]`，然后在 `main.py` 中注册即可。

```python
# hot_news_daily/fetchers/github_trending.py
def fetch_github_trending() -> list[str]:
    ...
```

---

## 🤝 贡献

欢迎提 Issue 和 PR！请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📄 License

MIT © [oneyesok](https://github.com/oneyesok)
