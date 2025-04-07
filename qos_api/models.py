from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class BaseResponse(BaseModel):
    msg: str = "OK"
    code: int = 0

class InstrumentInfo(BaseModel):
    c: str   # 股票代码
    e: Optional[str] = None  # 交易所
    tc: Optional[str] = None # 交易币种
    nc: Optional[str] = None # 中文名
    ne: Optional[str] = None # 英文名
    ls: Optional[int] = None # 最小交易单位
    ts: Optional[int] = None # 总股本
    os: Optional[int] = None # 流通股本
    ep: Optional[str] = None # 每股盈利
    na: Optional[str] = None # 每股净资产
    dy: Optional[str] = None # 股息率

class PeriodQuote(BaseModel):
    lp: str  # 最新价
    yp: str  # 昨收价
    h: str   # 最高价
    l: str   # 最低价
    ts: int  # 时间戳
    v: str   # 成交量
    t: str   # 成交额

class QuoteSnapshot(BaseModel):
    c: str   # 股票代码
    lp: str  # 最新价
    yp: Optional[str] = None  # 昨收价
    o: str   # 开盘价
    h: str   # 最高价
    l: str   # 最低价
    ts: int  # 时间戳
    v: str   # 成交量
    t: str   # 成交额
    s: int   # 停牌状态
    tt: Optional[int] = None  # 美股交易时段
    pq: Optional[PeriodQuote] = None # 盘前数据
    aq: Optional[PeriodQuote] = None # 盘后数据
    nq: Optional[PeriodQuote] = None # 夜盘数据

class DepthData(BaseModel):
    p: str  # 价格
    v: str  # 数量

class MarketDepth(BaseModel):
    c: str               # 股票代码
    b: List[DepthData]   # 买盘
    a: List[DepthData]   # 卖盘
    ts: int              # 时间戳

class TradeTick(BaseModel):
    c: str   # 股票代码
    p: str   # 价格
    v: str   # 成交量
    ts: int  # 时间戳
    d: int   # 交易方向

class KLine(BaseModel):
    c: str   # 股票代码
    o: str   # 开盘价
    cl: str  # 收盘价
    h: str   # 最高价
    l: str   # 最低价
    v: str   # 成交量
    ts: int  # 时间戳
    kt: int  # K线类型

class KLineResponse(BaseModel):
    c: str
    k: List[KLine]

class WSRequest(BaseModel):
    type: str  # 请求类型
    codes: Optional[List[str]] = None
    kline_reqs: Optional[List[Dict]] = None
    count: Optional[int] = None
    kt: Optional[int] = None
    a: Optional[int] = None
    e: Optional[int] = None
    reqid: Optional[int] = None

class WSResponse(BaseResponse):
    type: str
    reqid: Optional[int] = None
    time: Optional[int] = None
    data: Optional[List[Dict]] = None