基于tornado 实现简单的 python Restful API，用于机器学习模型部署和调用。下面示例中用 postman 来模拟 http 请求。

## description 接口示例
说明：返回restful API说明

请求：127.0.0.1:12340/description

返回：{"status": 0, "result": "this is restful API for machine learning. welcome !"}

<div align=centre><img width="80%" height="80%" src="https://github.com/caserwin/SimpleRestfulML/raw/master/pic/restfulAPI_1.png"/></div>


## 加减乘除 接口示例
说明：输入三个参数a、b、ctype。

1. ctype = 0：表示a+b。
2. ctype = 1：表示a-b。
3. ctype = 2：表示a*b。
4. ctype = 3：表示a/b。

请求：127.0.0.1:12340/compute?a=1&b=2&ctype=1

返回：{"status": 0, "result": -1}

<div align=centre><img width="80%" height="80%" src="https://github.com/caserwin/SimpleRestfulML/raw/master/pic/restfulAPI_2.png"/></div>


## iris数据集预测 接口示例
说明：使用sklearn 的iris数据集，基于逻辑回归训练好模型。现在传入样本feature参数，返回分类结果。
输入4个参数 sepal_length、sepal_width、sepal_width、sepal_width

请求：127.0.0.1:12340/iris_predict?sepal_length=3&sepal_width=5&sepal_width=0.3&sepal_width=0.6

返回：{"status": 0, "label": "setosa"}

<div align=centre><img width="80%" height="80%" src="https://github.com/caserwin/SimpleRestfulML/raw/master/pic/restfulAPI_3.png"/></div>
