# AI Resources Database Gradio版本 Makefile

.PHONY: help install test run clean docker deploy

# 默认目标
help:
	@echo "🚀 AI Resources Database - Gradio版本"
	@echo "可用命令:"
	@echo "  install    - 安装依赖包"
	@echo "  test       - 运行测试"
	@echo "  run        - 启动应用"
	@echo "  clean      - 清理临时文件"
	@echo "  docker     - 构建Docker镜像"
	@echo "  deploy     - 部署到生产环境"
	@echo "  check      - 检查代码质量"
	@echo "  backup     - 备份数据"

# 安装依赖
install:
	@echo "📦 安装依赖包..."
	pip install -r requirements.txt
	@echo "✅ 依赖安装完成"

# 运行测试
test:
	@echo "🧪 运行测试套件..."
	python tests/run_tests.py
	@echo "✅ 测试完成"

# 测试数据库连接
test-db:
	@echo "🔍 测试数据库连接..."
	python test_connection.py

# 运行应用
run:
	@echo "🚀 启动应用..."
	python app.py

# 快速启动
start:
	@echo "⚡ 快速启动..."
	./start.sh

# 清理临时文件
clean:
	@echo "🧹 清理临时文件..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf exports/*.csv exports/*.xlsx exports/*.json 2>/dev/null || true
	rm -rf logs/*.log 2>/dev/null || true
	@echo "✅ 清理完成"

# 构建Docker镜像
docker:
	@echo "🐳 构建Docker镜像..."
	docker build -t ai-resources-gradio -f docker/Dockerfile .
	@echo "✅ Docker镜像构建完成"

# Docker Compose启动
docker-up:
	@echo "🐳 启动Docker Compose服务..."
	docker-compose -f docker/docker-compose.yml up -d
	@echo "✅ 服务启动完成"

# Docker Compose停止
docker-down:
	@echo "🛑 停止Docker Compose服务..."
	docker-compose -f docker/docker-compose.yml down
	@echo "✅ 服务停止完成"

# 生产环境部署
deploy:
	@echo "🚀 部署到生产环境..."
	cd deploy && ./deploy.sh
	@echo "✅ 部署完成"

# 代码质量检查
check:
	@echo "🔍 检查代码质量..."
	@if command -v flake8 >/dev/null 2>&1; then \
		echo "运行 flake8..."; \
		flake8 --max-line-length=100 --ignore=E501,W503 *.py; \
	else \
		echo "⚠️  flake8 未安装，跳过代码检查"; \
	fi
	@echo "✅ 代码检查完成"

# 格式化代码
format:
	@echo "🎨 格式化代码..."
	@if command -v black >/dev/null 2>&1; then \
		echo "运行 black..."; \
		black --line-length=100 *.py; \
	else \
		echo "⚠️  black 未安装，跳过代码格式化"; \
	fi
	@echo "✅ 代码格式化完成"

# 备份数据
backup:
	@echo "💾 备份数据..."
	@mkdir -p backups
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	if [ -d "exports" ]; then \
		tar -czf "backups/exports_$$timestamp.tar.gz" exports/; \
		echo "✅ 导出文件备份完成: backups/exports_$$timestamp.tar.gz"; \
	fi; \
	if [ -d "logs" ]; then \
		tar -czf "backups/logs_$$timestamp.tar.gz" logs/; \
		echo "✅ 日志文件备份完成: backups/logs_$$timestamp.tar.gz"; \
	fi
	@echo "✅ 备份完成"

# 恢复数据
restore:
	@echo "🔄 恢复数据..."
	@echo "请手动指定要恢复的备份文件"
	@ls -la backups/ 2>/dev/null || echo "❌ 未找到备份文件"

# 查看日志
logs:
	@echo "📝 查看应用日志..."
	@if [ -f "logs/app.log" ]; then \
		tail -f logs/app.log; \
	else \
		echo "❌ 日志文件不存在"; \
	fi

# 查看系统状态
status:
	@echo "📊 系统状态..."
	@echo "Python版本: $$(python --version)"
	@echo "工作目录: $$(pwd)"
	@echo "磁盘使用: $$(df -h . | tail -1 | awk '{print $$5}')"
	@if command -v docker >/dev/null 2>&1; then \
		echo "Docker版本: $$(docker --version)"; \
		echo "Docker容器状态:"; \
		docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "无运行中的容器"; \
	fi

# 更新依赖
update:
	@echo "🔄 更新依赖包..."
	pip install --upgrade -r requirements.txt
	@echo "✅ 依赖更新完成"

# 生成需求文件
freeze:
	@echo "📋 生成当前环境的依赖列表..."
	pip freeze > requirements_freeze.txt
	@echo "✅ 依赖列表已保存到 requirements_freeze.txt"

# 安全检查
security:
	@echo "🔒 安全检查..."
	@if command -v safety >/dev/null 2>&1; then \
		echo "运行 safety 检查..."; \
		safety check; \
	else \
		echo "⚠️  safety 未安装，跳过安全检查"; \
		echo "安装命令: pip install safety"; \
	fi
	@echo "✅ 安全检查完成"