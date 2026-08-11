"""36氪 快讯抓取 — 通过 36氪 Gateway API 实时获取."""

import logging
from typing import Any, Dict, List

import requests

logger = logging.getLogger(__name__)

KR36_API = "https://gateway.36kr.com/api/mis/nav/newsflash/flow"
REQUEST_TIMEOUT = 15
TARGET_COUNT = 5
MIN_TITLE_LENGTH = 8


def fetch_36kr() -> List[str]:
    """通过 36氪 Gateway API 抓取实时快讯 TOP 5."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "partner_id": "web",
            "param": {
                "siteId": 1,
                "platformId": 2,
                "pageSize": TARGET_COUNT,
                "pageEvent": 0,
            },
        }
        resp = requests.post(
            KR36_API, headers=headers, json=payload, timeout=REQUEST_TIMEOUT
        )
        resp.raise_for_status()

        data: Dict[str, Any] = resp.json()
        items = data.get("data", {}).get("itemList", [])

        news: List[str] = []
        for item in items[:TARGET_COUNT]:
            material = item.get("templateMaterial", {})
            title = material.get("widgetTitle", "") or material.get("content", "")
            if title and len(title) >= MIN_TITLE_LENGTH:
                news.append(f"• {title}")

        logger.info("36氪 抓取完成（Gateway API），获取 %d 条", len(news))
        return news if news else ["暂无内容"]

    except requests.RequestException as e:
        logger.error("36氪 Gateway API 请求失败: %s", e)
        return [f"抓取失败: {e}"]
    except Exception as e:
        logger.exception("36氪 未知错误")
        return [f"未知错误: {e}"]
