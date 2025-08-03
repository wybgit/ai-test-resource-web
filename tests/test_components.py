#!/usr/bin/env python3
"""
组件功能测试
Component functionality tests
"""
import sys
import os
from pathlib import Path
import unittest
import pandas as pd
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 模拟Gradio组件
class MockGradioComponent:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

class MockGradio:
    @staticmethod
    def Textbox(**kwargs):
        return MockGradioComponent(**kwargs)
    
    @staticmethod
    def CheckboxGroup(**kwargs):
        return MockGradioComponent(**kwargs)
    
    @staticmethod
    def Button(**kwargs):
        return MockGradioComponent(**kwargs)
    
    @staticmethod
    def Dataframe(**kwargs):
        return MockGradioComponent(**kwargs)
    
    @staticmethod
    def Markdown(**kwargs):
        return MockGradioComponent(**kwargs)
    
    @staticmethod
    def File(**kwargs):
        return MockGradioComponent(**kwargs)
    
    @staticmethod
    def Row():
        return MockGradioComponent()
    
    @staticmethod
    def Column(**kwargs):
        return MockGradioComponent(**kwargs)

# 模拟gradio模块
sys.modules['gradio'] = MockGradio()

from components import (
    create_filter_interface, 
    create_data_display,
    update_data_display,
    export_data,
    reset_all_filters
)

class TestComponents(unittest.TestCase):
    """组件测试类"""
    
    def test_create_filter_interface(self):
        """测试筛选界面创建"""
        # 测试数据集筛选界面
        components = create_filter_interface("dataset_index")
        self.assertIn("search", components)
        self.assertIn("filter_正向目标", components)
        self.assertIn("filter_负向目标", components)
        self.assertIn("filter_目标距离", components)
        self.assertIn("reset", components)
        self.assertIn("export_csv", components)
        self.assertIn("export_excel", components)
        self.assertIn("export_json", components)
        
        # 测试测试用例筛选界面
        components = create_filter_interface("test_cases")
        self.assertIn("search", components)
        self.assertIn("filter_类别", components)
        self.assertIn("filter_标签", components)
        self.assertIn("filter_框架", components)
    
    def test_create_data_display(self):
        """测试数据显示组件创建"""
        components = create_data_display()
        self.assertIn("stats", components)
        self.assertIn("dataframe", components)
        self.assertIn("download", components)
    
    @patch('components.db_manager')
    def test_update_data_display(self, mock_db):
        """测试数据显示更新"""
        # 模拟数据库返回
        mock_df = pd.DataFrame({"测试列": ["测试值1", "测试值2"]})
        mock_db.search_data.return_value = mock_df
        mock_db.filter_data.return_value = mock_df
        mock_db.get_table_stats.return_value = (10, 5)
        
        # 测试搜索更新
        df, stats, file = update_data_display("dataset_index", "测试搜索")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("搜索", stats)
        
        # 测试筛选更新
        df, stats, file = update_data_display(
            "dataset_index", 
            "", 
            filter_正向目标=["行人"]
        )
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("统计", stats)
    
    def test_export_data(self):
        """测试数据导出"""
        # 创建测试数据
        test_df = pd.DataFrame({
            "列1": ["值1", "值2"],
            "列2": [1, 2]
        })
        
        # 创建导出目录
        os.makedirs("exports", exist_ok=True)
        
        # 测试CSV导出
        result = export_data("dataset_index", test_df, "csv")
        # 由于返回的是Mock对象，我们只检查函数是否正常执行
        self.assertIsNotNone(result)
        
        # 测试Excel导出
        result = export_data("dataset_index", test_df, "excel")
        self.assertIsNotNone(result)
        
        # 测试JSON导出
        result = export_data("dataset_index", test_df, "json")
        self.assertIsNotNone(result)
        
        # 测试空数据框
        empty_df = pd.DataFrame()
        result = export_data("dataset_index", empty_df, "csv")
        self.assertIsNotNone(result)
    
    @patch('components.db_manager')
    def test_reset_all_filters(self, mock_db):
        """测试重置所有筛选"""
        # 模拟数据库返回
        mock_df = pd.DataFrame({"测试列": ["测试值1", "测试值2"]})
        mock_db.get_all_data.return_value = mock_df
        mock_db.get_table_stats.return_value = (10, 10)
        
        # 测试重置
        result = reset_all_filters("dataset_index")
        self.assertIsInstance(result, tuple)
        self.assertGreater(len(result), 5)  # 应该返回多个值

class TestUtilityFunctions(unittest.TestCase):
    """工具函数测试类"""
    
    def test_performance_monitor(self):
        """测试性能监控"""
        from utils import performance_monitor
        
        # 测试监控功能
        performance_monitor.start("test_operation")
        duration = performance_monitor.end()
        
        self.assertIsInstance(duration, float)
        self.assertGreaterEqual(duration, 0)
        
        # 测试统计功能
        stats = performance_monitor.get_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn("total_operations", stats)

if __name__ == "__main__":
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 添加组件测试
    suite.addTest(unittest.makeSuite(TestComponents))
    suite.addTest(unittest.makeSuite(TestUtilityFunctions))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出结果
    if result.wasSuccessful():
        print("\n✅ 所有组件测试通过!")
        sys.exit(0)
    else:
        print(f"\n❌ 组件测试失败: {len(result.failures)} 个失败, {len(result.errors)} 个错误")
        sys.exit(1)