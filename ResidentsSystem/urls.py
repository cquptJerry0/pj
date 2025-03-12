"""ResidentsSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from app.views import show, admin, resident

urlpatterns = [

    # path('admin/', admin.site.urls),
    # 配置上传文件
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 前端页面显示部分的路由
    path('', show.index),
    path('resident/<int:nid>/detail/', show.detail),
    path('resident/detail/', show.detail),

    # 管理员登录和注销路由
    path('admin/login/', admin.admin_login),
    path('admin/logout/', admin.admin_logout),

    # 后台管理的路由
    path('resident/list/', resident.resident_list),
    path('resident/add/', resident.resident_add),
    path('resident/<int:nid>/edit/', resident.resident_edit),
    path('resident/<int:nid>/delete/', resident.resident_delete),

]
