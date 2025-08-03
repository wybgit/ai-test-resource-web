# API 文档

AI Resources Database Gradio版本的API接口文档。

## 📋 概述

本应用基于Gradio框架构建，提供Web界面和后端API接口。虽然主要通过Web界面使用，但也可以通过编程方式调用核心功能。

## 🔧 核心模块API

### 数据库管理器 (DatabaseManager)

#### 初始化
```python
from database import db_manager
```

#### 方法列表

##### get_connection()
获取数据库连接
```python
connection = db_manager.get_connection()
```
**返回**: MySQL连接对象

##### get_all_data(table_name: str)
获取表的所有数据
```python
df = db_manager.get_all_data("dataset_index")
```
**参数**:
- `table_name`: 表名 ("dataset_index" 或 "test_cases")

**返回**: pandas.DataFrame

##### filter_data(table_name: str, filters: Dict[str, List[str]])
根据筛选条件获取数据
```python
filters = {"正向目标": ["行人", "车辆"]}
df = db_manager.filter_data("dataset_index", filters)
```
**参数**:
- `table_name`: 表名
- `filters`: 筛选条件字典

**返回**: pandas.DataFrame

##### search_data(table_name: str, search_text: str)
全局搜索数据
```python
df = db_manager.search_data("dataset_index", "urban")
```
**参数**:
- `table_name`: 表名
- `search_text`: 搜索关键词

**返回**: pandas.DataFrame

##### get_table_stats(table_name: str, filters: Optional[Dict])
获取表统计信息
```python
total, filtered = db_manager.get_table_stats("dataset_index")
```
**参数**:
- `table_name`: 表名
- `filters`: 可选的筛选条件

**返回**: Tuple[int, int] (总数, 筛选后数量)

##### export_to_csv(df: pd.DataFrame, filename: str)
导出数据为CSV
```python
path = db_manager.export_to_csv(df, "export.csv")
```

##### export_to_excel(df: pd.DataFrame, filename: str)
导出数据为Excel
```python
path = db_manager.export_to_excel(df, "export.xlsx")
```

##### export_to_json(df: pd.DataFrame, filename: str)
导出数据为JSON
```python
path = db_manager.export_to_json(df, "export.json")
```

### 组件模块 (Components)

#### 创建筛选界面
```python
from components import create_filter_interface

components = create_filter_interface("dataset_index")
```

#### 更新数据显示
```python
from components import update_data_display

df, stats, file = update_data_display(
    "dataset_index", 
    search_text="test",
    filter_正向目标=["行人"]
)
```

#### 导出数据
```python
from components import export_data

file = export_data("dataset_index", df, "csv")
```

### 工具模块 (Utils)

#### 性能监控
```python
from utils import performance_monitor

performance_monitor.start("operation_name")
# ... 执行操作 ...
duration = performance_monitor.end()
```

#### 系统信息
```python
from utils import get_system_info, check_database_health

sys_info = get_system_info()
db_health = check_database_health()
```

## 🌐 Web API接口

虽然这是一个Gradio应用，但您可以通过HTTP请求与某些功能交互。

### 健康检查
```http
GET /health
```
**响应**: 
```json
{
  "status": "healthy",
  "timestamp": "2025-02-08T10:00:00Z"
}
```

### 获取应用信息
```http
GET /info
```
**响应**:
```json
{
  "name": "AI Resources Database",
  "version": "1.0.0",
  "description": "智能资源数据库管理系统"
}
```

## 📊 数据模型

### 数据集索引 (dataset_index)

| 字段名 | 类型 | 描述 |
|--------|------|------|
| image_id | int | 图像ID (主键) |
| image_name | varchar(255) | 图像名称 |
| image_height | int | 图像高度 |
| image_width | int | 图像宽度 |
| image_repository | varchar(255) | 图像仓库 |
| bmp_path | varchar(255) | BMP文件路径 |
| yuv_path | varchar(255) | YUV文件路径 |
| json_path | varchar(255) | JSON文件路径 |
| positive_target | set | 正向目标 |
| negative_target | set | 负向目标 |
| target_distance | set | 目标距离 |
| source | varchar(100) | 数据来源 |

### 测试用例 (test_cases)

| 字段名 | 类型 | 描述 |
|--------|------|------|
| case_id | int | 用例ID (主键) |
| case_name | varchar(255) | 用例名称 |
| case_repository | varchar(255) | 用例仓库 |
| case_path | varchar(500) | 用例路径 |
| case_json_path | varchar(500) | JSON配置路径 |
| category | enum | 类别 |
| label | set | 标签 |
| framework | enum | 框架 |
| input_shape | varchar(100) | 输入形状 |
| model_size | decimal(10,2) | 模型大小(MB) |
| params | bigint | 参数量 |
| flops | bigint | FLOPs |
| sources | varchar(255) | 来源 |
| update_time | timestamp | 更新时间 |
| remark | text | 备注 |

## 🔧 配置API

### 获取配置
```python
from config import get_config

# 获取所有配置
all_config = get_config()

# 获取特定配置
app_config = get_config("app")
db_config = get_config("db")
```

### 更新配置
```python
from config import update_config

success = update_config("app", "debug", False)
```

## 📝 使用示例

### 基本数据查询
```python
from database import db_manager

# 获取所有数据集
datasets = db_manager.get_all_data("dataset_index")
print(f"共有 {len(datasets)} 个数据集")

# 筛选包含"行人"的数据集
filters = {"正向目标": ["行人"]}
filtered_datasets = db_manager.filter_data("dataset_index", filters)
print(f"包含行人的数据集: {len(filtered_datasets)} 个")

# 搜索特定关键词
search_results = db_manager.search_data("dataset_index", "urban")
print(f"搜索'urban'的结果: {len(search_results)} 个")
```

### 数据导出
```python
import pandas as pd
from database import db_manager

# 获取数据
df = db_manager.get_all_data("test_cases")

# 导出为不同格式
csv_path = db_manager.export_to_csv(df, "test_cases.csv")
excel_path = db_manager.export_to_excel(df, "test_cases.xlsx")
json_path = db_manager.export_to_json(df, "test_cases.json")

print(f"数据已导出到:")
print(f"  CSV: {csv_path}")
print(f"  Excel: {excel_path}")
print(f"  JSON: {json_path}")
```

### 性能监控
```python
from utils import performance_monitor
from database import db_manager

# 监控数据库查询性能
performance_monitor.start("database_query")
df = db_manager.get_all_data("dataset_index")
duration = performance_monitor.end()

print(f"查询耗时: {duration:.2f}秒")

# 获取性能统计
stats = performance_monitor.get_stats()
print(f"总操作数: {stats['total_operations']}")
print(f"平均耗时: {stats.get('avg_duration', 0):.2f}秒")
```

## 🚨 错误处理

### 常见错误类型

#### 数据库连接错误
```python
try:
    connection = db_manager.get_connection()
except mysql.connector.Error as e:
    print(f"数据库连接失败: {e}")
```

#### 数据查询错误
```python
try:
    df = db_manager.get_all_data("invalid_table")
except Exception as e:
    print(f"查询失败: {e}")
```

#### 文件导出错误
```python
try:
    path = db_manager.export_to_csv(df, "export.csv")
    if not path:
        print("导出失败")
except Exception as e:
    print(f"导出错误: {e}")
```

## 📚 扩展开发

### 添加新的数据表支持

1. **更新数据库配置**
```python
# 在 database_config.py 中添加新表配置
TABLE_CONFIG["new_table"] = {
    "name": "新表名",
    "primary_key": "id",
    "columns": {
        "id": "ID",
        "name": "名称"
    }
}
```

2. **创建对应的UI组件**
```python
# 在 components.py 中添加新的标签页
def create_new_table_tab():
    # 实现新表的UI逻辑
    pass
```

3. **更新主应用**
```python
# 在 app.py 中添加新标签页
new_tab = create_new_table_tab()
```

### 添加新的导出格式

```python
# 在 database.py 中添加新的导出方法
def export_to_xml(self, df: pd.DataFrame, filename: str) -> str:
    """导出为XML格式"""
    try:
        xml_path = f"exports/{filename}"
        df.to_xml(xml_path)
        return xml_path
    except Exception as e:
        logger.error(f"导出XML失败: {e}")
        return ""
```

## 🔒 安全注意事项

1. **SQL注入防护**: 所有数据库查询都使用参数化查询
2. **输入验证**: 对用户输入进行严格验证
3. **文件路径安全**: 限制文件操作在指定目录内
4. **错误信息**: 避免在错误信息中泄露敏感信息

## 📞 技术支持

如需API相关的技术支持，请：
1. 查看相关源代码和注释
2. 运行测试用例验证功能
3. 提交Issue描述问题
4. 参考示例代码

---

**API版本**: v1.0.0  
**最后更新**: 2025-02-08  
**兼容性**: Python 3.8+, Gradio 4.0+