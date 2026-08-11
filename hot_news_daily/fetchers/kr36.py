"""36氪 快讯抓取."""

import logging
from typing import List

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

KR36_URL = "https://36kr.com/newsflashes"
REQUEST_TIMEOUT = 15
TARGET_COUNT = 5
MIN_TITLE_LENGTH = 10


def fetch_36kr() -> List[str]:
    """抓取 36氪 快讯 TOP 5."""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(KR36_URL, headers=headers, timeout=REQUEST_TIMEOUT)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        news: List[str] = []
        for item in soup.select("a[class*=title]")[:TARGET_COUNT]:
            title = item.get_text(strip=True)
            if title and len(title) > MIN_TITLE_LENGTH:
                news.append(f"• {title}")

        logger.info("36氪 抓取完成，获取 %d 条", len(news))
        return news if news else ["暂无内容"]

    except requests.RequestException as e:
        logger.error("36氪 抓取失败: %s", e)
        return [f"抓取失败: {e}"]
    except Exception as e:
        logger.exception("36氪 未知错误")
        return [f"未知错误: {e}"]
