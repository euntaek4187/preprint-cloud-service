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

        if not pw or not pw.isdigit() or len(pw) != 4:
            messages.error(req, "비밀번호는 숫자 4자리를 입력해야 합니다.")
            return render(req, "print_upload.html")

        upload = Upload.objects.create(upload_user=req.user, upload_pw=pw)

        for file in files:
            UploadFile.objects.create(upload=upload, upload_file=file)
        
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