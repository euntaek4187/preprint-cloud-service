from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import os
from preprint.models import Upload, UploadFile

class Command(BaseCommand):
    help = 'Delete uploaded or uploaded files whose expiration date has passed'

    def handle(self, *args, **options):
        now = timezone.now()
        expired_uploads = Upload.objects.filter(upload_date__lte=now - timedelta(days=7))

        for upload in expired_uploads:
            upload_files = UploadFile.objects.filter(upload=upload)

            for upload_file in upload_files:
                file_path = os.path.join(settings.MEDIA_ROOT, upload_file.upload_file.name)
                if os.path.isfile(file_path):
                    os.remove(file_path)

            upload.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {expired_uploads.count()} expired uploads and their files.'))
