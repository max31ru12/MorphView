import os
import sys
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy

from .services import latest_articles, popular_categories, article_to_edit, get_comments, category_articles, \
    unpublished_articles, category_with_count, article_thread

sys.path.append(os.path.join(os.getcwd(), '..'))
from services import *
from utils import DataMixin, StaffRequiredMixin
from .forms import ArticleAdminForm, CategoryForm, CommentForm
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from .models import *
from django.core.cache import cache


class MainPage(DataMixin, TemplateView):
    template_name = "blog/MainPage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = super().get_user_context(page_title='Главная')
        context["latest"] = latest_articles(2)
        context["popular"] = popular_categories(3)
        return {**context, **mixin_context}


class ArticleCreateView(StaffRequiredMixin, DataMixin, CreateView):
    template_name = "blog/CreatePage.html"
    form_class = ArticleAdminForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['category_form'] = CategoryForm()
        context['unpublished'] = unpublished_articles()
        mixin_context = super().get_user_context(page_title='Написать статью')
        return {**context, **mixin_context}


class ArticleEditView(StaffRequiredMixin, DataMixin, UpdateView):
    model = Article
    template_name = "blog/ArticleEdit.html"
    form_class = ArticleAdminForm
    context_object_name = "article"
    slug_url_kwarg = 'article_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = super().get_user_context(page_title='Править статью')
        context["form"] = article_to_edit(get_object(Article.objects, slug=self.object.slug))
        return {**context, **mixin_context}

    def get_success_url(self):
        return reverse_lazy('article', kwargs={"article_slug": self.object.slug})


class CategoryCreateView(CreateView):
    form_class = CategoryForm

    def form_valid(self, form):
        cache.delete('cats')
        return super().form_valid(form)


class CategoryListView(DataMixin, ListView):
    template_name = "blog/Categories.html"
    context_object_name = "categories"
    paginate_by = 10

    def get_queryset(self):
        try:
            cats = cache.get('cats')
            if cats:
                queryset = cats
            else:
                queryset = category_with_count()
                cache.set('cats', queryset, 3600)
            return queryset
        except:
            queryset = category_with_count()
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = super().get_user_context(page_title='Категории')
        return {**context, **mixin_context}


class ThreadView(DataMixin, ListView):
    template_name = "blog/Thread.html"
    queryset = article_thread()
    context_object_name = "articles"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = super().get_user_context(page_title='Статьи')
        context = {**context, **mixin_context}
        return context


class ArticleDetailView(DataMixin, DetailView):
    model = Article
    template_name = 'blog/ArticleDetail.html'
    context_object_name = "article"
    slug_url_kwarg = 'article_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = get_comments(self.object)
        context['article_slug'] = self.object.slug
        mixin_context = super().get_user_context(page_title=self.object)
        return {**context, **mixin_context}


class CategoryDetailView(DataMixin, DetailView):
    model = Category
    template_name = 'blog/CategoryDetail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'cat_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = category_articles(self.object.id)
        mixin_context = super().get_user_context(page_title=self.object)
        return {**context, **mixin_context}


class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    login_url = reverse_lazy('auth_app:login')

    def form_valid(self, form):
        # редирект происходит в model.get_absolute_url на страницу поста
        form.instance.user = self.request.user
        form.instance.post = get_object(Article.objects, slug=self.kwargs['article_slug'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article', kwargs={"article_slug": self.kwargs['article_slug']})
