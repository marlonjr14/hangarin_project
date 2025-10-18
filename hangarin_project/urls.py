from django.contrib import admin
from django.urls import path, include
from tasks.views import HomePageView

urlpatterns = [
    path("admin/", admin.site.urls),
     path('', include('pwa.urls')),  
    path("accounts/", include("allauth.urls")),  # allauth routes 
    path("accounts/", include("django.contrib.auth.urls")),
    path("", HomePageView.as_view(), name="home"),

    # Include all task-related URLs inside tasks/urls.py; remove direct task URL patterns here
    path('tasks/', include('tasks.urls')),
]
