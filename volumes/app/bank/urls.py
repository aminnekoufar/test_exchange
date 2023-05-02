from django.urls import path

from . import views


urlpatterns = [
    path('', views.balance_list.as_view(), name='index'),    
]