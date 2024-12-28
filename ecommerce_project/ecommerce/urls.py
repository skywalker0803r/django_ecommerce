# ecommerce/urls.py
from django.urls import path
from . import views  # 這裡應該是 .views，而不是 ecommerce_project.views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('signup/', views.signup, name='signup'),  # 註冊頁面路由
    path('login/', auth_views.LoginView.as_view(), name='login'),  # 登入
    path('logout/', views.user_logout, name='logout'),  # 自定義登出路由
    path('profile/', views.profile, name='profile'),  # 使用者個人資料頁面
]
