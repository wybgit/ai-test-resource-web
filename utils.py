"""
工具函数模块
Utility functions for the Gradio application
"""
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def setup_logging():
    """设置日志系统"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # 添加文件处理器
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        file_handler = logging.FileHandler(os.path.join(log_dir, 'app.log'), encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
    
    logger.info("日志系统初始化完成")
    return logger

def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def validate_dataframe(df: pd.DataFrame) -> bool:
    """验证DataFrame是否有效"""
    if df is None or df.empty:
        return False
    return True

def sanitize_filename(filename: str) -> str:
    """清理文件名，移除非法字符"""
    import re
    # 移除或替换非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 限制长度
    if len(filename) > 200:
        filename = filename[:200]
    return filename

def get_table_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """获取表格摘要信息"""
    if not validate_dataframe(df):
        return {"rows": 0, "columns": 0, "memory_usage": "0B"}
    
    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "memory_usage": format_file_size(df.memory_usage(deep=True).sum()),
        "dtypes": df.dtypes.value_counts().to_dict()
    }
    
    return summary

def create_export_filename(table_name: str, export_format: str = "csv") -> str:
    """创建导出文件名"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{table_name}_{timestamp}.{export_format}"
    return sanitize_filename(filename)

def check_database_health() -> Dict[str, Any]:
    """检查数据库健康状态"""
    try:
        from database import db_manager
        
        # 测试连接
        connection = db_manager.get_connection()
        if connection:
            connection.close()
            
        # 测试查询
        test_query = "SELECT 1 as test"
        result = db_manager.execute_query(test_query)
        
        return {
            "status": "healthy",
            "connection": True,
            "query_test": len(result) > 0,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "connection": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def format_number(num: Any) -> str:
    """格式化数字显示"""
    if pd.isna(num) or num is None:
        return "N/A"
    
    try:
        num = float(num)
        if num >= 1e9:
            return f"{num/1e9:.1f}B"
        elif num >= 1e6:
            return f"{num/1e6:.1f}M"
        elif num >= 1e3:
            return f"{num/1e3:.1f}K"
        else:
            return f"{num:.1f}"
    except (ValueError, TypeError):
        return str(num)

def create_status_message(total: int, filtered: int, table_name: str) -> str:
    """创建状态消息"""
    if filtered == total:
        return f"📊 **{table_name}**: 显示全部 {total:,} 条数据"
    else:
        percentage = (filtered / total * 100) if total > 0 else 0
        return f"📊 **{table_name}**: 筛选显示 {filtered:,} 条 / 总计 {total:,} 条 ({percentage:.1f}%)"

def get_system_info() -> Dict[str, Any]:
    """获取系统信息"""
    import platform
    
    try:
        import psutil
        return {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": format_file_size(psutil.virtual_memory().total),
            "memory_available": format_file_size(psutil.virtual_memory().available),
            "disk_usage": format_file_size(psutil.disk_usage('.').free)
        }
    except ImportError:
        return {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "cpu_count": "N/A (psutil not installed)",
            "memory_total": "N/A (psutil not installed)",
            "memory_available": "N/A (psutil not installed)",
            "disk_usage": "N/A (psutil not installed)"
        }

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.start_time = None
        self.operations = []
    
    def start(self, operation_name: str):
        """开始监控操作"""
        self.start_time = datetime.now()
        self.current_operation = operation_name
    
    def end(self) -> float:
        """结束监控并返回耗时"""
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            self.operations.append({
                "operation": self.current_operation,
                "duration": duration,
                "timestamp": datetime.now().isoformat()
            })
            return duration
        return 0.0
    
    def get_stats(self) -> Dict[str, Any]:
        """获取性能统计"""
        if not self.operations:
            return {"total_operations": 0}
        
        durations = [op["duration"] for op in self.operations]
        return {
            "total_operations": len(self.operations),
            "avg_duration": sum(durations) / len(durations),
            "max_duration": max(durations),
            "min_duration": min(durations),
            "recent_operations": self.operations[-5:]  # 最近5次操作
        }

# 全局性能监控器实例
performance_monitor = PerformanceMonitor()