# project_name/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('document_update.urls')), 
    path('admin/', admin.site.urls),
    path('health-check/', views.healthCheck),
    path('monitoring/', include('monitoring.urls'))

]
