from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'quiz'
urlpatterns = [
    path('',                             views.home,                         name = 'home'),
    path('home',                         views.home,                         name = 'home'),
    path('signup',                       views.signup,                       name = 'signup'),
    path('rank_list',                    views.global_rank_list,             name = 'rank_list'),
    url(r'^search_results/$',            views.search,                       name = 'search_results'),
    url(r'^send_request/$',              views.send_request,                 name = 'send_request'),
    url(r'^confirm_request/$',           views.confirm_request,              name = 'confirm_request'),
    url(r'^deny_request/$',              views.deny_request,                 name = 'deny_request'),
    url(r'^cancel_request/$',            views.cancel_request,               name = 'cancel_request'),
    url(r'^unfriend/$',                  views.unfriend,                     name = 'unfriend'),
    url(r'^submit_question/$',           views.submit_a_question,            name = 'submit_a_question'),
    url(r'^my_profile/$',                views.my_profile,                   name = 'my_profile'),
    url(r'^trophy_page/$',               views.trophy_page,                  name = 'trophy_page'),
    url(r'^friends_page/$',              views.friends_page,                name = 'friends_page'),
    
    # questions/need_validation
    url(r'^needs_validation/$',          views.needs_validation,             name = 'needs_validation'),
    url(r'^approve_question/$',          views.approve_question,             name = 'approve_question'),
    url(r'^moderator_candidates/$',      views.moderator_candidates,         name = 'moderator_candidates'),
    url(r'^approve_moderator/$',         views.approve_moderator,            name = 'approve_moderator'),
    url(r'^change_avatar/$',             views.change_avatar,                name = 'change_avatar'),
    
]