from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'quiz'
urlpatterns = [
    path('home',          views.home,                name = 'home'),
    path('signup',        views.signup,              name = 'signup'),
    path('rank_list',     views.global_rank_list,    name = 'rank_list'),
    url(r'^search_results/$',     views.search),
    url(r'^follow/$',     views.follow),
    url(r'^unfollow/$',     views.unfollow),
]