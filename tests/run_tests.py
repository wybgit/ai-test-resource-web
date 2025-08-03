#!/usr/bin/env python3
"""
测试运行器
Test runner for all tests
"""
import sys
import os
import unittest
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_all_tests():
    """运行所有测试"""
    print("🧪 AI Resources Database - 测试套件")
    print("=" * 50)
    
    # 发现并加载所有测试
    test_dir = Path(__file__).parent
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # 运行测试
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )
    
    print("🔍 开始运行测试...")
    result = runner.run(suite)
    
    # 输出测试结果摘要
    print("\n" + "=" * 50)
    print("📊 测试结果摘要:")
    print(f"   总测试数: {result.testsRun}")
    print(f"   成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   失败: {len(result.failures)}")
    print(f"   错误: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ 失败的测试:")
        for test, traceback in result.failures:
            print(f"   - {test}")
    
    if result.errors:
        print("\n💥 错误的测试:")
        for test, traceback in result.errors:
            print(f"   - {test}")
    
    # 计算成功率
    if result.testsRun > 0:
        success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
        print(f"\n📈 成功率: {success_rate:.1f}%")
    
    print("=" * 50)
    
    if result.wasSuccessful():
        print("🎉 所有测试通过!")
        return True
    else:
        print("❌ 部分测试失败，请检查上述错误信息")
        return False

def run_specific_test(test_name):
    """运行特定测试"""
    print(f"🧪 运行特定测试: {test_name}")
    print("=" * 50)
    
    try:
        # 导入并运行特定测试
        module = __import__(f"test_{test_name}", fromlist=[''])
        suite = unittest.TestLoader().loadTestsFromModule(module)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
    except ImportError as e:
        print(f"❌ 无法找到测试模块: test_{test_name}")
        print(f"   错误: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 运行特定测试
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
    else:
        # 运行所有测试
        success = run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()