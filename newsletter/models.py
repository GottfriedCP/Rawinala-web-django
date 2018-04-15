from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Subscriber(models.Model):
    email = models.EmailField(max_length=150, unique=True)
    time_added = models.DateTimeField(auto_now_add=True, editable=False)
    uuid = models.CharField(max_length=96, unique=True, null=True, editable=False)

    def __str__(self):
        return self.email

    def save(self):
        if self.uuid is None:
            import datetime
            import hashlib
            seed = str(datetime.datetime.now()).encode('utf-8')
            self.uuid = hashlib.sha384(seed).hexdigest()
            super(Subscriber, self).save()

class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.created_at.year, self.created_at.month)
