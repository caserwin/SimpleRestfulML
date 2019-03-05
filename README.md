## 1. 说明
基于tornado 实现简单的 python Restful API，用于机器学习模型部署和调用。用MySQL做数据持久化存储，Redis做缓存存储。以下是使用示例和部署说明：

## 2. 部署说明
依赖组件：

1. mysql
2. redis
3. python 3.6
4. tornado

### 2.1 MySQL部署说明

#### 2.1.1 启动mysql服务
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

## 3. 接口使用例

### 3.1 description 接口示例
说明：返回restful API说明

请求：127.0.0.1:12340/description

返回：{"status": 0, "result": "this is restful API for machine learning. welcome !"}

<div align=centre><img width="80%" height="80%" src="https://github.com/caserwin/SimpleRestfulML/raw/master/pic/restfulAPI_1.png"/></div>

### 3.2 加减乘除 接口示例
说明：输入三个参数a、b、ctype。

1. ctype = 0：表示a+b。
2. ctype = 1：表示a-b。
3. ctype = 2：表示a*b。
4. ctype = 3：表示a/b。

请求：127.0.0.1:12340/compute?a=1&b=2&ctype=1

返回：{"status": 0, "result": -1}

<div align=centre><img width="80%" height="80%" src="https://github.com/caserwin/SimpleRestfulML/raw/master/pic/restfulAPI_2.png"/></div>
