import requests
import sys
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# SMTP 配置（从环境变量读取）
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "1808203134@qq.com")
SENDER_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", "1808203134@qq.com")

# IT之家过滤词
ITHOME_BLOCK_WORDS = ["下载", "合集", "大全", "立即下载", "固件", "壁纸", "主题", "字体"]


def get_ithome_news():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
        res = requests.get("https://www.ithome.com/", headers=headers, timeout=15)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")
        seen = set()
        news = []
        for a in soup.select("a[href]"):
            href = a.get("href", "")
            if "/0/" not in href:
                continue
            title = a.get_text(strip=True)
            if not title or len(title) < 10:
                continue
            if any(w in title for w in ITHOME_BLOCK_WORDS):
                continue
            if href in seen:
                continue
            seen.add(href)
            news.append("• " + title)
            if len(news) >= 10:
                break
        return news if news else ["暂无内容"]
    except Exception as e:
        return ["抓取失败：" + str(e)]


def get_36kr_news():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
        res = requests.get("https://36kr.com/newsflashes", headers=headers, timeout=15)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")
        news = []
        for item in soup.select("a[class*=title]")[:5]:
            title = item.get_text(strip=True)
            if title and len(title) > 10:
                news.append("• " + title)
        return news if news else ["暂无内容"]
    except Exception as e:
        return ["抓取失败：" + str(e)]


def get_juejin_news():
    try:
        headers = {"Content-Type": "application/json"}
        data = {"id_type": 2, "cate_id": "6809637773935378440", "sort_type": 300, "cursor": "0", "limit": 5}
        res = requests.post(
            "https://api.juejin.cn/recommend_api/v1/article/recommend_cate_feed",
            headers=headers, json=data, timeout=15
        )
        items = res.json().get("data", [])[:5]
        news = []
        for item in items:
            title = item.get("article_info", {}).get("title", "")
            if title:
                news.append("• " + title)
        return news if news else ["暂无内容"]
    except Exception as e:
        return ["抓取失败：" + str(e)]


def get_baidu_hot():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(
            "https://top.baidu.com/api/board?platform=wise&ent=zbdata&sdk=1",
            headers=headers, timeout=15
        )
        data = res.json()
        news = []
        if data.get("success"):
            content_list = data["data"]["cards"][0]["content"][0]["content"]
            for item in content_list[:5]:
                word = item.get("word", "")
                if word:
                    news.append("• " + word + " 🔥")
        return news if news else ["暂无内容"]
    except Exception as e:
        return ["抓取失败：" + str(e)]


def send_email(content):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = "📊 今日科技热点 " + datetime.now().strftime("%Y-%m-%d %H:%M")
    msg.attach(MIMEText(content, "plain", "utf-8"))
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    print(f"[{datetime.now()}] 邮件发送成功 ✓")


def main():
    print(f"[{datetime.now()}] 开始抓取热点...", flush=True)

    ithome = get_ithome_news()
    kr36 = get_36kr_news()
    juejin = get_juejin_news()
    baidu = get_baidu_hot()

    content = f"""📊 今日科技热点
时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}

=== IT之家 ===
{chr(10).join(ithome)}

=== 36氪 ===
{chr(10).join(kr36)}

=== 掘金热门 🔥 ===
{chr(10).join(juejin)}

=== 百度热搜 🔥 ===
{chr(10).join(baidu)}
"""
    print(content)
    send_email(content)
    print(f"[{datetime.now()}] 任务完成", flush=True)


if __name__ == "__main__":
    main()
