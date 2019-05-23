from django.urls import path

from . import views

app_name = 'quiz'
urlpatterns = [
    path('home',        views.home,         name='home'),
    path('signup',      views.signup,       name='signup'),
    path('rank_list',   views.global_rank_list,    name='rank_list')
]