from django.urls import path
from .views import *


urlpatterns = [
    path('', MainPage.as_view(), name='base'),
    path('thread/', ThreadView.as_view(), name='thread'),
    path('create/', ArticleCreateView.as_view(), name='create-article'),
    path('comment/<slug:article_slug>/', CommentCreateView.as_view(), name='comment'),
    path('article/<slug:article_slug>/', ArticleDetailView.as_view(), name='article'),
    path('article/edit/<slug:article_slug>/', ArticleEditView.as_view(), name='edit-article'),
    path('category/', CategoryListView.as_view(), name='category-list'),
    path('category/create/', CategoryCreateView.as_view(), name='create-category'),
    path('category/<slug:cat_slug>/', CategoryDetailView.as_view(), name='category'),
]
