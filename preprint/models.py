from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Upload(models.Model):
    upload_user = models.ForeignKey(verbose_name='유저', to= User, on_delete=models.CASCADE, null=True, blank=True)
    upload_pw = models.CharField(verbose_name='비밀번호', max_length=16)
    upload_date = models.DateTimeField(verbose_name='주문날짜', auto_now_add=True)

class UploadFile(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    upload_file = models.FileField(upload_to='files/')