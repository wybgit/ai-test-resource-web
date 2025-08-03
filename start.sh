#!/bin/bash
# AI Resources Database Gradio版本启动脚本

echo "🚀 AI Resources Database - Gradio版本"
echo "======================================"

# 检查Python版本
python_version=$(python3 --version 2>&1)
echo "🐍 Python版本: $python_version"

# 检查是否存在虚拟环境
if [ -d "venv" ]; then
    echo "📦 激活虚拟环境..."
    source venv/bin/activate
elif [ -d "../venv" ]; then
    echo "📦 激活虚拟环境..."
    source ../venv/bin/activate
else
    echo "⚠️  未找到虚拟环境，使用系统Python"
fi

# 检查.env文件
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "⚠️  未找到.env文件，请复制.env.example并配置数据库连接"
        echo "   命令: cp .env.example .env"
        echo "   然后编辑.env文件填入正确的数据库信息"
        exit 1
    else
        echo "⚠️  未找到配置文件，将使用默认配置"
    fi
fi

# 检查依赖
echo "🔍 检查依赖包..."
if ! python3 -c "import gradio" 2>/dev/null; then
    echo "❌ Gradio未安装，正在安装依赖..."
    pip install -r requirements.txt
fi

# 运行连接测试
echo "🔍 运行连接测试..."
python3 test_connection.py

if [ $? -eq 0 ]; then
    echo "✅ 连接测试通过，启动应用..."
    python3 app.py
else
    echo "⚠️  连接测试失败，但仍将启动应用"
    echo "💡 应用可能无法正常显示数据，请检查数据库配置"
    read -p "是否继续启动？(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 app.py
    else
        echo "❌ 启动已取消"
        exit 1
    fi
fi