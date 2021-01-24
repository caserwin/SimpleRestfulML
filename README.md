## 1. 说明
基于python3.6 + tornado 实现简单的 RESTful API，用于机器学习模型部署和调用。项目中用MySQL做数据持久化存储，Redis做缓存存储。
包含以下部分：

1. server 启动时，自动加载model文件夹下所有训练好的模型。因此在调用模型预测时，无需每次都把模型加载一遍。
2. 超时退出机制，目前设置600s无响应，则返回错误信息。
3. 模型upload，即把训练好的模型文件上传到model文件夹下，并且自动reload该模型到内存中，更新已有的模型。
4. 模型reload，可以直接把训练好的模型放到model文件夹下，并且根据传入的参数call reload API，用于reload 全部/指定 模型到内存。
5. 基于sklearn 中iris 数据集，训练决策树、逻辑回归。用于功能示例。
6. 包含mysql/redis 基本操作示例。
7. 多进程方式启动 tornado，并行处理 request。

## 2. 使用

有两种使用方式：

第一、更新已有的模型，步骤

1. 通过pickle.dump()训练模型的对象，使用upload()接口上传模型到service中。
2. 直接把pickle文件放到model文件夹下。通过reload()加载到内存。

第二、新增加模型，步骤

1. 建议把训练的模型类放在src/train下，类似dt_train.py和lr_train.py。
2. 使用upload()接口上传模型到service或把model直接放到model文件夹下。
3. 在server.py import模型的训练类。类似：
```
class RenameUnpickler(pickle.Unpickler):
    """
    https://stackoverflow.com/questions/27732354/unable-to-load-files-using-pickle-and-multiple-modules
    """

    def find_class(self, module, name):
        if name == 'LogisticRegressionTrain':
            from src.train.lr_train import LogisticRegressionTrain
            return LogisticRegressionTrain
        if name == 'DecisionTreeTrain':
            from src.train.dt_train import DecisionTreeTrain
            return DecisionTreeTrain

        return super(RenameUnpickler, self).find_class(module, name)
``` 
4. 继承 BaseHandler，实现自定义的Handler。
5. 重启 service。
以下是部署说明和使用示例：

## 3. 部署说明
依赖组件：1. MySQL&emsp;&emsp;2. redis&emsp;&emsp;3. python 3.6&emsp;&emsp;4. tornado&emsp;&emsp;5. OpenTSDB

这里MySQL、OpenTSDB、redis 非必备组件，只是有些示例接口中用到了。

导入依赖package：
```
pip install -r requirements.txt
```

### 3.1 MySQL部署说明

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

### 3.2 Redis 部署说明
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

### 3.3 bash 命令

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

## 4. 接口示例
### 4.1 /description
GET请求：
```
127.0.0.1:7250/description
```
说明：返回restful API说明

返回：
```
{
	"status": 0,
	"run time": 0.00018286705017089844,
	"message": "this is restful API for machine learning. welcome !"
}
```

### 4.2 /compute
GET请求：
```
127.0.0.1:7250/compute?a=1&b=2&ctype=1
```

说明：加减乘除操作，输入三个参数a、b、ctype。

1. ctype = 0：表示a+b。
2. ctype = 1：表示a-b。
3. ctype = 2：表示a*b。
4. ctype = 3：表示a/b。

返回：
```
{
	"status": 0,
	"run time": 0.000209808349609375,
	"message": -1
}
```

### 4.3 /iris/lr_predict
GET请求：
```
127.0.0.1:7250/iris/lr_predict
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
{
	"status": 0,
	"run time": 0.0004200935363769531,
	"message": {
		"label": "versicolor",
		"model": "lr_iris.model",
		"version": 3.0
	}
}
```

### 4.4 /iris/dt_predict
GET请求：
```
127.0.0.1:7250/iris/dt_predict
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
{
	"status": 0,
	"run time": 0.0025141239166259766,
	"message": {
		"label": "virginica",
		"model": "dt_iris.model",
		"version": 1.0
	}
}
```
### 4.5 /dbtest/train_data
GET请求：
```
127.0.0.1:7250/dbtest/train_data
```
说明：mysql 建表和写入，redis写入。

返回
```
{
	"status": 0,
	"run time": 0.12604689598083496,
	"message": "succeed to insert ignore 5 rows to error500_test"
}
```
### 4.6 /dbtest/predict_data
GET请求：
```
127.0.0.1:7250/dbtest/predict_data
```
说明：redis 读取。有2个参数，且默认为：
```
     timestamp = self.get_argument('timestamp', "2018-10-10 00:01:00")
     value = float(self.get_argument('value', 0.5))
```

返回
```
{
	"status": 0,
	"run time": 0.006543874740600586,
	"message": {
		"label": 0,
		"reference": 1.1,
		"true value": 0.5
	}
}
```
### 4.7 /reload_model
GET请求：
```
127.0.0.1:7250/reload_model
```
说明：加载model文件夹下，全部/指定的模型文件。有一个参数，且默认为：
```
    model_name = self.get_argument('modelname', None)
```
返回
```
{
	"status": 0,
	"run time": 0.002156972885131836,
	"message": "server has reload all models"
}
```

如果指定参数：```127.0.0.1:12340/reload_model?modelname=lr_iris.model```。
返回：
```
{
	"status": 0,
	"run time": 0.001062154769897461,
	"message": "server has reload lr_iris.model"
}
```

### 4.8 /upload_model
POST请求：
```
127.0.0.1:7250/upload_model
```

说明：上传模型文件，到model文件夹下。并且把上传的模型更新到内存。
<div align=centre><img width="80%" height="80%" src="https://github.com/caserwin/SimpleRestfulML/raw/master/pic/restfulAPI_4.png"/></div>

返回
```
{
	"status": 0,
	"run time": 0.002052045678986552,
	"message": "upload lr_iris.model success! server has reload lr_iris.model"
}
```

## 5. 技术细节说明
1. [模型部署](https://www.yuque.com/caserwin/cv9nqd/oqvz96)
