from django.urls import path, include
from Order import views  # Importar las vistas desde la app 'orders'
from rest_framework.routers import DefaultRouter 
from Order.views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('orders/create/', views.CreateOrderView.as_view(), name='orders_create_create'),
    path('orders/user/', views.UserOrdersView.as_view(), name='orders_user_list'),
    path('', include(router.urls)),
]

