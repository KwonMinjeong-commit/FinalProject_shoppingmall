from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Manufacturer(models.Model):
    name = models.CharField(max_length=30, unique=True)  # 제조사명
    address = models.CharField(max_length=100)    # 주소
    phone_num = PhoneNumberField(unique=True)   # 연락처
    establish_date = models.DateTimeField() # 설립일

    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/product/manufacturer/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/product/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    title = models.CharField(max_length=30)  # 상품명
    slug = models.SlugField(max_length=200, null=True, unique=True, allow_unicode=True)

    hook_text = models.CharField(max_length=100, blank=True)  # 간단 설명
    content = models.TextField(null=True)    # 상품 설명
    price = models.IntegerField()  # 가격 (숫자형식)
    image = models.ImageField(upload_to='product/images/%Y/%m/%d/', blank=True)     # 이미지


    manufacturer = models.ForeignKey(Manufacturer, null=True, on_delete=models.SET_NULL)  # 제조사
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)  # 카테고리 models -> admin

    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.price}원 ㆍㆍㆍ {self.manufacturer}'

    def get_absolute_url(self):
        return f'/product/{self.slug}/'