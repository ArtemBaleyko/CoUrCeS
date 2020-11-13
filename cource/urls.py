from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:cource_id>/', views.cource, name='cource'),
    path('register-user', views.register_user, name='register_user'),
    path('login', views.login_user, name='login'),
    path('log_out', views.logged_out, name='log_out'),
    path('create-organization', views.create_organization, name='create_organization'),
    path('view-organization', views.view_organization, name='view_organization'),
    path('delete-organization', views.delete_organization, name='delete_organization'),
    path('edit-organization', views.edit_organization, name='edit_organization'),
    path('create-cource', views.create_cource, name='create_cource'),
    path('view-cources', views.view_cources, name='view_cources'),
    path('delete-cource/<int:cource_id>/', views.delete_cource, name='delete_cource'),
    path('edit-cource/<int:cource_id>/', views.edit_cource, name='edit_cource'),
    path('create-topic/<int:cource_id>/', views.create_topic, name='create_topic'),
    path('delete-topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    path('edit-topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('create-schedule/<int:cource_id>/', views.create_schedule, name='create_schedule'),
    path('delete-schedule/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
    path('edit-schedule/<int:schedule_id>/', views.edit_schedule, name='edit_schedule'),
    path('view_user_cource', views.view_user_cources, name='view_user_cources'),
    path('take_cource/<int:cource_id>/', views.take_cource, name='take_cource'),
    path('leave_cource/<int:cource_id>/', views.leave_cource, name='leave_cource'),
    path('search-cources', views.search_cources, name='search_cources'),
    path('view-search-result', views.view_search_result, name='view_search_result'),
]