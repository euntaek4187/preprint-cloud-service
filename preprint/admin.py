from django.contrib import admin
from .models import Upload, UploadFile

# Register your models here.
admin.site.register(Upload)
admin.site.register(UploadFile)