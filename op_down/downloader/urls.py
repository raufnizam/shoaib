from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download, name='download'),
    path('send_cookies/', views.send_cookies, name='send_cookies'),
]
