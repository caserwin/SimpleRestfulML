mysql 说明
#### 创建用户
```
CREATE USER 'xyd'@'localhost' IDENTIFIED BY 'test';
```
#### 创建数据库
```
create database fbprop;
```
#### 权限赋予
```
GRANT ALL ON fbprop.* TO 'xyd'@'localhost';
```

