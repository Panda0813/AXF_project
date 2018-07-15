"""
WSGI config for AXF_Project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AXF_Project.settings")

application = get_wsgi_application()

# [uwsgi]
# # 使用nginx连接时 使用
# #socket=127.0.0.1:8010
# # 直接作为web服务器使用
# http=127.0.0.1:8000
# # 配置工程目录
# chdir=D:/python/AXF_Project_ZYW
# # 配置项目的wsgi目录。相对于工程目录
# wsgi-file=AXF_Project/wsgi.py
#
# #配置进程，线程信息
# processes=4
# threads=2
# enable-threads=True
# master=True
# pidfile=uwsgi.pid
# daemonize=uwsgi.log