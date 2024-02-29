
from django.urls import path

from .views import predict_stock , index,scrape_news

urlpatterns = [ 
    path ('',index, name='index'),
    path ('predict/', predict_stock, name='predict_stock'),
    path ('news/', scrape_news, name='news'),
]