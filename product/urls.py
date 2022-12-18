from django.urls import path
from . import views

urlpatterns = [

    path('update_product/<int:pk>', views.ProductUpdate.as_view()),  # 상품 등록 페이지
    path('register_product/', views.ProductCreate.as_view()),  # 상품 등록 페이지
    path('color/<str:slug>/', views.color_page),  # 색 페이지
    path('type/<str:slug>/', views.type_page),  # 기종 페이지
    path('category/<str:slug>/', views.category_page),  # 카테고리 페이지
    path('manufacturer/<str:slug>/', views.manufacturer_page),  # 제조사 페이지

    path('<int:pk>/new_comment/', views.new_comment),

    path('', views.ProductList.as_view()),  # 상품 목록 페이지
    path('<int:pk>/', views.ProductDetail.as_view()),  # 상품 상세 페이지

]