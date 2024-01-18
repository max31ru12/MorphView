from django.db.models import QuerySet
from unidecode import unidecode
import re
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache


def custom_slugify(text: models.CharField) -> str:
    """функция для формирования слага из текста на кириллице"""
    # Транслитерация кириллических символов
    text = unidecode(str(text))
    # Замена пробелов и специальных символов на дефис
    text = re.sub(r'[^\w\s-]', '', text)
    # Замена пробелов на дефис и приведение к нижнему регистру
    text = re.sub(r'[-\s]+', '-', text).strip().lower()
    return text


def is_staff(user: User) -> bool:
    return user.is_staff and user.is_authenticated


def limit_decorator(func: callable):
    def wrapper(objects, limit=0, offset=0, *args, **kwargs):
        if not limit:
            return func(objects, *args, **kwargs)[offset:]
        return func(objects, *args, **kwargs)[offset:limit]

    return wrapper


def only_decorator(func: callable):
    def wrapper(objects, only=(), *args, **kwargs):
        return func(objects, *args, **kwargs).only(*only)
    return wrapper


def cache_decorator(func: callable):
    def wrapper(objects, cache_key: str = "", cache_time: int = 0, *args, **kwargs):
        cached_value = cache.get(cache_key)
        if cached_value:
            queryset = cached_value
        else:
            print('return queryset')
            queryset = func(objects, *args, **kwargs)
            cache.set(cache_key, queryset, cache_time)
        return queryset
    return wrapper


@limit_decorator
@only_decorator
def get_all_objects(objects):
    return objects.all()


def annotate(objects, **kwargs):
    return objects.annotate(**kwargs)


def order(queryset, *args):
    return queryset.order_by(*args)


@only_decorator
@limit_decorator
def fetch_latest(queryset: QuerySet, sort_field: str):
    """ Функция сортирует по полю, обязательные параметры queryset и sort_field можно указывать limit и offset"""
    return queryset.order_by(sort_field)


def get_id_by_name(queryset: QuerySet, condition, name: str) -> str:
    obj = queryset.filter(**{condition: name}).first()
    return obj.id


@only_decorator
def filter_objects(query, **kwargs):
    return query.filter(**kwargs)


def get_object(query, **kwargs):
    return query.get(**kwargs)
