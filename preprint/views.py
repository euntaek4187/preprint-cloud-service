from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Upload, UploadFile

# Create your views here.
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
        # color = req.POST['color']
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
        
        return redirect('main')

def detail(req):
    if not req.user.is_authenticated:
        return redirect('accounts:login')

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
                pass  # 혹은 오류 메시지 처리

    return render(req, 'print_detail.html', {'upload_with_files': upload_with_files})



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