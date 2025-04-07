class QOSError(Exception):
    """QOS API基础异常"""
    pass

class QOSAPIError(QOSError):
    """API业务逻辑异常"""
    def __init__(self, message: str, code: int = -1):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

class QOSHTTPError(QOSAPIError):
    """HTTP请求异常"""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code)
        self.status_code = status_code

class QOSWebSocketError(QOSAPIError):
    """WebSocket异常"""
    pass

class QOSLimitError(QOSAPIError):
    """访问限制异常"""
    pass