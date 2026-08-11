"""IT之家 科技新闻抓取."""

import logging
from typing import List

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

IT_HOME_URL = "https://www.ithome.com/"
BLOCK_WORDS = ["下载", "合集", "大全", "立即下载", "固件", "壁纸", "主题", "字体"]
REQUEST_TIMEOUT = 15
TARGET_COUNT = 10
MIN_TITLE_LENGTH = 10


def fetch_ithome() -> List[str]:
    """抓取 IT之家 首页科技新闻 TOP 10."""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(IT_HOME_URL, headers=headers, timeout=REQUEST_TIMEOUT)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        seen: set = set()
        news: List[str] = []

        for a in soup.select("a[href]"):
            href = a.get("href", "")
            if "/0/" not in href:
                continue
            title = a.get_text(strip=True)
            if not title or len(title) < MIN_TITLE_LENGTH:
                continue
            if any(w in title for w in BLOCK_WORDS):
                continue
            if href in seen:
                continue
            seen.add(href)
            news.append(f"• {title}")
            if len(news) >= TARGET_COUNT:
                break

        logger.info("IT之家 抓取完成，获取 %d 条", len(news))
        return news if news else ["暂无内容"]

    except requests.RequestException as e:
        logger.error("IT之家 抓取失败: %s", e)
        return [f"抓取失败: {e}"]
    except Exception as e:
        logger.exception("IT之家 未知错误")
        return [f"未知错误: {e}"]
