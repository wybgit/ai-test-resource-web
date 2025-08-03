"""
应用配置文件
Application configuration settings
"""
import os
from typing import Dict, Any

# 应用基本配置
APP_CONFIG = {
    "title": "AI Resources Database",
    "description": "智能资源数据库管理系统",
    "version": "1.0.0",
    "author": "AITest Team",
    "server_name": os.getenv("GRADIO_SERVER_NAME", "0.0.0.0"),
    "server_port": int(os.getenv("GRADIO_SERVER_PORT", "7860")),
    "debug": os.getenv("GRADIO_DEBUG", "true").lower() == "true",
    "share": os.getenv("GRADIO_SHARE", "false").lower() == "true"
}

# 界面配置
UI_CONFIG = {
    "theme": "soft",  # 可选: default, soft, monochrome
    "max_rows_per_page": 20,
    "enable_queue": True,
    "show_api": False,
    "show_error": True,
    "favicon_path": None,
    "css_paths": [],
    "js_paths": []
}

# 数据库配置
DB_CONFIG = {
    "connection_timeout": 30,
    "max_retries": 3,
    "retry_delay": 1,
    "pool_size": 5,
    "charset": "utf8mb4"
}

# 导出配置
EXPORT_CONFIG = {
    "max_export_rows": 10000,
    "supported_formats": ["csv", "excel", "json"],
    "csv_encoding": "utf-8-sig",
    "excel_engine": "openpyxl",
    "json_orient": "records"
}

# 日志配置
LOG_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file_path": "logs/app.log",
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

# 性能配置
PERFORMANCE_CONFIG = {
    "enable_monitoring": True,
    "cache_enabled": False,
    "cache_ttl": 300,  # 5分钟
    "max_concurrent_requests": 10
}

# 安全配置
SECURITY_CONFIG = {
    "enable_auth": False,
    "allowed_origins": ["*"],
    "max_request_size": 100 * 1024 * 1024,  # 100MB
    "rate_limit": {
        "enabled": False,
        "requests_per_minute": 60
    }
}

# 功能开关
FEATURE_FLAGS = {
    "enable_export": True,
    "enable_search": True,
    "enable_filtering": True,
    "enable_stats": True,
    "enable_system_monitor": True,
    "enable_performance_monitor": True
}

def get_config(section: str = None) -> Dict[str, Any]:
    """获取配置"""
    configs = {
        "app": APP_CONFIG,
        "ui": UI_CONFIG,
        "db": DB_CONFIG,
        "export": EXPORT_CONFIG,
        "log": LOG_CONFIG,
        "performance": PERFORMANCE_CONFIG,
        "security": SECURITY_CONFIG,
        "features": FEATURE_FLAGS
    }
    
    if section:
        return configs.get(section, {})
    
    return configs

def update_config(section: str, key: str, value: Any) -> bool:
    """更新配置"""
    try:
        configs = get_config()
        if section in configs and key in configs[section]:
            configs[section][key] = value
            return True
        return False
    except Exception:
        return False