from django.shortcuts import render, redirect,get_object_or_404
from .models import Product,Cart,Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from django.http import Http404

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

# 購物車邏輯 如果cart_items為空則返回空購物車
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    print(total_price,'11111111111111111')
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1  # 增加商品數量
        cart_item.save()
    return redirect('view_cart')

@login_required
def remove_from_cart(request, product_id):
    try:
        # 僅查詢當前用戶的購物車項目
        cart_item = get_object_or_404(Cart, id=product_id, user=request.user)
        cart_item.delete()
        return redirect('view_cart')
    except Cart.DoesNotExist:
        # 如果記錄不存在，返回 404 錯誤
        raise Http404("Cart item does not exist.")

# 訂單
@login_required
def checkout(request):
    # 撈出購物品項
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('view_cart')  # 如果購物車是空的，返回購物車頁面
    total_price = 0  # 初始化總價
    
    #初始化訂單
    order = Order.objects.create(user=request.user) 
    for item in cart_items: #遍歷購物品項
        item.total = item.product.price * item.quantity  # 每項的總價
        total_price += item.total  # 累加到總金額
        # 寫入訂單
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        item.delete()  # 清空購物車
    
    order.status = 'Pending'  # 設定訂單狀態為 "待處理"
    order.save()

    return render(request, 'order/order_confirmation.html', {
        'order': order,
        'total_price': total_price
        })
