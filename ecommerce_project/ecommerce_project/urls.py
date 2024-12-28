# ecommerce_project/urls.py
from django.contrib import admin
from django.urls import path, include  # 使用 include 導入應用中的 urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Django 管理後台
    path('', include('ecommerce.urls')),  # 這行確保應用的 URL 被包含進來
]

# 媒體文件的 URL 路由
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)