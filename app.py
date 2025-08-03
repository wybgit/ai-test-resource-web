"""
AI Resources Database - Gradio版本
基于Gradio的数据库查询和管理系统
"""
import gradio as gr
import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from components import create_dataset_tab, create_models_tab
from database import db_manager
from utils import setup_logging, check_database_health, get_system_info

# 创建必要的目录
os.makedirs("exports", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# 设置日志
logger = setup_logging()

def create_app():
    """创建Gradio应用"""
    
    # 自定义CSS样式
    custom_css = """
    .gradio-container {
        max-width: 1400px !important;
    }
    
    .tab-nav {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .markdown h2 {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
    }
    
    .markdown h3 {
        color: #34495e;
        margin-top: 20px;
    }
    
    .dataframe {
        font-size: 12px;
    }
    
    .stats-box {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .filter-section {
        background: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .data-section {
        background: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    """
    
    # 创建Gradio界面
    with gr.Blocks(
        title="AI Resources Database",
        theme=gr.themes.Soft(),
        css=custom_css
    ) as app:
        
        # 应用标题和描述
        gr.Markdown("""
        # 🚀 AI Resources Database
        
        **智能资源数据库管理系统** - 基于Gradio构建的现代化数据库查询和管理平台
        
        ---
        
        ### ✨ 主要功能
        - 📊 **数据集管理**: 查看和筛选图像数据集信息
        - 🤖 **测试用例管理**: 管理AI模型测试用例
        - 🔍 **智能搜索**: 支持全局搜索和多条件筛选
        - 📥 **数据导出**: 一键导出多种格式数据
        - 📱 **响应式设计**: 适配各种屏幕尺寸
        
        ---
        """)
        
        # 创建标签页
        with gr.Tabs():
            dataset_tab = create_dataset_tab()
            models_tab = create_models_tab()
            
            # 系统状态标签页
            with gr.Tab("⚙️ 系统状态") as status_tab:
                gr.Markdown("## 🔧 系统状态监控")
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 📊 数据库状态")
                        db_status = gr.JSON(label="数据库健康检查", value=check_database_health())
                        
                        gr.Markdown("### 💻 系统信息")
                        sys_info = gr.JSON(label="系统信息", value=get_system_info())
                    
                    with gr.Column():
                        gr.Markdown("### 🔄 刷新状态")
                        refresh_btn = gr.Button("🔄 刷新状态信息", variant="primary")
                        
                        gr.Markdown("### 📝 操作日志")
                        log_display = gr.Textbox(
                            label="最近日志",
                            lines=10,
                            max_lines=20,
                            value="日志加载中...",
                            interactive=False
                        )
                
                # 刷新按钮事件
                refresh_btn.click(
                    fn=lambda: (check_database_health(), get_system_info()),
                    inputs=[],
                    outputs=[db_status, sys_info]
                )
        
        # 页脚信息
        gr.Markdown("""
        ---
        
        <div style="text-align: center; color: #6c757d; margin-top: 30px;">
            <p>🔧 <strong>AI Resources Database</strong> © 2025 | 
            基于 <a href="https://gradio.app" target="_blank">Gradio</a> 构建 | 
            <a href="https://github.com" target="_blank">GitHub</a></p>
            <p><small>💡 提示: 使用筛选器可以快速定位所需数据，支持多条件组合筛选</small></p>
        </div>
        """)
    
    return app

def test_database_connection():
    """测试数据库连接"""
    try:
        print("🔍 正在测试数据库连接...")
        logger.info("开始数据库连接测试")
        
        connection = db_manager.get_connection()
        if connection:
            connection.close()
            print("✅ 数据库连接测试成功!")
            logger.info("数据库连接测试成功")
            return True
    except Exception as e:
        print(f"❌ 数据库连接测试失败: {e}")
        print("💡 请检查数据库配置和环境变量设置")
        logger.error(f"数据库连接测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 启动 AI Resources Database (Gradio版本)")
    print("=" * 50)
    
    logger.info("应用启动开始")
    
    # 测试数据库连接
    if not test_database_connection():
        print("⚠️  数据库连接失败，但应用仍将启动（可能显示空数据）")
        logger.warning("数据库连接失败，应用将以离线模式启动")
    
    # 创建并启动应用
    app = create_app()
    
    print("\n🌟 应用配置:")
    print(f"   📁 工作目录: {os.getcwd()}")
    print(f"   💾 导出目录: exports/")
    print(f"   📝 日志目录: logs/")
    print(f"   🌐 访问地址: http://localhost:7860")
    print("\n🎯 启动应用...")
    
    logger.info("Gradio应用启动")
    
    # 启动Gradio应用
    app.launch(
        server_name="0.0.0.0",  # 允许外部访问
        server_port=7860,       # 端口号
        share=False,            # 不创建公共链接
        debug=True,             # 开启调试模式
        show_error=True,        # 显示错误信息
        quiet=False             # 显示启动信息
    )

if __name__ == "__main__":
    main()