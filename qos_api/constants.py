from enum import Enum

class Market(Enum):
    US = "US"  # 美股
    HK = "HK"  # 港股
    SH = "SH"  # 沪市
    SZ = "SZ"  # 深市
    CF = "CF"  # 加密货币

class KLineType(Enum):
    MIN1 = 1     # 1分钟
    MIN5 = 5     # 5分钟
    MIN15 = 15   # 15分钟
    MIN30 = 30   # 30分钟
    HOUR1 = 60   # 1小时
    HOUR2 = 120  # 2小时
    HOUR4 = 240  # 4小时
    DAY = 1001   # 日线
    WEEK = 1007  # 周线
    MONTH = 1030 # 月线
    YEAR = 2001  # 年线

class TradeDirection(Enum):
    UNKNOWN = 0
    BUY = 1
    SELL = 2

class USSessionType(Enum):
    UNKNOWN = 0
    NIGHT = 1      # 夜盘
    PRE_MARKET = 2 # 盘前
    INTRADAY = 3   # 盘中
    AFTER_HOURS = 4# 盘后

class WSType(Enum):
    SNAPSHOT = "S"       # 快照订阅
    SNAPSHOT_CANCEL = "SC"
    TRADE = "T"          # 逐笔订阅
    TRADE_CANCEL = "TC"
    DEPTH = "D"          # 盘口订阅
    DEPTH_CANCEL = "DC"
    KLINE = "K"          # K线订阅
    KLINE_CANCEL = "KC"
    REQ_SNAPSHOT = "RS"  # 请求快照
    REQ_TRADE = "RT"     # 请求逐笔
    REQ_DEPTH = "RD"     # 请求盘口
    REQ_KLINE = "RK"     # 请求K线
    REQ_HISTORY = "RH"   # 请求历史K线
    REQ_INFO = "RI"      # 请求基础信息
    HEARTBEAT = "H"      # 心跳

BASE_URL = "https://api.qos.hk"
WS_URL = "wss://api.qos.hk/ws"
MAX_SUB_CODES = 10  # 默认最大订阅品种数