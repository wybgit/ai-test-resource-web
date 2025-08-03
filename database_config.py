"""
数据库配置文件
Database configuration for Gradio app
"""
import os
from typing import Dict, Any

# 数据库连接配置
DATABASE_CONFIG: Dict[str, Any] = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "database": os.getenv("MYSQL_DATABASE", "mydatabase"),
    "user": os.getenv("MYSQL_USER", "myuser"),
    "password": os.getenv("MYSQL_PASSWORD", "mypassword"),
    "auth_plugin": "mysql_native_password",
    "charset": "utf8mb4",
    "autocommit": True
}

# 表配置
TABLE_CONFIG = {
    "dataset_index": {
        "name": "数据集索引",
        "primary_key": "image_id",
        "columns": {
            "image_id": "图像ID",
            "image_name": "图像名称", 
            "image_height": "高度",
            "image_width": "宽度",
            "image_repository": "仓库",
            "bmp_path": "BMP路径",
            "yuv_path": "YUV路径", 
            "json_path": "JSON路径",
            "positive_target": "正向目标",
            "negative_target": "负向目标",
            "target_distance": "目标距离",
            "source": "来源"
        },
        "filter_columns": {
            "positive_target": ["行人", "车辆", "建筑", "动物", "基础设施"],
            "negative_target": ["天空", "植被", "水面", "路面", "背景"],
            "target_distance": ["10m", "15m", "20m", "25m", "30m"]
        }
    },
    "test_cases": {
        "name": "测试用例",
        "primary_key": "case_id",
        "columns": {
            "case_id": "用例ID",
            "case_name": "用例名称",
            "case_repository": "仓库",
            "case_path": "路径",
            "case_json_path": "JSON路径",
            "category": "类别",
            "label": "标签",
            "framework": "框架",
            "input_shape": "输入形状",
            "model_size": "模型大小(MB)",
            "params": "参数量",
            "flops": "FLOPs",
            "sources": "来源",
            "update_time": "更新时间",
            "remark": "备注"
        },
        "filter_columns": {
            "category": ["单算子", "级联算子", "block块", "模型"],
            "label": ["depth fusion", "fusion", "M2M", "tiling"],
            "framework": ["onnx", "caffe", "ir"]
        }
    }
}