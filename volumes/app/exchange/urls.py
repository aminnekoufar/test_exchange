from django.urls import path

from . import views


urlpatterns = [
    path('', views.ExchangeView.as_view(), name='index'),    
    path('get-wallet/', views.ConvertCheckView.as_view(), name='check'),    
    path('confirm-change/', views.ConfirmConvertView.as_view(), name='confirm'),    

]