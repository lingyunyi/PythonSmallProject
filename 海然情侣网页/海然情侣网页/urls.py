"""海然情侣网页 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path


from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 首页
    path(r'', views.index),
    # 日志页面page，别忘了逗号结尾,根目录前面不需要加/
    path(r'diary/', views.diary),
    path(r'diary/del/', views.diary_del),
    # 纪念日page，别忘了逗号结尾,根目录前面不需要加/
    path(r'memorial_day/', views.memorial_day),
    path(r'memorial_day/del/', views.memorial_day_del),

]
