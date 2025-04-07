import time
from typing import Any, Dict, Optional
from .exceptions import QOSAPIError

def validate_codes(codes: list, max_count: int = 10) -> str:
    """验证并格式化品种代码
    
    Args:
        codes: 品种代码列表
        max_count: 最大允许数量
        
    Returns:
        格式化后的逗号分隔字符串
        
    Raises:
        QOSAPIError: 当超过最大数量限制时
    """
    if len(codes) > max_count:
        raise QOSAPIError(f"Max {max_count} codes allowed per request")
    return ",".join(codes)

def current_timestamp() -> int:
    """获取当前时间戳（秒级）"""
    return int(time.time())

def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """解析API响应
    
    Args:
        response: 原始API响应
        
    Returns:
        解析后的数据字典
        
    Raises:
        QOSAPIError: 当响应包含错误时
    """
    if response.get("msg") != "OK":
        raise QOSAPIError(response.get("msg", "Unknown error"))
    return response.get("data", {})

def build_kline_request(
    codes: list,
    ktype: int,
    count: int,
    adjust: int = 0,
    end_time: Optional[int] = None
) -> Dict[str, Any]:
    """构建K线请求参数
    
    Args:
        codes: 品种代码列表
        ktype: K线类型
        count: 请求数量
        adjust: 复权类型 (0: 不复权, 1: 前复权)
        end_time: 结束时间戳（历史K线需要）
        
    Returns:
        构造好的请求参数字典
    """
    req = {
        "c": validate_codes(codes),
        "kt": ktype,
        "co": count,
        "a": adjust
    }
    if end_time is not None:
        req["e"] = end_time
    return {"kline_reqs": [req]}