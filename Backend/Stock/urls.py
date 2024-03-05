
from django.urls import path

from .views import index,scrape_news,upload_file

urlpatterns = [ 
    path ('',index, name='index'),
    path('upload/', upload_file, name='predict_stock'),
    path ('news/', scrape_news, name='news'),
]