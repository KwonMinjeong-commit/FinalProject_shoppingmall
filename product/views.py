from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category, Manufacturer

# Create your views here.
class ProductList(ListView):
    model = Product
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList,self).get_context_data()
        context['categories'] = Category.objects.all()      # 카테고리의 모든 정보 전달
        context['no_category_post_count'] = Product.objects.filter(category=None).count
        return context

class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetail,self).get_context_data()
        context['categories'] = Category.objects.all()      # 카테고리의 모든 정보 전달
        context['no_category_post_count'] = Product.objects.filter(category=None).count
        return context