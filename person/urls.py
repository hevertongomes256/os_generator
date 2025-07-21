from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import PersonListView

urlpatterns = [
    path('/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('/logout/', LogoutView.as_view(), name='logout'),
    path('/list', PersonListView.as_view(), name='clients-list'),
]
