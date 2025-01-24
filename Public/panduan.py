# -*- coding: utf-8 -*-
# @Date    : 2017-08-02 21:54:08
# @Author  : lileilei
import ast

from Public.fengzhuang_dict import res
from Public.log import logger, LOG


@logger('断言测试结果')
def assert_in(asserassert, returnjson):
    if len(asserassert.split('=')) > 1:
        data = asserassert.split('&')
        result = dict([(item.split('=')) for item in data])  # result = {'code': '0', 'result': "{'error_no': 1001, 'message': '请求数据不是有效的Json字符串'}"}
        value1 = ([str(res(returnjson, key)[0]) for key in result.keys()])  # value1 = ['0', "{'error_no': 1001, 'message': '请求数据不是有效的Json字符串'}"]
        value2 = ([value for value in result.values()])
        if value1 == value2:
            return {'code': 0, "result": 'pass'}
        else:
            return {'code': 1, 'result': 'fail'}
    else:
        LOG.info('填写测试预期值')
        return {"code": 2, 'result': '填写测试预期值'}


@logger('断言测试结果')
def assertre(asserassert):
    if len(asserassert.split('=')) > 1:
        data = asserassert.split('&')
        result = dict([(item.split('=')) for item in data])

        # 处理 result 字段，如果是 JSON 字符串，解析成字典
        if 'result' in result:
            try:
                # 尝试将 result 的值从字符串解析为字典
                result['result'] = ast.literal_eval(result['result'])  # 将字符串转换为字典
            except (ValueError, SyntaxError):  # 如果解析失败，说明 result 不是一个合法的字典字符串
                pass  # 保持原始字符串不变
        return result
    else:
        LOG.info('填写测试预期值')
        raise {"code": 1, 'result': '填写测试预期值'}


if __name__ == '__main__':
    asserassert = "code=0,result={'error_no': '1001', 'message': '请求数据不是有效的Json字符串'}"
    returnjson = "{'code': 0, 'result': {'error_no': 1001, 'message': '请求数据不是有效的Json字符串'}}"
    assert_in(asserassert, returnjson)
