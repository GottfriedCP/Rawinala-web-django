from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
import uuid

# Create your models here.
class Article(models.Model):
    """A blog post."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=1000, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True, help_text='Akan diisi oleh sistem bila kosong.')
    author = models.CharField(max_length=500, default='Rawinala', help_text='Nama penulis, bila kosong "Rawinala".')
    date_created = models.DateTimeField(default=timezone.now, help_text='YYYY-MM-DD HH:mm:ss')
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    view_count = models.IntegerField(default=0)
    comment_enabled = models.BooleanField('Izinkan komentar?', default=True)
    published = models.BooleanField('Publikasi sekarang?', default=True)
    content = models.TextField('Isi artikel:')

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def save(self):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save()

    def get_absolute_url(self):
        """Return absolute url for viewing the article."""
        return reverse('blog:article', args=[str(self.date_created.year), str(self.slug)])

    def get_edit_url(self):
        """Return url for editing the article."""
        return reverse('blog:edit', args=[str(self.date_created.year), str(self.slug)])
