from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product, Category, Manufacturer, Color, Type
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify

# Create your views here.
class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['title', 'hook_text', 'content', 'price', 'image', 'manufacturer', 'category', 'colors', 'types']

    template_name = 'product/product_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):  # 스태프나 슈퍼 유저만 수정 가능
            return super(ProductUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class ProductCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    fields = ['title', 'hook_text', 'content', 'price', 'image', 'manufacturer', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):  # 스태프나 슈퍼 유저만 등록 가능
            form.instance.author = current_user
            response = super(ProductCreate, self).form_valid(form)

            return response

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