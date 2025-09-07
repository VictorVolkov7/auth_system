from django.urls import path

from apps.resources.views import ProductListView, ProductDetailView

app_name = 'resources'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
