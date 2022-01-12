from django.urls import path
from core.views import create_user,update_user

urlpatterns = [
    path('', create_user, name='create-user'),

    path('update/<int:user_id>', update_user, name='update-user')
]