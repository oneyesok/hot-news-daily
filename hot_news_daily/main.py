"""主入口 — 协调抓取、排版、发送."""

import logging
import sys
from datetime import datetime

from hot_news_daily.config import load_config
from hot_news_daily.email import build_content, send_email
from hot_news_daily.fetchers import fetch_36kr, fetch_baidu, fetch_ithome, fetch_juejin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger("hot_news_daily")


def run() -> None:
    logger.info("开始抓取热点…")

    cfg = load_config()

    sources = [
        ("IT之家", fetch_ithome),
        ("36氪", fetch_36kr),
        ("掘金热门 🔥", fetch_juejin),
        ("百度热搜 🔥", fetch_baidu),
    ]

    sections = []
    for label, fetcher in sources:
        try:
            items = fetcher()
        except Exception:
            logger.exception("%s 抓取异常", label)
            items = [f"{label} 抓取异常，请检查日志"]
        sections.append((label, items))

    content = build_content(sections)
    print(content, flush=True)

    send_email(cfg.smtp, content)
    logger.info("任务完成 ✓")


if __name__ == "__main__":
    run()
