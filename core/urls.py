from django.urls import path
from core.views import create_user,update_user, list_sales_user

urlpatterns = [
    path('', create_user, name='create-user'),
    path('users/list', list_sales_user, name='list-users'),
    path('update/<int:user_id>', update_user, name='update-user')
]