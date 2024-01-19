import os
import sys
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy

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
        two_latest = fetch_latest(Article.objects.filter(is_published=True), sort_field='-publish', limit=2)
        context['latest'] = two_latest
        categories_with_article_count = Category.objects.annotate(article_count=Count('article_category'))
        context['popular'] = categories_with_article_count.order_by('-article_count')[:3]
        return {**context, **mixin_context}


class ArticleCreateView(StaffRequiredMixin, DataMixin, CreateView):
    template_name = "blog/CreatePage.html"
    form_class = ArticleAdminForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['category_form'] = CategoryForm()
        context['unpublished'] = Article.objects.filter(is_published=False)
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
        # context["form"] = ArticleAdminForm(instance=Article.objects.get(slug=self.object.slug))
        context["form"] = ArticleAdminForm(instance=get_object(Article.objects, slug=self.object.slug))
        mixin_context = super().get_user_context(page_title='Править статью')
        return {**context, **mixin_context}

    def form_valid(self, form):
        return super().form_valid(form)

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
        cats = cache.get('cats')
        if cats:
            queryset = cats
        else:
            queryset = annotate(Category.objects, article_count=Count('article_category')).order_by('-article_count')
            cache.set('cats', queryset, 3600)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = super().get_user_context(page_title='Категории')
        return {**context, **mixin_context}


class ThreadView(DataMixin, ListView):
    template_name = "blog/Thread.html"
    queryset = fetch_latest(Article.objects, sort_field='-publish').select_related('category').filter(is_published=True)
    context_object_name = "articles"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = super().get_user_context(page_title='Статьи')
        return {**context, **mixin_context}


class ArticleDetailView(DataMixin, DetailView):
    model = Article
    template_name = 'blog/ArticleDetail.html'
    context_object_name = "article"
    slug_url_kwarg = 'article_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = fetch_latest(self.object.comments.select_related('user'), sort_field='-created')
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
        context['articles'] = fetch_latest(filter_objects(Article.objects.filter(is_published=True),
                                                          category=self.object.id),
                                           sort_field='-publish')
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
