# -*- coding: utf-8 -*-
# @Author  : leizi
from testCase.ddt_case import MyTest
import unittest, time, os
from Public import BSTestRunner

# 定义历史记录保存目录
BASH_DIR = "history"

if __name__ == '__main__':
    # 获取当前文件的绝对路径
    basedir = os.path.abspath(os.path.dirname(__file__))
    # 构建测试报告目录路径
    file_dir = os.path.join(basedir, 'test_Report')
    # 构建测试结果文件路径
    file_reslut = os.path.join(file_dir, 'caseresult.yaml')
    
    # 尝试删除已存在的测试结果文件
    try:
        os.remove(file_reslut)
    except:
        pass
    
    # 创建测试套件
    suite = unittest.TestSuite()
    # 将MyTest测试类中的所有测试用例添加到测试套件中
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(MyTest))
    
    # 获取当前时间作为报告文件名的一部分
    now = time.strftime('%Y-%m%d', time.localtime(time.time()))
    # 构建HTML报告文件路径
    file = os.path.join(file_dir, (now + '.html'))
    # 以二进制写模式打开报告文件
    re_open = open(file, 'wb')
    
    # 创建测试运行器实例
    besautiful = BSTestRunner.BSTestRunner(
        title="报告",              # 报告标题
        description="测试报告",     # 报告描述
        stream=re_open,           # 报告文件流
        trynum=3,                 # 失败重试次数
        filepath=BASH_DIR,        # 历史记录保存路径
        is_show=True             # 是否显示详细信息
    )
    
    # 运行测试套件
    besautiful.run(suite)
