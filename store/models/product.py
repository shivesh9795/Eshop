from django.db import models
from .category import Category

# Create your models here.
class Product(models.Model):
    user_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category,on_delete= models.CASCADE , default=1)
    description = models.CharField(max_length=50,default='',null=True,blank=True)
    image = models.ImageField(upload_to ='uploads/')

    @staticmethod
    def get_all_product():
        return Product.objects.all()

    @staticmethod
    def get_product_by_id(ids):
        return Product.objects.filter(id__in = ids)


    @staticmethod
    def get_all_product_by_id(category_id):
        if category_id:           
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_product()


    def __str__(self):
        return (self.user_name)