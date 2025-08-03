"""
数据库操作模块
Database operations module for Gradio app
"""
import mysql.connector
from mysql.connector import Error
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
import logging
from database_config import DATABASE_CONFIG, TABLE_CONFIG
import json

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self):
        self.config = DATABASE_CONFIG
        self.table_config = TABLE_CONFIG
    
    def get_connection(self):
        """获取数据库连接"""
        try:
            connection = mysql.connector.connect(**self.config)
            if connection.is_connected():
                logger.info("数据库连接成功")
                return connection
        except Error as e:
            logger.error(f"数据库连接失败: {e}")
            raise e
    
    def execute_query(self, query: str, params: Optional[List] = None) -> List[Dict[str, Any]]:
        """执行查询并返回结果"""
        connection = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            return results
            
        except Error as e:
            logger.error(f"查询执行失败: {e}")
            return []
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def get_all_data(self, table_name: str) -> pd.DataFrame:
        """获取表的所有数据"""
        query = f"SELECT * FROM {table_name}"
        results = self.execute_query(query)
        
        if results:
            df = pd.DataFrame(results)
            # 重命名列为中文
            if table_name in self.table_config:
                column_mapping = self.table_config[table_name]["columns"]
                df = df.rename(columns=column_mapping)
            return df
        else:
            return pd.DataFrame()
    
    def filter_data(self, table_name: str, filters: Dict[str, List[str]]) -> pd.DataFrame:
        """根据筛选条件获取数据"""
        if not filters:
            return self.get_all_data(table_name)
        
        conditions = []
        params = []
        
        # 获取原始列名映射
        column_mapping = self.table_config[table_name]["columns"]
        reverse_mapping = {v: k for k, v in column_mapping.items()}
        
        for column_chinese, values in filters.items():
            if not values:
                continue
                
            # 转换为原始列名
            column_original = reverse_mapping.get(column_chinese, column_chinese)
            
            # 检查是否为SET类型字段
            filter_columns = self.table_config[table_name].get("filter_columns", {})
            if column_original in filter_columns:
                # SET类型字段使用FIND_IN_SET
                set_conditions = [f"FIND_IN_SET(%s, `{column_original}`)" for _ in values]
                conditions.append(f"({' OR '.join(set_conditions)})")
                params.extend(values)
            else:
                # 普通字段使用IN
                placeholders = ', '.join(['%s'] * len(values))
                conditions.append(f"`{column_original}` IN ({placeholders})")
                params.extend(values)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        query = f"SELECT * FROM {table_name} WHERE {where_clause}"
        
        results = self.execute_query(query, params)
        
        if results:
            df = pd.DataFrame(results)
            # 重命名列为中文
            df = df.rename(columns=column_mapping)
            return df
        else:
            return pd.DataFrame()
    
    def search_data(self, table_name: str, search_text: str) -> pd.DataFrame:
        """全局搜索数据"""
        if not search_text:
            return self.get_all_data(table_name)
        
        # 获取所有列名
        columns = list(self.table_config[table_name]["columns"].keys())
        
        # 构建搜索条件
        search_conditions = []
        params = []
        
        for column in columns:
            search_conditions.append(f"`{column}` LIKE %s")
            params.append(f"%{search_text}%")
        
        where_clause = " OR ".join(search_conditions)
        query = f"SELECT * FROM {table_name} WHERE {where_clause}"
        
        results = self.execute_query(query, params)
        
        if results:
            df = pd.DataFrame(results)
            # 重命名列为中文
            column_mapping = self.table_config[table_name]["columns"]
            df = df.rename(columns=column_mapping)
            return df
        else:
            return pd.DataFrame()
    
    def get_table_stats(self, table_name: str, filters: Optional[Dict[str, List[str]]] = None) -> Tuple[int, int]:
        """获取表统计信息"""
        # 总数
        total_query = f"SELECT COUNT(*) as total FROM {table_name}"
        total_result = self.execute_query(total_query)
        total_count = total_result[0]["total"] if total_result else 0
        
        # 筛选后数量
        if filters:
            filtered_df = self.filter_data(table_name, filters)
            filtered_count = len(filtered_df)
        else:
            filtered_count = total_count
        
        return total_count, filtered_count
    
    def export_to_csv(self, df: pd.DataFrame, filename: str) -> str:
        """导出数据为CSV文件"""
        try:
            # 添加BOM以支持Excel正确显示中文
            csv_path = f"exports/{filename}"
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            return csv_path
        except Exception as e:
            logger.error(f"导出CSV失败: {e}")
            return ""
    
    def export_to_excel(self, df: pd.DataFrame, filename: str) -> str:
        """导出数据为Excel文件"""
        try:
            excel_path = f"exports/{filename}"
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='数据')
            return excel_path
        except Exception as e:
            logger.error(f"导出Excel失败: {e}")
            return ""
    
    def export_to_json(self, df: pd.DataFrame, filename: str) -> str:
        """导出数据为JSON文件"""
        try:
            json_path = f"exports/{filename}"
            df.to_json(json_path, orient='records', force_ascii=False, indent=2)
            return json_path
        except Exception as e:
            logger.error(f"导出JSON失败: {e}")
            return ""
    
    def get_column_stats(self, table_name: str, column_name: str) -> Dict[str, Any]:
        """获取列统计信息"""
        try:
            # 获取原始列名
            table_config = self.table_config[table_name]
            column_mapping = table_config["columns"]
            reverse_mapping = {v: k for k, v in column_mapping.items()}
            original_column = reverse_mapping.get(column_name, column_name)
            
            query = f"""
            SELECT 
                COUNT(*) as total_count,
                COUNT(DISTINCT `{original_column}`) as unique_count,
                COUNT(`{original_column}`) as non_null_count
            FROM {table_name}
            """
            
            results = self.execute_query(query)
            if results:
                stats = results[0]
                stats['null_count'] = stats['total_count'] - stats['non_null_count']
                return stats
            return {}
            
        except Exception as e:
            logger.error(f"获取列统计失败: {e}")
            return {}

# 创建全局数据库管理器实例
db_manager = DatabaseManager()