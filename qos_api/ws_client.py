import asyncio
import json
import logging
import websockets
from typing import Callable, Awaitable, Optional, List, Dict, Any
from .models import *
from .exceptions import QOSAPIError
from .constants import WS_URL, WSType, MAX_SUB_CODES

class QOSWebSocketClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.ws_url = f"{WS_URL}?key={api_key}"
        self.websocket = None
        self._req_counter = 0
        self._callbacks = {
            WSType.SNAPSHOT.value: [],   # 快照回调
            WSType.TRADE.value: [],      # 逐笔回调
            WSType.DEPTH.value: [],      # 盘口回调
            WSType.KLINE.value: []       # K线回调
        }
        self._pending_requests = {}
        self._running = False

    async def connect(self):
        """建立WebSocket连接"""
        if self.websocket is None:
            self.websocket = await websockets.connect(
                self.ws_url,
                ping_interval=20,
                ping_timeout=60,
                close_timeout=1
            )
            self._running = True
            asyncio.create_task(self._listen_messages())
            asyncio.create_task(self._send_heartbeat_loop())  # 启动心跳协程

    async def _send_heartbeat_loop(self):
        """每隔20秒发送一次心跳"""
        while self._running and self.websocket:
            try:
                await self.heartbeat()
                await asyncio.sleep(20)
            except Exception as e:
                logging.warning(f"Heartbeat error: {e}")
                await asyncio.sleep(5)  # 等待后继续尝试
    async def disconnect(self):
        """断开连接"""
        self._running = False
        if self.websocket:
            await self.websocket.close()
            self.websocket = None

    async def _listen_messages(self):
        """持续监听消息"""
        while self._running and self.websocket:
            try:
                message = await self.websocket.recv()
                data = json.loads(message)
                
                # 处理心跳响应
                if data.get("type") == WSType.HEARTBEAT.value:
                    continue
                    
                # 处理请求响应
                reqid = data.get("reqid")
                if reqid and reqid in self._pending_requests:
                    self._pending_requests[reqid].set_result(data)
                    del self._pending_requests[reqid]
                    continue
                
                # 处理数据推送
                tp = data.get("tp")
                if tp in self._callbacks:
                    model = self._get_data_model(tp)
                    for callback in self._callbacks[tp]:
                        try:
                            await callback(model(**data))
                        except Exception as e:
                            logging.error(f"Callback error: {str(e)}")

            except websockets.exceptions.ConnectionClosed:
                logging.warning("WebSocket connection closed")
                await self._reconnect()
            except Exception as e:
                logging.error(f"WebSocket error: {str(e)}")
                await self._reconnect()

    async def _reconnect(self):
        """重新连接"""
        await self.disconnect()
        await asyncio.sleep(1)
        await self.connect()

    def _get_data_model(self, tp: str):
        """获取对应的数据模型"""
        models = {
            WSType.SNAPSHOT.value: QuoteSnapshot,
            WSType.TRADE.value: TradeTick,
            WSType.DEPTH.value: MarketDepth,
            WSType.KLINE.value: KLine
        }
        return models.get(tp, dict)

    async def _send_request(self, request: Dict) -> Dict:
        """发送请求并等待响应"""
        if not self.websocket:
            await self.connect()
            
        reqid = self._req_counter = (self._req_counter + 1) % 10000
        request["reqid"] = reqid
        
        # 创建Future对象存储响应
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        self._pending_requests[reqid] = future
        
        await self.websocket.send(json.dumps(request))
        
        # 等待响应或超时
        try:
            return await asyncio.wait_for(future, timeout=10)
        except asyncio.TimeoutError:
            del self._pending_requests[reqid]
            raise QOSAPIError("Request timeout")

    async def heartbeat(self):
        """5.1 发送心跳"""
        await self.websocket.send(json.dumps({"type": WSType.HEARTBEAT.value}))

    async def subscribe_snapshot(self, codes: List[str]):
        """5.2 订阅实时快照"""
        if len(codes) > MAX_SUB_CODES:
            raise QOSAPIError(f"Max subscription count is {MAX_SUB_CODES}")
        await self._send_request({
            "type": WSType.SNAPSHOT.value,
            "codes": codes
        })

    async def unsubscribe_snapshot(self, codes: List[str]):
        """5.2 取消订阅实时快照"""
        await self._send_request({
            "type": WSType.SNAPSHOT_CANCEL.value,
            "codes": codes
        })

    async def subscribe_trades(self, codes: List[str]):
        """5.3 订阅逐笔成交"""
        if len(codes) > MAX_SUB_CODES:
            raise QOSAPIError(f"Max subscription count is {MAX_SUB_CODES}")
        await self._send_request({
            "type": WSType.TRADE.value,
            "codes": codes
        })

    async def unsubscribe_trades(self, codes: List[str]):
        """5.3 取消订阅逐笔成交"""
        await self._send_request({
            "type": WSType.TRADE_CANCEL.value,
            "codes": codes
        })

    async def subscribe_depth(self, codes: List[str]):
        """5.4 订阅盘口数据"""
        if len(codes) > MAX_SUB_CODES:
            raise QOSAPIError(f"Max subscription count is {MAX_SUB_CODES}")
        await self._send_request({
            "type": WSType.DEPTH.value,
            "codes": codes
        })

    async def unsubscribe_depth(self, codes: List[str]):
        """5.4 取消订阅盘口数据"""
        await self._send_request({
            "type": WSType.DEPTH_CANCEL.value,
            "codes": codes
        })

    async def subscribe_kline(self, codes: List[str], ktype: int):
        """5.5 订阅K线数据"""
        if len(codes) > MAX_SUB_CODES:
            raise QOSAPIError(f"Max subscription count is {MAX_SUB_CODES}")
        await self._send_request({
            "type": WSType.KLINE.value,
            "codes": codes,
            "kt": ktype
        })

    async def unsubscribe_kline(self, codes: List[str], ktype: int):
        """5.5 取消订阅K线数据"""
        await self._send_request({
            "type": WSType.KLINE_CANCEL.value,
            "codes": codes,
            "kt": ktype
        })

    async def request_snapshot(self, codes: List[str]) -> List[QuoteSnapshot]:
        """5.6 请求实时快照"""
        response = await self._send_request({
            "type": WSType.REQ_SNAPSHOT.value,
            "codes": codes
        })
        return [QuoteSnapshot(**item) for item in response.get("data", [])]

    async def request_trades(self, codes: List[str], count: int = 1) -> List[TradeTick]:
        """5.7 请求逐笔成交"""
        response = await self._send_request({
            "type": WSType.REQ_TRADE.value,
            "codes": codes,
            "count": min(count, 50)
        })
        return [TradeTick(**item) for item in response.get("data", [])]

    async def request_depth(self, codes: List[str]) -> List[MarketDepth]:
        """5.8 请求盘口数据"""
        response = await self._send_request({
            "type": WSType.REQ_DEPTH.value,
            "codes": codes
        })
        return [MarketDepth(**item) for item in response.get("data", [])]

    async def request_kline(self, codes: List[str], ktype: int, count: int) -> List[KLine]:
        """5.9 请求K线数据"""
        response = await self._send_request({
            "type": WSType.REQ_KLINE.value,
            "kline_reqs": [{
                "c": code,
                "kt": ktype,
                "co": count,
                "a": 0
            }
            for code in codes
            ]
        })
        results = []
        for item in response.get("data", []):
            results.extend([KLine(**k) for k in item.get("k", [])])
        return results

    async def request_history_kline(self, codes: List[str], ktype: int, end_time: int, count: int) -> List[KLine]:
        """5.10 请求历史K线"""
        response = await self._send_request({
            "type": WSType.REQ_HISTORY.value,
            "kline_reqs": [{
                "c": code,
                "kt": ktype,
                "e": end_time,
                "co": count,
                "a": 0
            }
            for code in codes
            ]
        })
        results = []
        for item in response.get("data", []):
            results.extend([KLine(**k) for k in item.get("k", [])])
        return results

    async def request_instrument_info(self, codes: List[str]) -> List[InstrumentInfo]:
        """5.11 请求品种基础信息"""
        response = await self._send_request({
            "type": WSType.REQ_INFO.value,
            "codes": codes
        })
        return [InstrumentInfo(**item) for item in response.get("data", [])]

    def register_callback(self, data_type: str, callback: Callable[[BaseModel], Awaitable[None]]):
        """注册数据回调函数"""
        if data_type in self._callbacks:
            self._callbacks[data_type].append(callback)
        else:
            raise ValueError(f"Unsupported data type: {data_type}")