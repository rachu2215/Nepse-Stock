
from django.urls import path

from .views import index,scrape_news,upload_file,scrape_and_predict

urlpatterns = [ 
    path ('',index, name='index'),
    path('upload/', upload_file, name='predict_stock'),
    path ('news/', scrape_news, name='news'),
    path ('predict/',scrape_and_predict,name='scrape_and_predict')
]