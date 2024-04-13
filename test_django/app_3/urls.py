from django.urls import path

from .views import (
    taskView, DetailView, deletecheckedView, deleteView, searchView, userView, loginView, logoutView, profileView, addppView
)

urlpatterns = [
    path('/tasks', taskView.as_view(), name='task'),
    path('/tasks', taskView.as_view(), name='create_task'),

    path('/tasks/<int:pk>', DetailView.as_view(), name='detail_task'),
    path('/tasks/<int:pk>', DetailView.as_view(), name='update_task'),
    path('/tasks/delete/<int:pk>', deleteView.as_view(), name='delete_task'),

    path('/tasks-filter', searchView.as_view(), name='search'),

    path('/tasks/assignTask/<int:pk>', addppView.as_view(), name='add_people_task'),
    path('/tasks/assignTask/<int:pk>', addppView.as_view(), name='add_people'),

    path('/tasks/delete', deletecheckedView.as_view(), name='delete_checked'),

    # User
    path('/users/', userView.as_view(), name='user'),
    path('/users/', userView.as_view(), name='create_user'),

    path('/users/login', loginView.as_view(), name='login'),
    path('/users/login', loginView.as_view(), name='login_account'),

    path('/users/logout', logoutView.as_view(), name='logout'),
    path('/users/profile', profileView.as_view(), name='profile'),
]