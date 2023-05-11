from django.contrib import admin
from .models import Product,Category
from .models import Customer
from .models.orders import Order

# Register your models here.
class AdminProduct(admin.ModelAdmin):
    list_display=['user_name','price','category']

class AdminCategory(admin.ModelAdmin):
    list_display=['user_name']

admin.site.register(Product,AdminProduct)
admin.site.register(Category,AdminCategory)
admin.site.register(Customer)
admin.site.register(Order )

