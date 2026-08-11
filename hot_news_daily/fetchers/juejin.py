"""掘金 热门文章抓取."""

import logging
from typing import Any, Dict, List

import requests

logger = logging.getLogger(__name__)

JUEJIN_API = "https://api.juejin.cn/recommend_api/v1/article/recommend_cate_feed"
REQUEST_TIMEOUT = 15
TARGET_COUNT = 5


def fetch_juejin() -> List[str]:
    """抓取掘金热门文章 TOP 5."""
    try:
        headers = {"Content-Type": "application/json"}
        payload: Dict[str, Any] = {
            "id_type": 2,
            "cate_id": "6809637773935378440",
            "sort_type": 300,
            "cursor": "0",
            "limit": TARGET_COUNT,
        }
        resp = requests.post(
            JUEJIN_API, headers=headers, json=payload, timeout=REQUEST_TIMEOUT
        )
        resp.raise_for_status()

        items = resp.json().get("data", [])[:TARGET_COUNT]
        news: List[str] = []
        for item in items:
            article = item.get("article_info", {})
            title = article.get("title", "")
            if title:
                news.append(f"• {title}")

        logger.info("掘金 抓取完成，获取 %d 条", len(news))
        return news if news else ["暂无内容"]

    except requests.RequestException as e:
        logger.error("掘金 抓取失败: %s", e)
        return [f"抓取失败: {e}"]
    except Exception as e:
        logger.exception("掘金 未知错误")
        return [f"未知错误: {e}"]
