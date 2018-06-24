# Educational Administration System - Course Select

### 开发流程

1. 将master分支pull到本地，**创建自己的分支**进行代码改动

```shell
git checkout -b *** # 自己的分支名
```

2. 开启虚拟环境

```shell
source venv/bin/activate
```

3. 安装依赖

```shell
pip3 install -r requirements.txt
```

​    如果提示超时错误的话尝试以下命令，使用镜像安装：

```shell
pip3 install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
```

4. 本地运行

```shell
python3 manage.py makemigrations 
python3 manage.py migrate
python3 manage.py runserver
```

5. 在本地进行改动，确认无误后merge到master分支（同时处理冲突）

6. 有问题及时沟通！
