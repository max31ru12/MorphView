from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import *


class ArticleAdminForm(forms.ModelForm):

    body = forms.CharField(widget=CKEditorUploadingWidget, label='Текст')

    class Meta:
        model = Article
        fields = ('title', 'body', 'category')
        labels = {
            'title': 'Название',
            'category': 'Категория'
        }


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name', )
        labels = {
            'name': 'Название категории'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': 'Комментарий'
        }

    body = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 60}), label='',
        # Другие параметры вашего поля...
    )
