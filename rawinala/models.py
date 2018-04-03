from django.db import models

# Create your models here.
class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    content = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

    def save(self):
        super(Message, self).save()