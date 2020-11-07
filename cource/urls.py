from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:cource_id>/', views.cource, name='cource'),
]