from django.urls import path
from . import views

app_name = 'shortener'

urlpatterns = [
    path('shorten/', views.shorten, name='shorten'),
    path('check/', views.check, name='check'),
    path('goto/', views.goto, name='goto_new'),
    path('mylinks/', views.my_links, name='my_links'),
    path('<int:pk>/delete', views.delete, name='delete'),
]
