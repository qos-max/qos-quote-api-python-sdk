from typing import Optional, List
from .http_client import QOSHttpClient
from .ws_client import QOSWebSocketClient
from .models import *

class QOSClient:
    """QOS行情API统一客户端"""
    
    def __init__(self, api_key: str):
        """
        初始化客户端
        :param api_key: 官网注册的API Key
        """
        self._api_key = api_key
        self._http_client: Optional[QOSHttpClient] = None
        self._ws_client: Optional[QOSWebSocketClient] = None

    @property
    def http(self) -> QOSHttpClient:
        """HTTP客户端"""
        if self._http_client is None:
            self._http_client = QOSHttpClient(self._api_key)
        return self._http_client

    @property
    def ws(self) -> QOSWebSocketClient:
        """WebSocket客户端"""
        if self._ws_client is None:
            self._ws_client = QOSWebSocketClient(self._api_key)
        return self._ws_client

    # HTTP接口
    def get_instrument_info(self, codes: List[str]) -> List[InstrumentInfo]:
        """4.2 获取品种基础信息"""
        return self.http.get_instrument_info(codes)

    def get_snapshot(self, codes: List[str]) -> List[QuoteSnapshot]:
        """4.3 获取行情快照"""
        return self.http.get_snapshot(codes)

    def get_depth(self, codes: List[str]) -> List[MarketDepth]:
        """4.4 获取盘口深度"""
        return self.http.get_depth(codes)

    def get_trades(self, codes: List[str], count: int = 1) -> List[TradeTick]:
        """4.5 获取逐笔成交"""
        return self.http.get_trades(codes, count)

    def get_kline(self, codes: List[str], ktype: int, count: int, adjust: int = 0) -> List[KLine]:
        """4.6 获取K线数据"""
        return self.http.get_kline(codes, ktype, count, adjust)

    def get_history_kline(self, codes: List[str], ktype: int, end_time: int, count: int, adjust: int = 0) -> List[KLine]:
        """4.7 获取历史K线"""
        return self.http.get_history_kline(codes, ktype, end_time, count, adjust)

    # WebSocket接口
    async def connect_ws(self):
        """连接WebSocket"""
        await self.ws.connect()

    async def disconnect_ws(self):
        """断开WebSocket连接"""
        await self.ws.disconnect()

    async def heartbeat(self):
        """5.1 发送心跳"""
        await self.ws.heartbeat()

    async def subscribe_snapshot(self, codes: List[str]):
        """5.2 订阅实时快照"""
        await self.ws.subscribe_snapshot(codes)

    async def unsubscribe_snapshot(self, codes: List[str]):
        """5.2 取消订阅实时快照"""
        await self.ws.unsubscribe_snapshot(codes)

    async def subscribe_trades(self, codes: List[str]):
        """5.3 订阅逐笔成交"""
        await self.ws.subscribe_trades(codes)

    async def unsubscribe_trades(self, codes: List[str]):
        """5.3 取消订阅逐笔成交"""
        await self.ws.unsubscribe_trades(codes)

    async def subscribe_depth(self, codes: List[str]):
        """5.4 订阅盘口数据"""
        await self.ws.subscribe_depth(codes)

    async def unsubscribe_depth(self, codes: List[str]):
        """5.4 取消订阅盘口数据"""
        await self.ws.unsubscribe_depth(codes)

    async def subscribe_kline(self, codes: List[str], ktype: int):
        """5.5 订阅K线数据"""
        await self.ws.subscribe_kline(codes, ktype)

    async def unsubscribe_kline(self, codes: List[str], ktype: int):
        """5.5 取消订阅K线数据"""
        await self.ws.unsubscribe_kline(codes, ktype)

    async def request_snapshot(self, codes: List[str]) -> List[QuoteSnapshot]:
        """5.6 请求实时快照"""
        return await self.ws.request_snapshot(codes)

    async def request_trades(self, codes: List[str], count: int = 1) -> List[TradeTick]:
        """5.7 请求逐笔成交"""
        return await self.ws.request_trades(codes, count)

    async def request_depth(self, codes: List[str]) -> List[MarketDepth]:
        """5.8 请求盘口数据"""
        return await self.ws.request_depth(codes)

    async def request_kline(self, codes: List[str], ktype: int, count: int) -> List[KLine]:
        """5.9 请求K线数据"""
        return await self.ws.request_kline(codes, ktype, count)

    async def request_history_kline(self, codes: List[str], ktype: int, end_time: int, count: int) -> List[KLine]:
        """5.10 请求历史K线"""
        return await self.ws.request_history_kline(codes, ktype, end_time, count)

    async def request_instrument_info(self, codes: List[str]) -> List[InstrumentInfo]:
        """5.11 请求品种基础信息"""
        return await self.ws.request_instrument_info(codes)

    def register_callback(self, data_type: str, callback):
        """注册数据回调"""
        self.ws.register_callback(data_type, callback)