import sys, os
# Этот импорт нужен импорта сервисов
sys.path.append(os.path.join(os.getcwd(), '..'))

from django.db import models
from django.contrib.auth.models import User
from services import custom_slugify

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name="Категория")
    slug = models.SlugField(max_length=64)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["id", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = custom_slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Article(models.Model):

    title = models.CharField(max_length=265)
    slug = models.SlugField(max_length=256)
    publish = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True, null=True, blank=True)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="article_category")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["id", "title", "category"]

    def save(self, *args, **kwargs):
        self.slug = custom_slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article", kwargs={"article_slug": self.slug})


class Comment(models.Model):

    post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["user", "created"]
        indexes = [
            models.Index(fields=['user', 'created'])
        ]

    def __str__(self):
        return f"Comment by {self.user}"

    def get_absolute_url(self):
        return reverse('article', kwargs={"article_slug": self.post.slug})
