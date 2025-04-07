import requests
from typing import List, Dict, Any, Union
from .models import *
from .exceptions import QOSAPIError
from .constants import BASE_URL

class QOSHttpClient:
    def __init__(self, api_key: str):
        self.base_url = BASE_URL
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, endpoint: str, data: dict = None) -> dict:
        params = {"key": self.api_key}
        try:
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                json=data,
                params=params,
                timeout=10
            )
            result = response.json()
            if result.get("msg") != "OK":
                raise QOSAPIError(result.get("msg", "Unknown error"))
            return result["data"]
        except requests.exceptions.RequestException as e:
            raise QOSAPIError(f"HTTP request failed: {str(e)}")

    def get_instrument_info(self, codes: List[str]) -> List[InstrumentInfo]:
        """4.2 获取品种基础信息"""
        endpoint = "/instrument-info"
        data = {"codes": codes}
        return [InstrumentInfo(**item) for item in self._request(endpoint, data)]

    def get_snapshot(self, codes: List[str]) -> List[QuoteSnapshot]:
        """4.3 获取行情快照"""
        endpoint = "/snapshot"
        data = {"codes": codes}
        return [QuoteSnapshot(**item) for item in self._request(endpoint, data)]

    def get_depth(self, codes: List[str]) -> List[MarketDepth]:
        """4.4 获取盘口深度"""
        endpoint = "/depth"
        data = {"codes": codes}
        return [MarketDepth(**item) for item in self._request(endpoint, data)]

    def get_trades(self, codes: List[str], count: int = 1) -> List[TradeTick]:
        """4.5 获取逐笔成交"""
        endpoint = "/trade"
        data = {
            "codes": codes,
            "count": min(count, 50)
        }
        return [TradeTick(**item) for item in self._request(endpoint, data)]

    def get_kline(self, codes: List[str], ktype: int, count: int, adjust: int = 0) -> List[KLine]:
        """4.6 获取K线数据"""
        endpoint = "/kline"
        data = {
            "kline_reqs": [{
                "c": code,
                "kt": ktype,
                "co": count,
                "a": adjust
            }
            for code in codes
            ]
        }
        results = []
        for item in self._request(endpoint, data):
            results.extend([KLine(**k) for k in item["k"]])
        return results

    def get_history_kline(self, codes: List[str], ktype: int, end_time: int, count: int, adjust: int = 0) -> List[KLine]:
        """4.7 获取历史K线"""
        endpoint = "/history"
        data = {
            "kline_reqs": [{
                "c": code,
                "kt": ktype,
                "e": end_time,
                "co": count,
                "a": adjust
            }
            for code in codes
            ]
        }
        results = []
        for item in self._request(endpoint, data):
            results.extend([KLine(**k) for k in item["k"]])
        return results