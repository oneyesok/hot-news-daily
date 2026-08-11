"""抓取器基础测试."""

import pytest
from hot_news_daily.fetchers import (
    fetch_36kr,
    fetch_baidu,
    fetch_ithome,
    fetch_juejin,
)


class TestFetchers:
    """验证每个抓取器至少能返回非空列表且不抛异常."""

    def test_fetch_ithome(self):
        result = fetch_ithome()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_fetch_36kr(self):
        result = fetch_36kr()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_fetch_juejin(self):
        result = fetch_juejin()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_fetch_baidu(self):
        result = fetch_baidu()
        assert isinstance(result, list)
        assert len(result) > 0
