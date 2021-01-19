"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
"""
from django.contrib import admin
from django.urls import path
from api.views import AuthorRegisterView,AuthorLoginView,AuthorContentView,AdminRegisterView
from api.views import AdminLoginView,AdminContentView,SearchContent
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('author_register',AuthorRegisterView.as_view(),name='author_register'),
    path('author_login',AuthorLoginView.as_view(),name='author_login'),
    path('author_view',AuthorContentView.as_view(),name='author_view'),
    path('admin_register',AdminRegisterView.as_view(),name='admin_register'),
    path('admin_login',AdminLoginView.as_view(),name='admin_login'),
    path('admin_view',AdminContentView.as_view(),name='admin_view'),
    path('filter/',SearchContent.as_view(),name='serach_view'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
