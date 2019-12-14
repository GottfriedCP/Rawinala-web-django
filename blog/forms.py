from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'author', 'date_created', 'comment_enabled', 'published', 'summary', 'content', ]
        widgets = {
            'content': SummernoteWidget(),
        }
