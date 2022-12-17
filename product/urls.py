from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductList.as_view()),  # 상품 목록 페이지
    path('<str:slug>/', views.ProductDetail.as_view()), # 상품 상세 페이지

]