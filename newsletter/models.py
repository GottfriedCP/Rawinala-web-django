from django.db import models
from django.urls import reverse
from django.utils import timezone
import uuid

class Subsr(models.Model):
    """Subscriber (subsr) model.\n\n
    - id: subsr's id, also used for un-subscription\n
    - email: subsr's email address\n
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_unsubscribe_path(self):
        return reverse('newsletter:unsubscribe', args=[self.id])

class Newsletter(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True, default='', help_text='Opsional.')
    date_created = models.DateTimeField(default=timezone.now, help_text='Newsletter edition (date), default is now.')
    content = models.TextField()

    def __str__(self):
        return self.title
