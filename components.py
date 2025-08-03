"""
Gradio组件模块
UI components for the Gradio application
"""
import gradio as gr
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
import os
from datetime import datetime
from database import db_manager
from database_config import TABLE_CONFIG
from utils import create_status_message, create_export_filename, performance_monitor

def toggle_filter_visibility(current_visible: bool) -> Tuple[gr.Column, str]:
    """切换筛选器显示/隐藏状态"""
    new_visible = not current_visible
    button_text = "🔧 隐藏筛选选项" if new_visible else "🔧 显示筛选选项"
    return gr.Column(visible=new_visible), button_text

def create_filter_interface(table_name: str) -> Dict[str, gr.components.Component]:
    """创建筛选界面组件"""
    components = {}
    
    # 获取表配置
    table_config = TABLE_CONFIG[table_name]
    filter_columns = table_config.get("filter_columns", {})
    
    # 全局搜索框
    components["search"] = gr.Textbox(
        label="🔍 全局搜索",
        placeholder="输入关键词搜索所有字段...",
        value=""
    )
    
    # 为每个可筛选字段创建多选框
    for column_original, options in filter_columns.items():
        column_chinese = table_config["columns"][column_original]
        components[f"filter_{column_chinese}"] = gr.CheckboxGroup(
            label=f"📋 {column_chinese}",
            choices=options,
            value=[],
            interactive=True
        )
    
    # 重置按钮
    components["reset"] = gr.Button("🔄 重置所有筛选", variant="secondary")
    
    # 导出按钮组
    with gr.Row():
        components["export_csv"] = gr.Button("📥 导出CSV", variant="primary", scale=1)
        components["export_excel"] = gr.Button("📊 导出Excel", variant="secondary", scale=1)
        components["export_json"] = gr.Button("📄 导出JSON", variant="secondary", scale=1)
    
    return components

def create_data_display(table_name: str = None) -> Dict[str, gr.components.Component]:
    """创建数据显示组件"""
    components = {}
    
    # 获取初始数据
    if table_name:
        try:
            initial_df, initial_stats, _ = update_data_display(table_name)
        except:
            initial_df = pd.DataFrame({"提示": ["数据加载中..."]})
            initial_stats = "📊 **统计信息**: 数据加载中..."
    else:
        initial_df = pd.DataFrame({"提示": ["请选择数据表"]})
        initial_stats = "📊 **统计信息**: 请选择数据表"
    
    # 统计信息
    components["stats"] = gr.Markdown(initial_stats)
    
    # 数据表格 - 根据表格内容动态调整列宽
    if table_name == "dataset_index":
        # 数据集表格有12列，调整列宽
        column_widths = ["8%", "12%", "6%", "6%", "10%", "12%", "12%", "12%", "8%", "8%", "8%", "8%"]
    elif table_name == "test_cases":
        # 测试用例表格有15列，调整列宽
        column_widths = ["6%", "10%", "8%", "8%", "8%", "6%", "6%", "6%", "8%", "6%", "6%", "6%", "8%", "8%", "10%"]
    else:
        column_widths = None
    
    components["dataframe"] = gr.Dataframe(
        label="数据表格",
        interactive=False,
        wrap=True,
        value=initial_df,
        column_widths=column_widths
    )
    
    # 下载文件组件
    components["download"] = gr.File(
        label="下载导出文件",
        visible=False
    )
    
    return components

def update_data_display(
    table_name: str,
    search_text: str = "",
    **filter_kwargs
) -> Tuple[pd.DataFrame, str, gr.File]:
    """更新数据显示"""
    performance_monitor.start(f"update_data_display_{table_name}")
    
    try:
        # 提取筛选条件
        filters = {}
        for key, value in filter_kwargs.items():
            if key.startswith("filter_") and value:
                column_name = key.replace("filter_", "")
                filters[column_name] = value
        
        # 获取数据
        if search_text:
            df = db_manager.search_data(table_name, search_text)
        else:
            df = db_manager.filter_data(table_name, filters)
        
        # 获取统计信息
        total_count, filtered_count = db_manager.get_table_stats(table_name, filters if not search_text else None)
        
        # 使用工具函数格式化统计信息
        table_chinese_name = TABLE_CONFIG[table_name]["name"]
        if search_text:
            stats_text = f"🔍 **{table_chinese_name}**: 搜索 \"{search_text}\" 找到 {len(df):,} 条结果 / 总计 {total_count:,} 条"
        else:
            stats_text = create_status_message(total_count, filtered_count, table_chinese_name)
        
        # 添加性能信息
        duration = performance_monitor.end()
        stats_text += f" | ⏱️ 查询耗时: {duration:.2f}s"
        
        return df, stats_text, gr.File(visible=False)
        
    except Exception as e:
        performance_monitor.end()
        error_df = pd.DataFrame({"错误": [f"数据加载失败: {str(e)}"]})
        error_stats = f"❌ **错误**: 数据加载失败 - {str(e)}"
        return error_df, error_stats, gr.File(visible=False)

def export_data(
    table_name: str,
    current_df: pd.DataFrame,
    export_format: str = "csv"
) -> gr.File:
    """导出当前显示的数据"""
    performance_monitor.start(f"export_data_{table_name}_{export_format}")
    
    try:
        if current_df.empty:
            return gr.File(visible=False)
        
        # 创建导出目录
        export_dir = "exports"
        os.makedirs(export_dir, exist_ok=True)
        
        # 使用工具函数生成文件名
        table_chinese_name = TABLE_CONFIG[table_name]["name"]
        filename = create_export_filename(table_chinese_name, export_format)
        filepath = os.path.join(export_dir, filename)
        
        # 根据格式导出
        if export_format == "csv":
            current_df.to_csv(filepath, index=False, encoding='utf-8-sig')
        elif export_format == "excel":
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                current_df.to_excel(writer, index=False, sheet_name='数据')
        elif export_format == "json":
            current_df.to_json(filepath, orient='records', force_ascii=False, indent=2)
        else:
            raise ValueError(f"不支持的导出格式: {export_format}")
        
        duration = performance_monitor.end()
        print(f"✅ 导出完成: {filename} ({len(current_df)} 条记录, 耗时 {duration:.2f}s)")
        
        return gr.File(value=filepath, visible=True)
        
    except Exception as e:
        performance_monitor.end()
        print(f"❌ 导出失败: {e}")
        return gr.File(visible=False)

def reset_all_filters(table_name: str) -> Tuple[str, Dict[str, List], pd.DataFrame, str, gr.File]:
    """重置所有筛选条件"""
    # 重置搜索框
    search_text = ""
    
    # 重置所有筛选器
    filter_resets = {}
    table_config = TABLE_CONFIG[table_name]
    filter_columns = table_config.get("filter_columns", {})
    
    for column_original in filter_columns.keys():
        column_chinese = table_config["columns"][column_original]
        filter_resets[f"filter_{column_chinese}"] = []
    
    # 获取重置后的数据
    df = db_manager.get_all_data(table_name)
    total_count, _ = db_manager.get_table_stats(table_name)
    table_chinese_name = table_config["name"]
    stats_text = create_status_message(total_count, total_count, table_chinese_name)
    
    # 返回重置值
    result = [search_text]  # 搜索框重置
    
    # 添加各个筛选器的重置值
    for column_original in filter_columns.keys():
        result.append([])  # 每个筛选器都重置为空列表
    
    # 添加数据显示更新
    result.extend([df, stats_text, gr.File(visible=False)])
    
    return tuple(result)

def create_dataset_tab() -> gr.Tab:
    """创建数据集标签页"""
    with gr.Tab("📊 数据集") as tab:
        gr.Markdown("## 🗂️ 数据集管理")
        gr.Markdown("查看和筛选图像数据集信息，支持多条件筛选和数据导出。")
        
        # 筛选控制显示/隐藏按钮
        with gr.Row():
            toggle_filter_btn = gr.Button("🔧 显示筛选选项", variant="secondary", elem_classes=["toggle-button"])
        
        with gr.Row():
            with gr.Column(scale=1, visible=False) as filter_column:
                gr.Markdown("### 🔧 筛选控制")
                
                # 创建筛选组件
                filter_components = create_filter_interface("dataset_index")
                
                search_box = filter_components["search"]
                positive_target_filter = filter_components["filter_正向目标"]
                negative_target_filter = filter_components["filter_负向目标"]
                target_distance_filter = filter_components["filter_目标距离"]
                reset_btn = filter_components["reset"]
                export_csv_btn = filter_components["export_csv"]
                export_excel_btn = filter_components["export_excel"]
                export_json_btn = filter_components["export_json"]
            
            with gr.Column(scale=3):
                gr.Markdown("### 📋 数据展示")
                
                # 创建数据显示组件
                display_components = create_data_display("dataset_index")
                
                stats_display = display_components["stats"]
                data_display = display_components["dataframe"]
                download_file = display_components["download"]
        
        # 筛选器显示/隐藏切换事件
        filter_visible_state = gr.State(False)  # 初始状态为隐藏
        
        toggle_filter_btn.click(
            fn=lambda visible: (
                gr.Column(visible=not visible),
                "🔧 隐藏筛选选项" if not visible else "🔧 显示筛选选项",
                not visible
            ),
            inputs=[filter_visible_state],
            outputs=[filter_column, toggle_filter_btn, filter_visible_state]
        )
        
        # 设置事件处理
        inputs = [
            search_box,
            positive_target_filter,
            negative_target_filter, 
            target_distance_filter
        ]
        
        outputs = [data_display, stats_display, download_file]
        
        # 搜索和筛选事件
        for component in inputs:
            component.change(
                fn=lambda search, pos, neg, dist: update_data_display(
                    "dataset_index", search, 
                    **{"filter_正向目标": pos, "filter_负向目标": neg, "filter_目标距离": dist}
                ),
                inputs=inputs,
                outputs=outputs
            )
        
        # 重置事件
        reset_btn.click(
            fn=lambda: reset_all_filters("dataset_index"),
            inputs=[],
            outputs=[search_box, positive_target_filter, negative_target_filter, 
                    target_distance_filter, data_display, stats_display, download_file]
        )
        
        # 导出事件
        export_csv_btn.click(
            fn=lambda df: export_data("dataset_index", df, "csv"),
            inputs=[data_display],
            outputs=[download_file]
        )
        
        export_excel_btn.click(
            fn=lambda df: export_data("dataset_index", df, "excel"),
            inputs=[data_display],
            outputs=[download_file]
        )
        
        export_json_btn.click(
            fn=lambda df: export_data("dataset_index", df, "json"),
            inputs=[data_display],
            outputs=[download_file]
        )
        
        # 初始化数据加载
        # 在Gradio 4.x中，我们在组件创建时直接设置初始值
    
    return tab

def create_models_tab() -> gr.Tab:
    """创建模型测试用例标签页"""
    with gr.Tab("🤖 测试用例") as tab:
        gr.Markdown("## 🧪 测试用例管理")
        gr.Markdown("查看和筛选AI模型测试用例信息，支持多条件筛选和数据导出。")
        
        # 筛选控制显示/隐藏按钮
        with gr.Row():
            toggle_filter_btn = gr.Button("🔧 显示筛选选项", variant="secondary", elem_classes=["toggle-button"])
        
        with gr.Row():
            with gr.Column(scale=1, visible=False) as filter_column:
                gr.Markdown("### 🔧 筛选控制")
                
                # 创建筛选组件
                filter_components = create_filter_interface("test_cases")
                
                search_box = filter_components["search"]
                category_filter = filter_components["filter_类别"]
                label_filter = filter_components["filter_标签"]
                framework_filter = filter_components["filter_框架"]
                reset_btn = filter_components["reset"]
                export_csv_btn = filter_components["export_csv"]
                export_excel_btn = filter_components["export_excel"]
                export_json_btn = filter_components["export_json"]
            
            with gr.Column(scale=3):
                gr.Markdown("### 📋 数据展示")
                
                # 创建数据显示组件
                display_components = create_data_display("test_cases")
                
                stats_display = display_components["stats"]
                data_display = display_components["dataframe"]
                download_file = display_components["download"]
        
        # 筛选器显示/隐藏切换事件
        filter_visible_state = gr.State(False)  # 初始状态为隐藏
        
        toggle_filter_btn.click(
            fn=lambda visible: (
                gr.Column(visible=not visible),
                "🔧 隐藏筛选选项" if not visible else "🔧 显示筛选选项",
                not visible
            ),
            inputs=[filter_visible_state],
            outputs=[filter_column, toggle_filter_btn, filter_visible_state]
        )
        
        # 设置事件处理
        inputs = [
            search_box,
            category_filter,
            label_filter,
            framework_filter
        ]
        
        outputs = [data_display, stats_display, download_file]
        
        # 搜索和筛选事件
        for component in inputs:
            component.change(
                fn=lambda search, cat, lab, frame: update_data_display(
                    "test_cases", search,
                    **{"filter_类别": cat, "filter_标签": lab, "filter_框架": frame}
                ),
                inputs=inputs,
                outputs=outputs
            )
        
        # 重置事件
        reset_btn.click(
            fn=lambda: reset_all_filters("test_cases"),
            inputs=[],
            outputs=[search_box, category_filter, label_filter, framework_filter,
                    data_display, stats_display, download_file]
        )
        
        # 导出事件
        export_csv_btn.click(
            fn=lambda df: export_data("test_cases", df, "csv"),
            inputs=[data_display],
            outputs=[download_file]
        )
        
        export_excel_btn.click(
            fn=lambda df: export_data("test_cases", df, "excel"),
            inputs=[data_display],
            outputs=[download_file]
        )
        
        export_json_btn.click(
            fn=lambda df: export_data("test_cases", df, "json"),
            inputs=[data_display],
            outputs=[download_file]
        )
        
        # 初始化数据加载
        # 在Gradio 4.x中，我们在组件创建时直接设置初始值
    
    return tab