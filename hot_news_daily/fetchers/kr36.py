"""36氪 快讯抓取 — 通过 API 获取."""

import logging
from typing import Any, Dict, List

import requests

logger = logging.getLogger(__name__)

KR36_API = "https://www.36kr.com/api/newsflash"
REQUEST_TIMEOUT = 15
TARGET_COUNT = 5
MIN_TITLE_LENGTH = 8


def fetch_36kr() -> List[str]:
    """通过 36氪开放 API 抓取快讯 TOP 5."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(KR36_API, headers=headers, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        data: Dict[str, Any] = resp.json()
        items = data.get("data", {}).get("items", [])

        news: List[str] = []
        for item in items[:TARGET_COUNT]:
            title = item.get("title", "")
            if title and len(title) >= MIN_TITLE_LENGTH:
                news.append(f"• {title}")

        logger.info("36氪 抓取完成（API），获取 %d 条", len(news))
        return news if news else ["暂无内容"]

    except requests.RequestException as e:
        logger.error("36氪 API 请求失败: %s", e)
        return [f"抓取失败: {e}"]
    except Exception as e:
        logger.exception("36氪 未知错误")
        return [f"未知错误: {e}"]
