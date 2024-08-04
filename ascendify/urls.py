from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ascendify_app.urls')),  # Include the URLs from the ascendify_app application
]
