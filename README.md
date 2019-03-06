## 1. 说明
基于tornado 实现简单的 python Restful API，用于机器学习模型部署和调用。用MySQL做数据持久化存储，Redis做缓存存储。
包含以下部分：

1. server 启动时，自动加载model文件夹下所有训练好的模型。因此在调用模型预测时，无需每次都把模型加载一遍。
2. 超时退出机制，目前设置600s无响应，则返回错误信息。
3. 模型upload，即把训练好的模型文件上传到model文件夹下，并且自动reload该模型到内存中，更新已有的模型。
4. 模型reload，可以直接把训练好的模型放到model文件夹下，并且根据传入的参数call reload API，用于reload 全部/指定 模型到内存。
5. 基于sklearn 中iris 数据集，训练决策树、逻辑回归。用于功能示例。
6. 包含mysql/redis 操作基本示例。

以下是部署说明和使用示例：

## 2. 部署说明
依赖组件：1. mysql&emsp;&emsp;2. redis&emsp;&emsp;3. python 3.6&emsp;&emsp;4. tornado

### 2.1 MySQL部署说明

#### 2.1.1 启动/停止mysql服务
```
mysql.server start
mysql.server stop
```
#### 2.1.2 以root用户登入
```
mysql -u root -p
```
#### 2.1.3 创建用户
```
CREATE USER 'xyd'@'localhost' IDENTIFIED BY 'test';
```
#### 2.1.4 创建数据库
```
create database fbprop;
```
#### 2.1.5 赋予用户权限
```
GRANT ALL ON fbprop.* TO 'xyd'@'localhost';
```

### 2.2 Redis 部署说明
redis 默认端口是6379，且数据库是由一个整数索引标识，而非数据库名称。默认情况下，一个客户端连接到数据库0。
所以在app.conf中配置：
```
[redis]
host=localhost
port=6379
db=0
```

## 3. 接口示例

### 3.1 description
说明：返回restful API说明

GET请求：127.0.0.1:12340/description

返回：{"status": 0, "result": "this is restful API for machine learning. welcome !"}

### 3.2 加减乘除 接口示例
说明：输入三个参数a、b、ctype。

1. ctype = 0：表示a+b。
2. ctype = 1：表示a-b。
3. ctype = 2：表示a*b。
4. ctype = 3：表示a/b。

请求：127.0.0.1:12340/compute?a=1&b=2&ctype=1

返回：{"status": 0, "result": -1}