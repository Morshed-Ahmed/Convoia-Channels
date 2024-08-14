from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('home/', include('home.urls')),
    path('chat/', include('chat.urls')),
]
