from django.urls import path 

from .views import RegisterUserView, LoginUserView, index,register

urlpatterns = [
    path ('', index, name='index'),
    # path ('register1/', register, name='register'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),

]