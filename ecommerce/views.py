from django.shortcuts import render, redirect,get_object_or_404
from .models import Product,Cart,Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from django.http import Http404
import paypalrestsdk
from django.conf import settings
from django.contrib import messages

# 初始化 PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

# paypal支付
@login_required
def paypal_checkout(request):
    # 遍歷購物車
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        messages.warning(request, "您的購物車為空，無法結帳。")
        return redirect('view_cart')
    # 計算總價
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    # 定義支付
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.build_absolute_uri('/paypal/execute/'),
            "cancel_url": request.build_absolute_uri('/paypal/cancel/')
        },
        "transactions": [{
            "item_list": {
                "items": [
                    {
                        "name": item.product.name,
                        "sku": str(item.product.id),
                        "price": str(item.product.price),
                        "currency": "USD",
                        "quantity": item.quantity
                    } for item in cart_items
                ]
            },
            "amount": {"total": str(total_price), "currency": "USD"},
            "description": "訂單支付"
        }]
    })
    # 創建支付
    if payment.create():
        # 尋找支付頁面
        for link in payment.links:
            # 如果支付連結存在
            if link.rel == "approval_url":
                # 導向 PayPal 支付頁面
                return redirect(link.href)
    else:
        messages.error(request, "PayPal 支付創建失敗，請重試。")
        return redirect('view_cart')

# 支付執行
@login_required
def paypal_execute(request):
    # 取得支付信息
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    payment = paypalrestsdk.Payment.find(payment_id)
    # 如果支付execute成功
    if payment.execute({"payer_id": payer_id}):
        # 撈出user購物車
        cart_items = Cart.objects.filter(user=request.user)
        # 初始化總價
        total_price = 0    
        # 初始化user訂單
        order = Order.objects.create(user=request.user) 
        # 遍歷購物品項
        for item in cart_items: 
            item.total = item.product.price * item.quantity  # 每項的總價
            total_price += item.total  # 累加到總金額
            # 寫入user訂單後清空購物車
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            item.delete()  
        # 設定訂單狀態為 "OK" 並保存
        order.status = 'OK'  
        order.save()
        # 返回支付成功頁面
        return render(request, 'order/order_confirmation.html', {'order': order,'total_price': total_price})
    else:
        messages.error(request, "支付失敗！")
        return redirect('view_cart')

# 用戶取消支付，顯示提示信息
@login_required
def paypal_cancel(request):
    messages.warning(request, "您已取消支付。")
    return redirect('view_cart')

# 商品列表頁面
def product_list(request):
    products = Product.objects.all()  # 查詢所有商品
    return render(request, 'product_list.html', {'products': products})  # 渲染商品列表模板

# 商品詳情頁面
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # 根據商品 ID 獲取商品，找不到則返回 404
    return render(request, 'product_detail.html', {'product': product})  # 渲染商品詳情模板

# 使用者資料頁面
@login_required
def profile(request):
    return render(request, 'profile.html')

# 註冊
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

# 查看購物車
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

# 新增商品
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1  # 增加商品數量
        cart_item.save()
    return redirect('/')

# 移除商品
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