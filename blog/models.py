from django.db import models
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    content = RichTextUploadingField()
    time_created = models.DateTimeField('Created at', auto_now_add=True, editable=False)
    time_modified = models.DateTimeField('Modified at', auto_now=True, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag', blank=True)
    publish_status = models.BooleanField('Publish?', default=True)
    views = models.IntegerField(default=0, editable=False)
    uuid = models.CharField(max_length=96, unique=True, null=True, editable=False)

    def __str__(self):
        return self.title

    def save(self):
        if self.uuid is None:
            import datetime
            import hashlib
            seed = str(datetime.datetime.now()).encode('utf-8')
            self.uuid = hashlib.sha384(seed).hexdigest()
        if self.slug is None:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super(Article, self).save()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:display', kwargs={'year': self.time_created.year, 'slug': self.slug})

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))
