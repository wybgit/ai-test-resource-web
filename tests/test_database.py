#!/usr/bin/env python3
"""
数据库功能测试
Database functionality tests
"""
import sys
import os
from pathlib import Path
import unittest
import pandas as pd

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database import db_manager
from database_config import TABLE_CONFIG

class TestDatabase(unittest.TestCase):
    """数据库测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.db = db_manager
        self.test_tables = ["dataset_index", "test_cases"]
    
    def test_database_connection(self):
        """测试数据库连接"""
        try:
            connection = self.db.get_connection()
            self.assertIsNotNone(connection)
            if connection:
                self.assertTrue(connection.is_connected())
                connection.close()
        except Exception as e:
            self.fail(f"数据库连接失败: {e}")
    
    def test_get_all_data(self):
        """测试获取所有数据"""
        for table in self.test_tables:
            with self.subTest(table=table):
                df = self.db.get_all_data(table)
                self.assertIsInstance(df, pd.DataFrame)
                # 如果表不为空，检查列名是否正确
                if not df.empty:
                    expected_columns = list(TABLE_CONFIG[table]["columns"].values())
                    self.assertEqual(list(df.columns), expected_columns)
    
    def test_filter_data(self):
        """测试数据筛选"""
        # 测试数据集索引筛选
        filters = {"正向目标": ["行人"]}
        df = self.db.filter_data("dataset_index", filters)
        self.assertIsInstance(df, pd.DataFrame)
        
        # 测试测试用例筛选
        filters = {"类别": ["模型"]}
        df = self.db.filter_data("test_cases", filters)
        self.assertIsInstance(df, pd.DataFrame)
    
    def test_search_data(self):
        """测试搜索功能"""
        for table in self.test_tables:
            with self.subTest(table=table):
                df = self.db.search_data(table, "test")
                self.assertIsInstance(df, pd.DataFrame)
    
    def test_get_table_stats(self):
        """测试表统计"""
        for table in self.test_tables:
            with self.subTest(table=table):
                total, filtered = self.db.get_table_stats(table)
                self.assertIsInstance(total, int)
                self.assertIsInstance(filtered, int)
                self.assertGreaterEqual(total, 0)
                self.assertGreaterEqual(filtered, 0)
    
    def test_export_functions(self):
        """测试导出功能"""
        # 创建测试数据
        test_data = pd.DataFrame({
            "列1": ["值1", "值2"],
            "列2": [1, 2]
        })
        
        # 测试CSV导出
        csv_path = self.db.export_to_csv(test_data, "test.csv")
        if csv_path:
            self.assertTrue(os.path.exists(csv_path))
            os.remove(csv_path)  # 清理测试文件
        
        # 测试Excel导出
        excel_path = self.db.export_to_excel(test_data, "test.xlsx")
        if excel_path:
            self.assertTrue(os.path.exists(excel_path))
            os.remove(excel_path)  # 清理测试文件
        
        # 测试JSON导出
        json_path = self.db.export_to_json(test_data, "test.json")
        if json_path:
            self.assertTrue(os.path.exists(json_path))
            os.remove(json_path)  # 清理测试文件

class TestDatabaseConfig(unittest.TestCase):
    """数据库配置测试类"""
    
    def test_table_config(self):
        """测试表配置"""
        self.assertIn("dataset_index", TABLE_CONFIG)
        self.assertIn("test_cases", TABLE_CONFIG)
        
        for table_name, config in TABLE_CONFIG.items():
            with self.subTest(table=table_name):
                self.assertIn("name", config)
                self.assertIn("primary_key", config)
                self.assertIn("columns", config)
                self.assertIsInstance(config["columns"], dict)
    
    def test_column_mappings(self):
        """测试列映射"""
        for table_name, config in TABLE_CONFIG.items():
            with self.subTest(table=table_name):
                columns = config["columns"]
                self.assertGreater(len(columns), 0)
                
                # 检查是否有重复的中文列名
                chinese_names = list(columns.values())
                self.assertEqual(len(chinese_names), len(set(chinese_names)))

if __name__ == "__main__":
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 添加数据库测试
    suite.addTest(unittest.makeSuite(TestDatabase))
    suite.addTest(unittest.makeSuite(TestDatabaseConfig))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出结果
    if result.wasSuccessful():
        print("\n✅ 所有测试通过!")
        sys.exit(0)
    else:
        print(f"\n❌ 测试失败: {len(result.failures)} 个失败, {len(result.errors)} 个错误")
        sys.exit(1)