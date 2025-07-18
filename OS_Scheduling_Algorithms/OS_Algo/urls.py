from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('algorithms/', views.algorithms, name='algorithms'),
]
