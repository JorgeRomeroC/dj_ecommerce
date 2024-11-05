from django.urls import path, include

from web import views

app_name = 'web'

urlpatterns = [
   path('', views.index, name='index'),
   path('product_per_category/<int:category_id>/', views.product_per_category, name='product_per_category'),
   path('product_per_name/', views.product_per_name, name='product_per_name'),
   path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
   path('cart/', views.cart, name='cart'),
   path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
   path('delete_cart/<int:product_id>/', views.delete_cart, name='delete_cart'),
   path('clear_cart/', views.clear_cart, name='clear_cart'),
]