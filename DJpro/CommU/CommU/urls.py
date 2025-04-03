"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""


"""
URL configuration for CommU project.

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
from django.urls import path

from main.views import (show_index, show_info,
                        signup, login, logout, show_userpage, 
                        crud_skill, crud_contract, crud_project, crud_event)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_index), ## index page 
    path('<str:args>', show_index), ## index.html page to show choosen user/skill/contract/project

    path('user/', show_userpage),
    path('user/<str:args>', show_userpage),

    path('info/', show_info),
    path('info/<str:args>', show_info),


    path('signup/', signup),
    path('login/', login),
    path('logout/',logout),

    path('skill/', crud_skill),
    path('skill/<str:args>', crud_skill),

    path('contract/', crud_contract),
    path('contract/<str:args>', crud_contract),

    path('project/', crud_project),
    path('project/<str:args>', crud_project),

    path('event/', crud_event),
    path('event/<str:args>', crud_event),
]
