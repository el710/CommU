"""
URL configuration for DJproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    ## added paths
    
    path('accounts/', include('django.contrib.auth.urls')),
        # This automatically provides views and URLs for:
        # + /accounts/login/ (login)  
        # + /accounts/logout/ (logout)
        # /accounts/password_change/ (password change)
        # /accounts/password_change/done/
        # /accounts/password_reset/ (password reset)
        # /accounts/password_reset/done/
        # /accounts/reset/<uidb64>/<token>/
        # /accounts/reset/done/

    path('', include('WebCommU.urls')),

]
