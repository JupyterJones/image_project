"""image_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

from django.contrib import admin
from django.urls import path
from image_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('show-image/', views.show_image, name='show_image'),
]

"""
# urls.py
from django.contrib import admin
from django.urls import path
from image_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  
    path('show-image/', views.show_image, name='show_image'),
    path('show-text/', views.show_text, name='show_text'),
    path('show-jonna/', views.show_jonna, name='show_jonna'),
    path('show-videos/', views.show_videos, name='show_videos'),
    path('search-code/', views.search_code, name='search_code'),
    path('edit-text/', views.edit_text, name='edit_text'),
    path('trim-video/', views.trim_video, name='trim_video'),
    path('edit-video/<str:video_name>/', views.edit_video, name='edit_video'),
    path('process-trim/', views.process_trim, name='process_trim'),
    path('trim-only/', views.trim_only, name='trim_only'),
    path('delete-video/<str:video_name>/', views.delete_video, name='delete_video'),

    
]
