# 接口测试框架（基于json格式、http请求,python3,不兼容python2.x版本）

## 项目介绍

 注：基于excel文件管理测试用例基本实现

 备注：大家在运行的时候，如果参数不需要key，只需要字典，可以在ddt_case.py和case.py改造parame,注释掉现在的parem，启用新的即可

 依赖用例支持用例执行，在testCase的ddt_case.py有实现，逻辑在代码中有写，参数的格式{"name":"$case1=data"}即代表name的值是case1的data字段，简单的实现

 依赖用例是简单的实现，具体在业务上面还有很多复杂的要处理，知识实现了，部分的思路

 (目前在部分window上会出现FileNotFoundError [Errno 2] No such file or directory，这个bug是路径过长,解决方案为吧log日志放在当前目录，或者修改动态生成的文件的名字，给了第一种方式，测试日志放在当前目录）

 使用的库 requests，绝大部分是基于Python原有的库进行的，这样简单方便

 使用脚本参数分离等思想，尽可能降低代码的耦合度

 如果你不配置钉钉机器人，注释到机器人相关的代码

## 目录结构介绍

### 1.Case文件夹用来存放我们的测试用例相关的

### 2.test_case_data用来存储我们的测试数据，excel管理测试用例，yaml文件管理测试用例，后续要把yaml管理测试用例的也封装出来

### 3.Interface对测试接口相关的封装，包括requests库，发送测试报告的email的封装，从excel取测试数据的封装

### 4.Public 展示测试报告相关的脚本，这里可以自己封装，也可以使用现成的，我这里是基于我自己封装的，最后生成的测试报告更加易懂，出错可以尽快排查相关原因

### 5.test_Report 存放测试报告

### 6.run_excel_re.py/run_html.py/run_new.py 主运行文件。运行后可以生成相应的测试报告

    run_excel_re.py生成 excel 报告，
    run_html.py生成 html 报告，
    run_new.py生成新的报告。

### 7.run_new.py 新版执行方式，重写了unittest方法，利用ddt驱动，生成漂亮的测试报告

## 快速开始

1. 安装依赖

```shell
pip install -r requirements.txt
```

2. 添加测试数据
   最后一列如果参与测试则设置为 Y，如果不参与则设置为非 Y，如 N，多个断言条件用`&`拼接
   ![添加测试数据](images/mdimages/2025-01-21-19-16-41.png)

3. 运行脚本

```shell
python run_new.py
```

4. 查看测试报告,测试报告在test_Report目录下

## run_new.py产生的html测试报告如下

![html 测试报告](images/mdimages/2025-01-21-18-00-33.png)

## run_excel_re.py产生的Excel测试报告如下

![excel 测试报告](images/mdimages/2025-01-21-18-03-23.png)
![excel 测试详情](images/mdimages/2025-01-21-18-03-58.png)

### 现在的测试结构更加完整，最新的一次提交增加了log日志的展示，使功能更加完善，log日志在控制台展示如下，对目录进行优化

![log 日志](images/mdimages/2025-01-21-18-04-54.png)
