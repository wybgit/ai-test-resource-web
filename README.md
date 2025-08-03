# AI Resources Database - Gradio版本

基于Gradio构建的现代化数据库查询和管理系统，提供直观的Web界面用于查看和管理AI资源数据。

## 🌟 功能特性

### 📊 数据集管理
- 查看图像数据集索引信息
- 支持按正向目标、负向目标、目标距离等条件筛选
- 实时统计显示当前筛选结果

### 🤖 测试用例管理  
- 管理AI模型测试用例
- 支持按类别、标签、框架等条件筛选
- 详细的模型信息展示

### 🔍 智能搜索
- 全局关键词搜索，覆盖所有字段
- 多条件组合筛选
- 实时搜索结果更新

### 📥 数据导出
- 一键导出当前筛选结果为CSV格式
- 支持中文文件名和内容
- 自动添加时间戳

### 🎨 用户界面
- 现代化响应式设计
- 直观的标签页布局
- 清晰的数据统计信息
- 友好的错误提示

## 🚀 快速开始

### 1. 环境准备

确保已安装Python 3.8+和MySQL 8.0+

### 2. 安装依赖

```bash
cd gradio_app
pip install -r requirements.txt
```

### 3. 数据库配置

在项目根目录创建`.env`文件：

```bash
# MySQL数据库连接配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=mydatabase
MYSQL_USER=myuser
MYSQL_PASSWORD=mypassword
```

### 4. 启动应用

```bash
python app.py
```

应用将在 http://localhost:7860 启动

## 📁 项目结构

```
gradio_app/
├── app.py                 # 主应用文件
├── components.py          # UI组件模块
├── database.py           # 数据库操作模块
├── database_config.py    # 数据库配置
├── requirements.txt      # 依赖包列表
├── exports/             # CSV导出文件目录
└── README.md            # 项目说明
```

## 🔧 配置说明

### 数据库配置

`database_config.py`文件包含：
- 数据库连接参数
- 表结构配置
- 字段中文映射
- 筛选选项配置

### 表配置

支持两个主要数据表：
- `dataset_index`: 数据集索引表
- `test_cases`: 测试用例表

每个表都配置了：
- 中文列名映射
- 可筛选字段选项
- 主键字段定义

## 🎯 使用指南

### 数据集管理
1. 点击"📊 数据集索引"标签页
2. 使用左侧筛选器选择条件
3. 或使用全局搜索框输入关键词
4. 查看右侧数据表格和统计信息
5. 点击"📥 导出CSV"下载数据

### 测试用例管理
1. 点击"🤖 测试用例"标签页
2. 按类别、标签、框架等条件筛选
3. 查看模型详细信息
4. 导出筛选结果

### 筛选技巧
- 多个筛选条件会进行AND组合
- 同一筛选器内的多个选项进行OR组合
- 全局搜索会覆盖所有字段
- 使用"🔄 重置所有筛选"清空条件

## 🔍 故障排除

### 数据库连接问题
1. 检查MySQL服务是否运行
2. 验证`.env`文件中的连接参数
3. 确认数据库和表是否存在
4. 检查用户权限设置

### 应用启动问题
1. 确认Python版本>=3.8
2. 检查依赖包是否完整安装
3. 查看控制台错误信息
4. 确认端口7860未被占用

### 数据显示问题
1. 检查表结构是否与配置匹配
2. 验证字段名映射是否正确
3. 确认数据编码格式

## 🔄 与原版对比

| 功能 | React版本 | Gradio版本 |
|------|-----------|------------|
| 数据筛选 | ✅ | ✅ |
| 全局搜索 | ✅ | ✅ |
| 数据导出 | ✅ | ✅ |
| 响应式设计 | ✅ | ✅ |
| 实时统计 | ✅ | ✅ |
| 列宽调整 | ✅ | ❌ |
| 列显示控制 | ✅ | ❌ |
| 行选择 | ✅ | ❌ |
| 部署复杂度 | 高 | 低 |
| 开发速度 | 慢 | 快 |

## 🚀 部署方式

### 开发环境
```bash
# 方式1: 直接运行
python app.py

# 方式2: 使用启动脚本
./start.sh

# 方式3: 使用快速启动
python run.py
```

### Docker部署
```bash
# 单容器部署
docker build -t ai-resources-gradio -f docker/Dockerfile .
docker run -d -p 7860:7860 ai-resources-gradio

# Docker Compose部署（推荐）
docker-compose -f docker/docker-compose.yml up -d
```

### 生产环境
```bash
# 使用生产环境配置
cd deploy
./deploy.sh
```

详细部署说明请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

## 📝 更新日志

### v1.0.0 (2025-02-08)
- ✨ 初始版本发布
- 📊 支持数据集索引管理
- 🤖 支持测试用例管理
- 🔍 实现全局搜索和多条件筛选
- 📥 支持CSV数据导出
- 🎨 现代化UI设计

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

本项目采用MIT许可证。