# QOS行情API Python SDK

[![PyPI version](https://img.shields.io/pypi/v/qos-api)](https://pypi.org/project/qos-api/)
[![Python versions](https://img.shields.io/pypi/pyversions/qos-api)](https://pypi.org/project/qos-api/)

官方Python SDK for [QOS行情API](https://qos.hk)，支持港股、美股、A股和加密货币的实时行情数据。

## 功能特性

- 完整实现所有7个HTTP接口和11个WebSocket命令
- 强类型检查（基于Pydantic）
- 同步HTTP客户端和异步WebSocket客户端
- 自动重连和心跳维护
- 完善的错误处理机制

## 安装

```bash
pip install qos-api
```

## 注册API KEY
[注册api key](https://qos.hk)

## 快速开始

### 初始化客户端
[注册api key](https://qos.hk)
```python
from qos_api import QOSClient

client = QOSClient(api_key="您的API_KEY")
```

### HTTP接口使用示例

#### 获取品种基础信息

```python
# 获取股票基础信息
info = client.get_instrument_info(["US:AAPL", "HK:00700", "SH:600519"])
print(info)
```

#### 获取实时行情快照

```python
# 获取实时行情
snapshot = client.get_snapshot(["US:TSLA", "HK:09988"])
print(snapshot)
```

#### 获取K线数据

```python
from qos_api.constants import KLineType

# 获取日K线
kline = client.get_kline(
    codes=["SH:600519"],
    ktype=KLineType.DAY.value,
    count=10
)
print(kline)
```

### WebSocket接口使用示例

#### 实时行情订阅
[注册api key](https://qos.hk)
```python
import asyncio
from qos_api import QOSClient

async def handle_snapshot(snapshot):
    print(f"行情更新: {snapshot}")

async def pull_snapshot_periodically(client):
    """每10秒主动请求一次快照"""
    try:
        while True:
            data = await client.request_snapshot(["US:AAPL"])
            print(f"手动拉取快照数据: {data}")
            await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("快照任务已取消")
        raise

async def main():
    client = QOSClient(api_key="您的API_KEY")
    client.register_callback("S", handle_snapshot)
    await client.connect_ws()
    await client.subscribe_snapshot(["US:AAPL", "HK:700"])

    # 启动后台任务
    snapshot_task = asyncio.create_task(pull_snapshot_periodically(client))

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("收到退出信号，正在清理...")
        snapshot_task.cancel()
        await asyncio.gather(snapshot_task, return_exceptions=True)
        await client.close()
        print("已优雅退出")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # 再次捕获，防止 asyncio.run 抛出错误
        print("主程序强制退出")

```

#### 请求实时数据
[注册api key](https://qos.hk)
```python
import asyncio
from qos_api import QOSClient
from qos_api.constants import KLineType

async def request_realtime_data():
    client = QOSClient(api_key="您的API_KEY")
    await client.connect_ws()
    
    # 请求实时行情
    snapshot = await client.request_snapshot(["US:AAPL"])
    print(snapshot)
    
    # 请求K线
    kline = await client.request_kline(
        codes=["HK:700"],
        ktype=KLineType.DAY.value,
        count=10
    )
    print(kline)

asyncio.run(request_realtime_data())
```

## 完整API参考

### HTTP接口

| 方法 | 描述 | 对应API |
|------|------|---------|
| `get_instrument_info(codes)` | 获取品种基础信息 | `GET /instrument-info` |
| `get_snapshot(codes)` | 获取实时行情快照 | `GET /snapshot` |
| `get_depth(codes)` | 获取盘口深度 | `GET /depth` |
| `get_trades(codes, count)` | 获取逐笔成交 | `GET /trade` |
| `get_kline(codes, ktype, count, adjust)` | 获取K线数据 | `GET /kline` |
| `get_history_kline(codes, ktype, end_time, count, adjust)` | 获取历史K线 | `GET /history` |

### WebSocket接口

#### 订阅管理

| 方法 | 描述 | 对应命令 |
|------|------|---------|
| `subscribe_snapshot(codes)` | 订阅实时快照 | `S` |
| `unsubscribe_snapshot(codes)` | 取消订阅快照 | `SC` |
| `subscribe_trades(codes)` | 订阅逐笔成交 | `T` |
| `unsubscribe_trades(codes)` | 取消订阅逐笔 | `TC` |
| `subscribe_depth(codes)` | 订阅盘口数据 | `D` |
| `unsubscribe_depth(codes)` | 取消订阅盘口 | `DC` |
| `subscribe_kline(codes, ktype)` | 订阅K线数据 | `K` |
| `unsubscribe_kline(codes, ktype)` | 取消订阅K线 | `KC` |

#### 数据请求

| 方法 | 描述 | 对应命令 |
|------|------|---------|
| `request_snapshot(codes)` | 请求实时快照 | `RS` |
| `request_trades(codes, count)` | 请求逐笔成交 | `RT` |
| `request_depth(codes)` | 请求盘口数据 | `RD` |
| `request_kline(codes, ktype, count)` | 请求K线数据 | `RK` |
| `request_history_kline(codes, ktype, end_time, count)` | 请求历史K线 | `RH` |
| `request_instrument_info(codes)` | 请求品种信息 | `RI` |

#### 连接管理

| 方法 | 描述 |
|------|------|
| `connect_ws()` | 建立WebSocket连接 |
| `disconnect_ws()` | 断开WebSocket连接 |
| `heartbeat()` | 发送心跳包 |
| `register_callback(data_type, callback)` | 注册数据回调 |

## 数据模型

所有返回数据都使用Pydantic模型，主要模型包括：

- `InstrumentInfo`: 品种基础信息
- `QuoteSnapshot`: 行情快照
- `MarketDepth`: 盘口深度
- `TradeTick`: 逐笔成交
- `KLine`: K线数据

## 错误处理

所有异常都继承自 `QOSAPIError`：

```python
from qos_api import QOSAPIError

try:
    data = client.get_snapshot(["US:AAPL"])
except QOSAPIError as e:
    print(f"API错误: {e.code} - {e.message}")
```

## 限制说明

1. 默认每个连接最多订阅10个品种
2. HTTP请求频率限制为每分钟10次
3. WebSocket消息间隔需大于1秒

## 技术支持

- 官网: [https://qos.hk](https://qos.hk)
- 邮箱: support@qos.hk
- Telegram: [@stock_quote_api](https://t.me/stock_quote_api)

## License

MIT