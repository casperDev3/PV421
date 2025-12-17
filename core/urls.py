from django.contrib import admin
from django.urls import path, include
from wishes.views import wish_view
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet, ProductsSidebarViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'sidebar', ProductsSidebarViewSet, basename='product-sidebar')

urlpatterns = [
    # client routes
    path('', wish_view, name='wish'),
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),

    # api routes
    path('api/', include(router.urls)),
    path('api/auth/', include('auth.urls')),
]
