from django.db.models import Count

from blog.forms import ArticleAdminForm
from blog.models import Article, Category
from services import *


def latest_articles(count: int = 0) -> dict:
    """ N latest categories """
    if count:
        articles = fetch_latest(filter_objects(Article.objects.select_related('category'), is_published=True),
                                sort_field='-publish', limit=count)
    else:
        articles = fetch_latest(filter_objects(Article.objects.select_related('category'), is_published=True),
                                sort_field='-publish')
    return articles


def popular_categories(count: int) -> dict:
    """" N popular categories """
    categories = Category.objects.annotate(article_count=Count('article_category'))
    categories = categories.order_by('-article_count')[:count]
    return categories
    # return {'popular': categories}


def article_to_edit(obj):
    """ Get certain instance with provided slug """
    return ArticleAdminForm(instance=obj)


def get_comments(obj: Article):
    """ Get all comments of a single Article """
    comments = fetch_latest(obj.comments.select_related('user'), sort_field='-created')
    return comments


def category_articles(cat_id: int):
    articles = latest_articles()
    articles = filter_objects(articles, category=cat_id)
    return articles


def unpublished_articles():
    return Article.objects.filter(is_published=False)


def category_with_count():
    cats = Category.objects.annotate(article_count=Count('article_category'))
    return order(cats, '-article_count')


def article_thread():
    """ Get published and latest DESC """
    return latest_articles()



