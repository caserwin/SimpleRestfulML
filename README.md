## 1. 说明
基于python3.6 + tornado 实现简单的 RESTful API，用于机器学习模型部署和调用。项目中用MySQL做数据持久化存储，Redis做缓存存储。
包含以下部分：

1. server 启动时，自动加载model文件夹下所有训练好的模型。因此在调用模型预测时，无需每次都把模型加载一遍。
2. 超时退出机制，目前设置600s无响应，则返回错误信息。
3. 模型upload，即把训练好的模型文件上传到model文件夹下，并且自动reload该模型到内存中，更新已有的模型。
4. 模型reload，可以直接把训练好的模型放到model文件夹下，并且根据传入的参数call reload API，用于reload 全部/指定 模型到内存。
5. 基于sklearn 中iris 数据集，训练决策树、逻辑回归。用于功能示例。
6. 包含mysql/redis 基本操作示例。

以下是部署说明和使用示例：

## 2. 部署说明
依赖组件：1. mysql&emsp;&emsp;2. redis&emsp;&emsp;3. python 3.6&emsp;&emsp;4. tornado

导入项目依赖package，命令：
```
pip install -r requirements.txt
```

### 2.1 MySQL部署说明

1 启动/停止mysql服务
```
mysql.server start
mysql.server stop
```
2 以root用户登入
```
mysql -u root -p
```
3 创建用户
```
CREATE USER 'xyd'@'localhost' IDENTIFIED BY 'test';
```
4 创建数据库
```
create database fbprop;
```
5 赋予用户权限
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

在redis-xxx/src下后台启动redis服务：
```
./redis-server &
```

### 2.3 bash 命令

* 启动服务: ```sh server.sh start```
```
正在启动服务
服务启动成功
```

* 重启服务:```sh server.sh restart```
```
正在停止服务
服务停止成功
正在启动服务
服务启动成功
```

* 查看状态:```sh server.sh status```
```
501 42733     1   0  8:21下午 ttys000    0:13.28 python -u /Users/cisco/workspace/restfulML/server.py
```

* 暂停服务:```sh server.sh stop```
```
正在停止服务
服务停止成功
```

## 3. 接口示例
### 3.1 /description
GET请求：
```
127.0.0.1:12340/description
```
说明：返回restful API说明

返回：
```
{"status": 0, "result": "this is restful API for machine learning. welcome !"}
```

### 3.2 /compute
GET请求：
```
127.0.0.1:12340/compute?a=1&b=2&ctype=1
```

说明：加减乘除操作，输入三个参数a、b、ctype。

1. ctype = 0：表示a+b。
2. ctype = 1：表示a-b。
3. ctype = 2：表示a*b。
4. ctype = 3：表示a/b。

返回：
```
{"status": 0, "result": -1}
```

### 3.3 /iris/lr_predict
GET请求：
```
127.0.0.1:12340/iris/lr_predict
```

说明：基于逻辑回归训练的模型，有4个参数，且默认为：
```
    sepal_length = float(self.get_argument('sepal_length', 2.0))
    sepal_width = float(self.get_argument('sepal_width', 2.0))
    petal_length = float(self.get_argument('petal_length', 2.0))
    petal_width = float(self.get_argument('petal_width', 2.0))
```
根据传入的参数，判断该样本属于哪种类别。

返回
```
{"status": 0, "model": "lr_iris.model", "version": 1.0, "label": "versicolor"}
```

### 3.4 /iris/dt_predict
GET请求：
```
127.0.0.1:12340/iris/dt_predict
```
说明：基于决策树训练的模型，有4个参数，且默认为：
```
     sepal_length = float(self.get_argument('sepal_length', 2.0))
     sepal_width = float(self.get_argument('sepal_width', 2.0))
     petal_length = float(self.get_argument('petal_length', 2.0))
     petal_width = float(self.get_argument('petal_width', 2.0))
```
根据传入的参数，判断该样本属于哪种类别。

返回
```
{"status": 0, "model": "dt_iris.model", "version": 1.0, "label": "virginica"}
```
### 3.5 /dbtest/train_data
GET请求：
```
127.0.0.1:12340/dbtest/train_data
```
说明：mysql 建表和写入示例，redis写入示例。

返回
```
{"status": 0, "message": "succeed to insert ignore 5 rows to error500_test"}
```
### 3.6 /dbtest/predict_data
GET请求：
```
127.0.0.1:12340/dbtest/predict_data
```
说明：redis 读取示例。有2个参数，且默认参数为：
```
     timestamp = self.get_argument('timestamp', "2018-10-10 00:01:00")
     value = float(self.get_argument('value', 0.5))
```

返回
```
{"status": 0, "true value": 0.5, "reference": 1.1, "label": 0}
```
### 3.7 /reload_model
GET请求：
```
127.0.0.1:12340/reload_model
```
说明：加载model文件夹下，全部/指定的模型文件。有一个参数，且默认为：
```
    model_name = self.get_argument('modelname', None)
```
返回
```
{"status": 0, "message": "server has reload all models"}
```

如果指定参数：```127.0.0.1:12340/reload_model?modelname=lr_iris.model```。
返回：
```
{"status": 0, "message": "server has reload lr_iris.model"}
```

### 3.8 /upload_model
POST请求：
```
127.0.0.1:12340/upload_model
```

说明：上传模型文件，到model文件夹下。并且把上传的模型更新到内存。
<div align=centre><img width="80%" height="80%" src="https://github.com/caserwin/SimpleRestfulML/raw/master/pic/restfulAPI_4.png"/></div>

返回
```
{"status": 0, "message": "upload lr_iris.model success! server has reload lr_iris.model"}
```

### 3.9 新增加模型类
如果用户训练了自己的模型，那么如何使用？以下步骤：

1. 建议把训练的模型类放在src/train下，类似dt_train.py和lr_train.py。
2. pickle.dump()训练模型对象，通过upload()方式或直接放到model文件夹下。
3. 继承 BaseHandler，实现自定义的Handler。
4. 在server.py import模型的训练类。类似：
```
# noinspection PyUnresolvedReferences
from src.train.lr_train import LogisticRegressionTrain
# noinspection PyUnresolvedReferences
from src.train.dt_train import DecisionTreeTrain
``` 
5. 重启server。

## 4. 技术细节说明
参考：