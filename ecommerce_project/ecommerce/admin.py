from django.contrib import admin
from .models import Product, Category
from django.utils.html import format_html

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'image_display')  # 顯示圖片欄位
    search_fields = ('name',)
    
    # 自定義顯示圖片
    def image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return '無圖片'

    image_display.short_description = '商品圖片'  # 設置欄位名稱

# 註冊商品模型
#admin.site.register(Product)

# 如果需要也可以註冊商品類別模型
admin.site.register(Category)

admin.site.register(Product, ProductAdmin)
