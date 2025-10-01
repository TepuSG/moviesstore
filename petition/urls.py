from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='petition.index'),
    path('create/', views.create, name='petition.create'),
    path('<int:id>/toggle-like/', views.toggle_like, name='petition.toggle_like'),
]
