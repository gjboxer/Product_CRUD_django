from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product_list/', views.product_list, name='product_list'),
    path('product_update/<int:pk>', views.product_update, name='product_update'),
    path('product_delete/<str:name>', views.product_delete, name='product_delete'),
]
