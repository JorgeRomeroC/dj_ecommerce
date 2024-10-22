from django.urls import path, include

from web import views

app_name = 'web'

urlpatterns = [
   path('', views.index, name='index'),
   path('product_per_category/<int:category_id>/', views.product_per_category, name='product_per_category'),
   path('product_per_name/', views.product_per_name, name='product_per_name'),
   path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
]