from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
import os

# Create your models here.
class Color(models.Model):  # 색
    color = models.CharField(max_length=30)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.color

    def get_absolute_url(self):
        return f'/product/color/{self.slug}/'

class Type(models.Model):   # 기종
    type = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return f'/product/type/{self.slug}/'

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
    hook_text = models.CharField(max_length=100, blank=True)  # 간단 설명
    content = models.TextField(null=True)    # 상품 설명
    price = models.IntegerField()  # 가격 (숫자형식)
    image = models.ImageField(upload_to='product/images/%Y/%m/%d/', blank=True)     # 이미지


    manufacturer = models.ForeignKey(Manufacturer, null=True, on_delete=models.SET_NULL)  # 제조사
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)  # 카테고리 models -> admin

    colors = models.ManyToManyField(Color, blank=True)
    types = models.ManyToManyField(Type, blank=True)


    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.price}원 ㆍㆍㆍ {self.manufacturer}'

    def get_absolute_url(self):
        return f'/product/{self.pk}/'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.product.get_absolute_url()}#comment-{self.pk}' # admin에서 View On Site 시 게시물을 보여주는 것이 아닌 게시물의 댓글을 보여줌

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'