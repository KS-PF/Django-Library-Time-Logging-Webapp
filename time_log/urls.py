from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('time_logging.urls')),
    path('accounts/', include('accounts.urls')),
    path('management/', include('management.urls')),
    path('admin/', admin.site.urls),
]