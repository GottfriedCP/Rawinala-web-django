from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class NewsletterForm(forms.Form):
    content = forms.CharField(widget=CKEditorUploadingWidget(), label='')
