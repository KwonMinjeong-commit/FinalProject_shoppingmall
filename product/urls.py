from django.urls import path
from . import views

urlpatterns = [
    path('category/<str:slug>/', views.category_page),  # 카테고리 페이지
    path('manufacturer/<str:slug>/', views.manufacturer_page),  # 제조사 페이지
    path('', views.ProductList.as_view()),  # 상품 목록 페이지
    path('<str:slug>/', views.ProductDetail.as_view()), # 상품 상세 페이지
]