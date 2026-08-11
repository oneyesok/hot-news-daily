"""数据抓取器集合."""

from hot_news_daily.fetchers.ithome import fetch_ithome
from hot_news_daily.fetchers.kr36 import fetch_36kr
from hot_news_daily.fetchers.juejin import fetch_juejin
from hot_news_daily.fetchers.baidu import fetch_baidu

__all__ = ["fetch_ithome", "fetch_36kr", "fetch_juejin", "fetch_baidu"]
