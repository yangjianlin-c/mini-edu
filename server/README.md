# 使用
更多功能参考：
https://github.com/jmitchel3/django-nextjs/tree/main

## 安装依赖
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
## 迁移
```shell
# 生成迁移文件
python manage.py makemigrations
python manage.py migrate
```
## 创建管理员账号
```shell
# 执行命令后进入交互界面（自行设置账号密码）
python manage.py createsuperuser
```
## 运行服务
```shell
python manage.py runserver
```
## 检查服务
> 浏览器访问
```shell
# 接口文档
http://127.0.0.1:8000/api/docs
# 后台系统
http://127.0.0.1:8000/admin
```


python manage.py flush
python manage.py loaddata data.json