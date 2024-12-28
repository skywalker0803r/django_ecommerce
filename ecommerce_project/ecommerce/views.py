from django.shortcuts import render, redirect,get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout

# 商品列表視圖
def product_list(request):
    products = Product.objects.all()  # 查詢所有商品
    return render(request, 'product_list.html', {'products': products})  # 渲染商品列表模板

# 商品詳情視圖
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # 根據商品 ID 獲取商品，找不到則返回 404
    return render(request, 'product_detail.html', {'product': product})  # 渲染商品詳情模板

# 使用者頁面
@login_required
def profile(request):
    return render(request, 'profile.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # 保存用戶
            login(request, user)  # 自動登入
            return redirect('profile')  # 註冊後重定向到個人資料頁面
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_logout(request):
    logout(request)  # 執行登出
    return redirect('/')  # 登出後重定向到首頁（或者您想要的頁面）
