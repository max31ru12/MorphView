from django.urls import path, include
from .views import Register, Logout, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
from .views import LoginView, CustomPasswordResetView, CustomPasswordResetDoneView

import django.contrib.auth.urls

app_name = 'auth_app'

urlpatterns = [

    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # path('', include('django.contrib.auth.urls')),

]
