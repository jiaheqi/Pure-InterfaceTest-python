""" 
@author: lileilei
@file: python_dict.py 
@time: 2018/6/15 13:54 
"""
'''字典取值'''


def res(d, code):
    result = []
    if isinstance(d, dict) and code in d.keys():
        value = d[code]
        result.append(value)
        return result
    elif isinstance(d, (list, tuple)):
        for item in d:
            value = res(item, code)
            if value == "None" or value is None:
                pass
            elif len(value) == 0:
                pass
            else:
                result.append(value)
        return result
    else:
        if isinstance(d, dict):
            for k in d:
                value = res(d[k], code)
                if value == "None" or value is None:
                    pass
                elif len(value) == 0:
                    pass
                else:
                    for item in value:
                        result.append(item)
            return result

if __name__ == '__main__':
    d = {'code': 0, 'result': {'error_no': 1001, 'message': '请求数据不是有效的Json字符串'}}
    key = 'code'
    result = {'code': '0'}
    print(res(d, 'code'))
    value1 = ([(str(res(d, key))) for key in result.keys()])
    print(value1)