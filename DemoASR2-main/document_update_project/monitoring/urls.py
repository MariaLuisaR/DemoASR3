from django.urls import path
from . import views

urlpatterns = [
    path('', views.server_list, name='server_list'),
    path('check-links/', views.check_links, name='check_links')
]
