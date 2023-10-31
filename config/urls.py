from django.contrib import admin
from django.urls import path
from preprint.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name="main")
]
