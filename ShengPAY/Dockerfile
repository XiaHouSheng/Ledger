# 使用 Python 3.9 作为基础镜像
FROM python:3.10.0

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器
COPY . /app/
# 设置清华 pip 镜像
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn
# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
#数据表同步
RUN python3 manage.py makemigrations

RUN python3 manage.py migrate
# 设置静态文件的路径
ENV STATIC_ROOT /app/static_new

ENV MEDIA_ROOT /app/media
# 设置 Django 相关环境变量
ENV DJANGO_SETTINGS_MODULE=ShengPAY.settings
ENV PYTHONUNBUFFERED=1

