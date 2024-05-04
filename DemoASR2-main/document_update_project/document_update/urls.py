from django.urls import path
from . import views
urlpatterns = [
    path('', views.upload_file, name='upload_file'),  
    path('process_email/', views.process_email, name='process_email')

]
