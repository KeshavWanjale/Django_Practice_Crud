from django.urls import path
from .views import *

urlpatterns = [

    path('', greet, name = 'greet'),
    path('users', user_crud, name = 'user_crud'),
    path('users/<int:user_id>', user_crud, name = 'user_crud'),
    # path('get-users/', get_users, name = 'get_users'),
    # path('create/', create_user, name = 'get_users'),
    # path('update/<int:contact_id>', update_user, name = 'update_user'),
    # path('delete/<int:contact_id>', delete_user, name = 'delete_user'),

] 