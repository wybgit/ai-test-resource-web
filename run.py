#!/usr/bin/env python3
"""
快速启动脚本
Quick start script for AI Resources Database Gradio App
"""
import os
import sys
from pathlib import Path

def setup_environment():
    """设置环境"""
    # 添加当前目录到Python路径
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    # 检查.env文件
    env_file = current_dir / ".env"
    env_example = current_dir / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        print("⚠️  未找到.env文件，请根据.env.example创建配置文件")
        print(f"   示例: cp {env_example} {env_file}")
        print("   然后编辑.env文件填入正确的数据库连接信息")
        return False
    
    return True

def main():
    """主函数"""
    print("🚀 AI Resources Database - Gradio版本")
    print("=" * 50)
    
    if not setup_environment():
        sys.exit(1)
    
    try:
        from app import main as app_main
        app_main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 请确保已安装所有依赖: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()