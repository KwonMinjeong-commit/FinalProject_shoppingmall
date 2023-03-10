from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product, Category, Manufacturer, Color, Type, Comment
from .forms import CommentForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.db.models import Q

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
    fields = ['title', 'hook_text', 'content', 'price', 'image', 'manufacturer', 'category', 'colors', 'types']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):  # 스태프나 슈퍼 유저만 등록 가능
            form.instance.author = current_user
            return super(ProductCreate, self).form_valid(form)

        else:
            return redirect('/product/')

class ProductList(ListView):
    model = Product
    ordering = '-pk'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList,self).get_context_data()
        context['categories'] = Category.objects.all()      # 카테고리의 모든 정보 전달
        context['no_category_product_count'] = Product.objects.filter(category=None).count
        context['manufacturers'] = Manufacturer.objects.all()  # 제조사의 모든 정보 전달
        context['no_manufacturer_product_count'] = Product.objects.filter(category=None).count
        return context

class ProductSearch(ProductList): # ListView 상속 -> post_list, post_list.html 자동 연결
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        product_list = Product.objects.filter(Q(title__contains=q) | Q(content__contains=q)).distinct()
        return product_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context

class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetail,self).get_context_data()
        context['categories'] = Category.objects.all()  # 카테고리의 모든 정보 전달
        context['no_category_product_count'] = Product.objects.filter(category=None).count
        context['manufacturers'] = Manufacturer.objects.all()  # 제조사의 모든 정보 전달
        context['no_manufacturer_product_count'] = Product.objects.filter(category=None).count
        context['comment_form'] = CommentForm
        return context


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def category_page(request, slug):
    category = Category.objects.get(slug=slug)
    product_list = Product.objects.filter(category=category)

    return render(request, 'product/product_list.html', {
        'category': category,  # 'category': 템플릿 안의 변수명
        'product_list': product_list,
        'categories': Category.objects.all(),  # 사이드바 정상적 출력을 위해
        'no_category_product_count': Product.objects.filter(category=None).count  # 사이드바 정상적 출력을 위해
    })

def manufacturer_page(request, slug):
    manufacturer = Manufacturer.objects.get(slug=slug)
    product_list = Product.objects.filter(manufacturer=manufacturer)

    return render(request, 'product/product_list.html', {
        'manufacturer': manufacturer,  # 'category': 템플릿 안의 변수명
        'product_list': product_list,
        'manufacturers': Manufacturer.objects.all(),  # 사이드바 정상적 출력을 위해
        'no_manufacturer_product_count': Product.objects.filter(category=None).count  # 사이드바 정상적 출력을 위해
    })

def color_page(request, slug):
    color = Color.objects.get(slug=slug)
    product_list = color.product_set.all()
    return render(request, 'product/product_list.html', {
        'color' : color,
        'product_list' : product_list,
        'colors': Color.objects.all(),  # 사이드바 정상적 출력을 위해
        'no_colors_product_count': Product.objects.filter(category=None).count  # 사이드바 정상적 출력을 위해
    })

def type_page(request, slug):
    type = Type.objects.get(slug=slug)
    product_list = type.product_set.all()
    return render(request, 'product/product_list.html', {
        'type' : type,
        'product_list' : product_list,
        'types': Type.objects.all(),  # 사이드바 정상적 출력을 위해
        'no_types_product_count': Product.objects.filter(category=None).count  # 사이드바 정상적 출력을 위해
    })

def new_comment(request,pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)  # comment_form : 변수
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)  # 저장하긴 하는데 모델에 저장은 x
                comment.product = product
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:  # GET
            return redirect(product.get_absolute_url())
    else:  # 로그인 안 한 사용자
        raise PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    product = comment.product
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(product.get_absolute_url())
    else:
        PermissionDenied

def scrap(request, pk):
    product = get_object_or_404(Product, pk=pk) # pk값에 해당하는 게시물 받아옴
    user = request.user
    if user in product.scrap.all():     # 요청 유저가 이미 스크랩을 했으면
        product.scrap.remove(user)  # 유저 삭제
    else: # 스크랩을 아직 안한 유저라면
        product.scrap.add(user)     # 스크랩 목록에 요청 유저 추가
    return redirect('product_detail', pk)


def scrap_list(request):
    user = request.user
    return render(request, 'mypage.html', {'user':user})
