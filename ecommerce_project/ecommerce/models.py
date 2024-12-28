from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)  # 商品名稱
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 商品價格
    description = models.TextField()  # 商品描述
    stock = models.PositiveIntegerField()  # 商品庫存數量
    created_at = models.DateTimeField(auto_now_add=True)  # 創建時間
    updated_at = models.DateTimeField(auto_now=True)  # 更新時間
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # 商品圖片，保存在 'media/images/' 目錄

    def __str__(self):
        return self.name

# 類別模型
class Category(models.Model):
    name = models.CharField(max_length=50)  # 類別名稱
    description = models.TextField(blank=True, null=True)  # 類別描述
    created_at = models.DateTimeField(auto_now_add=True)  # 創建時間

    def __str__(self):
        return self.name  # 返回類別名稱作為模型的字符串表示
