from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, CartListView, CartDetailView, CartItemListView, \
    CartItemDetailView
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'post': 'create_action'}), name='product-detail'),
    path('carts/', CartListView.as_view(), name='cart-list'),
    path('carts/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('cart-items/', CartItemListView.as_view(), name='cart-item-list'),
    path('cart-items/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),
]
