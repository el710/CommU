
from django.urls import path

from .views import *

urlpatterns = [
    path('', view_index, name ='index'), # it can be used in html templates like {% url 'index' %}

    path('info/', view_info),
    path('info/<str:args>', view_info, name='info'),

    path('signup/', view_signup, name='signup'),
    # path('logout/', view_logout),

    path('profile/', view_profile, name='profile'),
    
    path('user/', view_dashboard, name='dashboard'),
    # for search results
    path('user/<str:args>', view_dashboard, name='dashboard'),

    ## CRUD template skills
    path('uskill/', crud_skill), # create
    path('uskill/<str:args>', crud_skill), 

    path('event/', crud_event),
    path('event/<str:args>', crud_event),

    path('ucontract/', crud_contract),
    path('ucontract/<str:args>', crud_contract),

    path('uproject/', crud_project),
    path('uproject/<str:args>', crud_project),

]