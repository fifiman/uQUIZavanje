from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'quiz'
urlpatterns = [
    # /
    path('',                             views.home,                         name = 'home'),
    # /home
    path('home',                         views.home,                         name = 'home'),
    # /signup
    path('signup',                       views.signup,                       name = 'signup'),
    # /rank_list
    path('rank_list',                    views.global_rank_list,             name = 'rank_list'),
    # /search_results/
    url(r'^search_results/$',            views.search,                       name = 'search_results'),
    # /send_request/
    url(r'^send_request/$',              views.send_request,                 name = 'send_request'),
    # /confirm_request
    url(r'^confirm_request/$',           views.confirm_request,              name = 'confirm_request'),
    # /deny_request
    url(r'^deny_request/$',              views.deny_request,                 name = 'deny_request'),
    # /cancel_request
    url(r'^cancel_request/$',            views.cancel_request,               name = 'cancel_request'),
    # /unfriend
    url(r'^unfriend/$',                  views.unfriend,                     name = 'unfriend'),
    # /submit_question
    url(r'^submit_question/$',           views.submit_a_question,            name = 'submit_a_question'),
    # /my_profile
    url(r'^my_profile/$',                views.my_profile,                   name = 'my_profile'),
    # /trophy_page
    url(r'^trophy_page/$',               views.trophy_page,                  name = 'trophy_page'),
    # /friends_page
    url(r'^friends_page/$',              views.friends_page,                 name = 'friends_page'),
    # /submit_wants_moderator
    url(r'^submit_wants_moderator/$',    views.submit_wants_moderator,       name = 'submit_wants_moderator'),
    # questions/need_validation
    url(r'^needs_validation/$',          views.needs_validation,             name = 'needs_validation'),
    # /approve_question
    url(r'^approve_question/$',          views.approve_question,             name = 'approve_question'),
    # /moderator_candidates
    url(r'^moderator_candidates/$',      views.moderator_candidates,         name = 'moderator_candidates'),
    # /approve_moderator
    url(r'^approve_moderator/$',         views.approve_moderator,            name = 'approve_moderator'),
    # /change_avatar
    url(r'^change_avatar/$',             views.change_avatar,                name = 'change_avatar'),
    # /choose_avatar
    url(r'^choose_avatar/$',             views.choose_avatar,                name = 'choose_avatar'),


    
]