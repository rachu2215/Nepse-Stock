
from django.urls import path

from .views import index,scrape_news,upload_file,download_data

urlpatterns = [ 
    path ('',index, name='index'),
    path('upload/', upload_file, name='predict_stock'),
    path ('news/', scrape_news, name='news'),
    path ('download/',download_data, name='download_data')
    
  
]