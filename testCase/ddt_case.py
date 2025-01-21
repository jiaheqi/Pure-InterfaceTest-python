import ddt, unittest, os, yaml
from Interface.testFengzhuang import TestApi
from Public.get_excel import makedata
from Public.log import LOG
from Public.panduan import assertre
from config.config import TestPlanUrl

file_dir = os.path.join(os.getcwd(), 'test_Report')
file_reslut = os.path.join(file_dir, 'caseresult.yaml')

data_test = makedata()


def write(data):
    with open(file_reslut, 'a', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)


def read(data):
    f = open(file_reslut, 'r', encoding='utf-8')
    d = yaml.load(f, Loader=yaml.FullLoader)
    return d[data]

# 递归转换非字符串类型为字符串
# 递归转换非字符串类型为字符串，但如果是字典或列表（即 JSON 对象），不进行转换
# 递归转换值为 int 类型的数据为 string，其它类型不做更改
def convert_values_to_string(data):
    if isinstance(data, dict):  # 如果是字典，递归转换其值
        return {key: convert_values_to_string(value) for key, value in data.items()}
    elif isinstance(data, list):  # 如果是列表，递归转换其元素
        return [convert_values_to_string(item) for item in data]
    elif isinstance(data, int):  # 如果是整数类型，转换为字符串
        return str(data)
    else:
        return data  # 对于其它类型（如字符串、浮动类型、布尔值等）保持不变

@ddt.ddt  # 使用ddt装饰器实现数据驱动测试
class MyTest(unittest.TestCase):
    def setUp(self):
        """测试前置操作"""
        LOG.info('测试用例开始执行')

    def tearDown(self):
        """测试后置操作"""
        LOG.info('测试用例执行完毕')

    @ddt.data(*data_test)  # 使用data_test数据集进行参数化测试
    def test_api(self, data_test):
        '''
        接口测试主函数
        1.处理参数
        2.判断参数是否有依赖
        3.依赖用例参数从本地获取
        4.获取失败，用例失败
        5.拼接后请求
        '''
        # 初始化基础参数字典
        # data_test = {
        # 'id': '',           # 用例ID
        # 'key': '',          # 接口密钥
        # 'coneent': '',      # 请求参数内容（注：这里可能是拼写错误，应该是'content'）
        # 'url': '',          # 接口URL
        # 'method': '',       # 请求方法（GET/POST等）
        # 'assertconnect': '' # 断言内容
        # }
        '''动态测试用例名称'''
        # 设置当前测试用例的名称
        test_name = data_test.get('casename', f"测试用例_{data_test['id']}")  # 假设Excel中用例名称字段为'casename'
        setattr(self, self._testMethodName, test_name)
        self._testMethodDoc = test_name
        parem = {'key': data_test['key']}
        try:
            # 将字符串格式的测试数据转换为字典
            # data_test['coneent'] 的示例值可能是这样的字符串：
            # '{"param1": "value1", "param2": "&case001=response_key"}'
            parem_dict = eval(data_test['coneent'])
            # 遍历参数字典，处理依赖参数
            for key, value in parem_dict.items():
                # 检查是否存在依赖参数（以&开头的参数）
                if str(value).startswith("&"):
                    try:
                        # 解析依赖参数格式：&用例ID=参数名
                        reply_key_id = str(value).split("&")[-1].split("=")
                        reply_keyid = reply_key_id[0]  # 依赖的用例ID
                        reply_key_key = reply_key_id[1]  # 依赖的参数名
                        # 从本地读取依赖用例的执行结果
                        reslut = read(reply_keyid)
                        if reslut is None:
                            self.assertTrue(False, '依赖用例获取失败')
                        # 获取依赖参数的值
                        get_value = reslut[reply_key_key]
                        if get_value is None:
                            self.assertTrue(False, '依赖参数获取失败，不存在')
                        # 更新当前参数值
                        parem_dict[key] = get_value
                    except Exception as e:
                        LOG.info("用例依赖执行失败：" + str(e))
                        self.assertTrue(False, '用例依赖执行失败')

            # 将处理后的参数更新到请求参数中
            parem.update({'info': parem_dict})
        except:
            self.assertTrue(False, msg="参数格式不对")
            
        # 记录最终的请求参数
        LOG.info(parem)
        
        # 构造API请求对象
        api = TestApi(url=TestPlanUrl + data_test['url'],
                      parame=parem,
                      method=data_test['method'])
                      
        # 记录请求信息（注：这里存在重复的日志输出）
        LOG.info('输入参数：url:%s,key:%s,参数:%s,请求方式：%s' % (data_test['url'], data_test['key'], data_test['assertconnect'],
                                                       LOG.info('输入参数：url:%s,key:%s,参数:%s,请求方式：%s' % (
                                                           data_test['url'], data_test['key'], data_test['assertconnect'],
                                                           data_test['method']))))
                                                           
        # 发送请求并获取JSON响应
        apijson = api.getJson()
        
        # 保存测试结果到本地
        reslut = {}
        reslut[data_test['id']] = apijson
        write(reslut)
        
        # 记录响应结果
        LOG.info('返回结果:%s' % apijson)
        
        # 解析预期结果并进行断言验证
        assertall = assertre(asserassert=data_test['assertconnect'])
        apijson = convert_values_to_string(apijson)
        print("=======")
        print(f'断言数据：{apijson}')
        print(f'请求返回数据：{assertall}')
        print("=======")
        # 断言 apijson 中是否包含 assertall 中的所有键值对，且其值为字符串
        self.assertEqual(assertall, apijson,msg="断言失败")
