from django.urls import path
from preprint.views import *

app_name = 'preprint'

urlpatterns = [
    path('mypage/', mypage, name='mypage'),
    path('cloud_history/', cloud_history, name='cloud_history'),
]