# 贡献指南

感谢您对AI Resources Database项目的关注！我们欢迎各种形式的贡献。

## 🤝 如何贡献

### 报告问题
- 使用GitHub Issues报告bug
- 提供详细的错误信息和复现步骤
- 包含系统环境信息

### 提出功能建议
- 在Issues中描述新功能需求
- 说明功能的使用场景和价值
- 提供设计思路或实现建议

### 提交代码
1. Fork项目到您的GitHub账户
2. 创建功能分支: `git checkout -b feature/new-feature`
3. 提交更改: `git commit -am 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 创建Pull Request

## 📋 开发规范

### 代码风格
- 使用Python PEP 8规范
- 函数和变量使用下划线命名
- 类名使用驼峰命名
- 添加适当的注释和文档字符串

### 提交信息
使用清晰的提交信息格式：
```
类型(范围): 简短描述

详细描述（可选）

相关Issue: #123
```

类型包括：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建或工具相关

### 测试要求
- 为新功能添加测试用例
- 确保所有测试通过
- 保持测试覆盖率

## 🧪 开发环境设置

### 1. 克隆项目
```bash
git clone <repository-url>
cd ai-test-resources/gradio_app
```

### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装依赖
```bash
make install
# 或
pip install -r requirements.txt
```

### 4. 配置数据库
```bash
cp .env.example .env
# 编辑.env文件配置数据库连接
```

### 5. 运行测试
```bash
make test
# 或
python tests/run_tests.py
```

### 6. 启动应用
```bash
make run
# 或
python app.py
```

## 🔧 开发工具

### 推荐的IDE设置
- **VS Code**: 安装Python扩展
- **PyCharm**: 配置Python解释器
- **Vim/Neovim**: 使用相关Python插件

### 有用的命令
```bash
# 代码格式化
make format

# 代码质量检查
make check

# 运行特定测试
python tests/run_tests.py database

# 查看日志
make logs

# 清理临时文件
make clean
```

## 📚 项目结构

```
gradio_app/
├── app.py              # 主应用
├── components.py       # UI组件
├── database.py         # 数据库操作
├── database_config.py  # 数据库配置
├── utils.py           # 工具函数
├── config.py          # 应用配置
├── tests/             # 测试文件
├── docker/            # Docker配置
├── deploy/            # 部署配置
└── docs/              # 文档
```

## 🎯 贡献重点

我们特别欢迎以下方面的贡献：

### 高优先级
- 🐛 Bug修复
- 📊 数据可视化功能
- 🔐 用户认证系统
- 📱 移动端适配

### 中优先级
- 🌍 国际化支持
- 📈 性能优化
- 🔌 插件系统
- 📧 通知功能

### 低优先级
- 🎨 UI美化
- 📝 文档完善
- 🧪 测试覆盖率提升
- 🔧 开发工具改进

## 📖 文档贡献

### 文档类型
- 用户文档：使用说明、教程
- 开发文档：API文档、架构说明
- 部署文档：安装、配置、运维

### 文档规范
- 使用Markdown格式
- 包含代码示例
- 添加截图说明
- 保持内容更新

## 🔍 代码审查

### 审查要点
- 功能正确性
- 代码质量
- 性能影响
- 安全考虑
- 文档完整性

### 审查流程
1. 自动化测试通过
2. 代码审查通过
3. 文档更新完成
4. 合并到主分支

## 🏆 贡献者认可

我们会在以下地方认可贡献者：
- README.md贡献者列表
- 发布说明
- 项目网站
- 社区活动

## 📞 联系方式

如有疑问，请通过以下方式联系：
- GitHub Issues
- 邮件：[联系邮箱]
- 社区讨论：[讨论链接]

## 📄 许可证

通过贡献代码，您同意您的贡献将在MIT许可证下发布。

---

再次感谢您的贡献！🎉