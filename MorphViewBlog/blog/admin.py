from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms
from .models import *


widget = CKEditorUploadingWidget()


class ArticleAdminForm(forms.ModelForm):

    body = forms.CharField(widget=widget)

    class Meta:
        model = Article
        fields = '__all__'


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'created')


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('id', 'title', 'slug', 'publish', 'edited', 'category')
    prepopulated_fields = {'slug': ("title", )}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ("name",)}


admin.site.register(Article, ArticleAdmin)
