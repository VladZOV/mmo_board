from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Post, Response, Newsletter


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

    def clean_category(self):
        category = self.cleaned_data['category']
        if not category:
            raise forms.ValidationError("Выберите категорию.")
        return category


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['subject', 'message']
