from django.contrib import admin
from django.urls import path, include
from wishes.views import wish_view
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet, ProductsSidebarViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'sidebar', ProductsSidebarViewSet, basename='product-sidebar')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', wish_view, name='wish'),
    path('news/', include('news.urls')),
    path('api/', include(router.urls)),
]
