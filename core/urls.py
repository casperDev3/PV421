from django.contrib import admin
from django.urls import path, include
from wishes.views import wish_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', wish_view, name='wish'),
    path('news/', include('news.urls'))
]
