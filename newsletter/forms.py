from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Newsletter

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'date_created', 'content', ]
        widgets = {
            'content': SummernoteWidget(),
        }
