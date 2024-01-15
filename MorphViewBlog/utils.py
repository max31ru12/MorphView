from services import is_staff
from django.contrib.auth.mixins import AccessMixin

menu = [
    {'title': 'Главная', 'url_name': 'base'},
    {'title': 'Статьи', 'url_name': 'thread'},
    {'title': 'Категории', 'url_name': 'category-list'},
]

admin_menu = {'title': 'Админка', 'url_name': 'admin:index'}
create_menu = {'title': 'Написать', 'url_name': 'create-article'}

# Жуткий костыль, стоило бы разобраться
path_dict = {
    'blog': {'url': 'blog', 'nav_title': 'Главная'},
    'article': {'url': 'blog/thread', 'nav_title': 'Статьи'},
    'category': {'url': 'blog/category', 'nav_title': 'Категории'},
    'thread': {'url': 'blog/thread', 'nav_title': 'Статьи'},
    'edit': {'url': 'blog/', 'nav_title': 'Изменить'},
    'auth': {'url': 'auth/register', 'nav_title': 'Регистрация'},
    'login': {'url': 'auth/login', 'nav_title': 'Войти'},
    'logout': {'url': 'auth/logout', 'nav_title': 'Выйти'},
    'password_reset': {'url': 'auth/password_reset', 'nav_title': 'Забыли пароль'},
}


def path_parse(request):

    path = request.path.strip('/').split('/')
    path = path[:len(path)-1]
    path_list = [path_dict[point] for point in path]

    return path_list


class DataMixin:

    def get_user_context(self, **kwargs) -> dict:
        context = kwargs

        if is_staff(self.request.user):
            if create_menu not in menu:
                menu.append(create_menu)
            if admin_menu not in menu:
                menu.append(admin_menu)
        elif admin_menu and create_menu in menu:
            menu.remove(admin_menu)
            menu.remove(create_menu)

        context['menu'] = menu

        context['path'] = path_parse(self.request)
        return context


class StaffRequiredMixin(AccessMixin):
    """Verify that the current user is staff."""

    def dispatch(self, request, *args, **kwargs):
        if not is_staff(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
