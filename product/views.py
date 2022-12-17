from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category, Manufacturer, Color, Type

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

def category_page(request, slug):
    category = Category.objects.get(slug=slug)
    product_list = Product.objects.filter(category=category)

    return render(request, 'product/product_list.html', {
        'category': category,  # 'category': 템플릿 안의 변수명
        'product_list': product_list,
        'categories': Category.objects.all(),  # 사이드바 정상적 출력을 위해
        'no_category_post_count': Product.objects.filter(category=None).count  # 사이드바 정상적 출력을 위해
    })

def manufacturer_page(request, slug):
    manufacturer = Manufacturer.objects.get(slug=slug)
    product_list = Product.objects.filter(manufacturer=manufacturer)

    return render(request, 'product/product_list.html', {
        'manufacturer': manufacturer,  # 'category': 템플릿 안의 변수명
        'product_list': product_list,
        'categories': Category.objects.all(),  # 사이드바 정상적 출력을 위해
        'no_category_post_count': Product.objects.filter(category=None).count  # 사이드바 정상적 출력을 위해
    })

def color_page(request, slug):
    color = Color.objects.get(slug=slug)
    product_list = color.product_set.all()
    return render(request, 'product/product_list.html', {
        'color' : color,
        'product_list' : product_list,
        'categories': Category.objects.all(),  # 사이드바 정상적 출력을 위해
        'no_category_post_count': Product.objects.filter(category=None).count  # 사이드바 정상적 출력을 위해
    })

def type_page(request, slug):
    type = Type.objects.get(slug=slug)
    product_list = type.product_set.all()
    return render(request, 'product/product_list.html', {
        'type' : type,
        'product_list' : product_list,
        'categories': Category.objects.all(),  # 사이드바 정상적 출력을 위해
        'no_category_post_count': Product.objects.filter(category=None).count  # 사이드바 정상적 출력을 위해
    })