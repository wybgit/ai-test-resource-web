#!/bin/bash
# AI Resources Database 生产环境部署脚本

set -e

echo "🚀 AI Resources Database - 生产环境部署"
echo "========================================"

# 检查Docker和Docker Compose
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 检查环境变量文件
if [ ! -f ".env.prod" ]; then
    echo "❌ 未找到.env.prod文件，请创建生产环境配置"
    echo "示例内容:"
    echo "MYSQL_ROOT_PASSWORD=your_root_password"
    echo "MYSQL_DATABASE=mydatabase"
    echo "MYSQL_USER=myuser"
    echo "MYSQL_PASSWORD=mypassword"
    exit 1
fi

# 加载环境变量
source .env.prod

echo "📋 部署配置:"
echo "   数据库: $MYSQL_DATABASE"
echo "   用户: $MYSQL_USER"
echo "   主机: $(hostname)"

# 创建必要的目录
echo "📁 创建目录结构..."
mkdir -p ../logs ../exports ssl

# 生成自签名SSL证书（如果不存在）
if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
    echo "🔐 生成SSL证书..."
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
        -subj "/C=CN/ST=State/L=City/O=Organization/CN=localhost"
fi

# 停止现有服务
echo "🛑 停止现有服务..."
docker-compose -f docker-compose.prod.yml down --remove-orphans

# 构建和启动服务
echo "🔨 构建和启动服务..."
docker-compose -f docker-compose.prod.yml up --build -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 健康检查
echo "🔍 健康检查..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ HTTP服务正常"
else
    echo "❌ HTTP服务异常"
fi

if curl -f -k https://localhost/health > /dev/null 2>&1; then
    echo "✅ HTTPS服务正常"
else
    echo "❌ HTTPS服务异常"
fi

# 显示服务状态
echo "📊 服务状态:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "🎉 部署完成!"
echo "📱 访问地址:"
echo "   HTTP:  http://localhost"
echo "   HTTPS: https://localhost"
echo ""
echo "🔧 管理命令:"
echo "   查看日志: docker-compose -f docker-compose.prod.yml logs -f"
echo "   停止服务: docker-compose -f docker-compose.prod.yml down"
echo "   重启服务: docker-compose -f docker-compose.prod.yml restart"