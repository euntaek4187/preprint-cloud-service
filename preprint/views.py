from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Upload, UploadFile
import os
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

def check_file_date():
    now = timezone.now()
    for upload in Upload.objects.all():
        if now - upload.upload_date > timedelta(minutes=5):
            upload_files = UploadFile.objects.filter(upload=upload)

            for upload_file in upload_files:
                file_path = os.path.join(settings.MEDIA_ROOT, upload_file.upload_file.name)
                if os.path.exists(file_path):
                    os.remove(file_path)

            upload.delete()


def main(req):
    return render(req, 'print_main.html')

def upload(req):
    if req.method == "GET":
        if not req.user.is_authenticated:
            return redirect('accounts:login')
        else:
            return render(req, "print_upload.html")
    elif req.method == "POST":
        files = req.FILES.getlist('files')
        pw = req.POST['pw']

        if not files:
            messages.error(req, "파일을 선택해주세요.")
            return render(req, "print_upload.html")
        
        if not pw or len(pw) < 8:
            messages.error(req, "비밀번호는 8자리 이상의 문자, 숫자를 입력해야합니다.")
            return render(req, "print_upload.html")

        if Upload.objects.filter(upload_pw=pw).exists():
            messages.error(req, "이미 존재하는 비밀번호입니다.")
            return render(req, "print_upload.html")

        upload = Upload.objects.create(upload_user=req.user, upload_pw=pw)

        for file in files:
            UploadFile.objects.create(upload=upload, upload_file=file)
    check_file_date()
    return redirect('main')

def detail(req):
    upload_with_files = None
    if req.method == 'GET':
        cloud_code = req.GET.get('cloud_code', None)
        if cloud_code:
            try:
                upload = Upload.objects.get(upload_pw=cloud_code)
                upload_files = UploadFile.objects.filter(upload=upload)
                upload_with_files = {
                    'upload': upload,
                    'upload_files': upload_files,
                }
            except Upload.DoesNotExist:
                messages.error(req, "해당 파일 코드가 존재하지 않습니다.")
                return render(req, "print_main.html")

    return render(req, 'print_detail.html', {'upload_with_files': upload_with_files})

def delete_upload(req, upload_id):
    if req.method == 'POST':
        upload = get_object_or_404(Upload, pk=upload_id, upload_user=req.user)
        upload_files = UploadFile.objects.filter(upload=upload)

        for upload_file in upload_files:
            file_path = os.path.join(settings.MEDIA_ROOT, upload_file.upload_file.name)
            if os.path.exists(file_path):
                os.remove(file_path)

        upload.delete()
        return redirect('main')


def mypage(req):
    if not req.user.is_authenticated:
        return redirect('accounts:login')
    context = {
        'user': req.user
    }
    return render(req, 'preprint/mypage.html', context)

def cloud_history(req):
    if not req.user.is_authenticated:
        return redirect('accounts:login')

    uploads = Upload.objects.filter(upload_user=req.user).order_by('-upload_date')
    uploads_with_files = []
    
    for upload in uploads:
        upload_files = UploadFile.objects.filter(upload=upload)
        uploads_with_files.append({
            'upload': upload,
            'upload_files': upload_files,
        })
    
    context = {
        'uploads_with_files': uploads_with_files,
        'uploads_count': uploads.count(),
    }

    return render(req, 'preprint/cloud_history.html', context)