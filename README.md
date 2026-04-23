# 📊 每日科技热点自动推送

自动抓取 IT之家、36氪、掘金、百度热搜，通过 QQ 邮箱每日定时发送。

## 数据源

| 来源 | 内容 |
|------|------|
| IT之家 | 科技新闻 TOP 10 |
| 36氪 | 快讯 TOP 5 |
| 掘金 | 热门文章 TOP 5 |
| 百度热搜 | 实时热搜 TOP 5 |

## 定时发送

每天 5 次：北京时间 08:00 / 12:00 / 15:00 / 18:00 / 21:00

## 手动触发

去 Actions 页面点击 `hot_news.yml` → `Run workflow` 即可手动执行。

## 配置 Secrets

在 GitHub 仓库 Settings → Secrets 中添加：

| Name | 说明 |
|------|------|
| `SENDER_EMAIL` | 发件人 QQ 邮箱 |
| `SMTP_PASSWORD` | QQ 邮箱 SMTP 授权码 |
| `RECEIVER_EMAIL` | 收件人邮箱 |
