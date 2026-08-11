"""百度热搜抓取."""

import logging
from typing import Any, Dict, List

import requests

logger = logging.getLogger(__name__)

BAIDU_API = "https://top.baidu.com/api/board?platform=wise&ent=zbdata&sdk=1"
REQUEST_TIMEOUT = 15
TARGET_COUNT = 5


def fetch_baidu() -> List[str]:
    """抓取百度实时热搜 TOP 5."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(BAIDU_API, headers=headers, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        data: Dict[str, Any] = resp.json()
        news: List[str] = []

        if data.get("success"):
            cards = data["data"]["cards"]
            if cards:
                content = cards[0]["content"]
                if content:
                    items = content[0].get("content", [])
                    for item in items[:TARGET_COUNT]:
                        word = item.get("word", "")
                        if word:
                            news.append(f"• {word} 🔥")

        logger.info("百度热搜 抓取完成，获取 %d 条", len(news))
        return news if news else ["暂无内容"]

    except requests.RequestException as e:
        logger.error("百度热搜 抓取失败: %s", e)
        return [f"抓取失败: {e}"]
    except Exception as e:
        logger.exception("百度热搜 未知错误")
        return [f"未知错误: {e}"]
