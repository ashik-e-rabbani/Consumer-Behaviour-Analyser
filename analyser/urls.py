
from django.urls import path
from . import views

urlpatterns = [
    path('analyser/', views.analyser, name='analyser'),
    path('social/', views.social, name='social')
]