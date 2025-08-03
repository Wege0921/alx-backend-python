from django.urls import path
from .views import delete_user
from django.urls import path
from .views import cached_message_list

urlpatterns = [
    path('delete-account/', delete_user, name='delete_user'),
    path('messages/', cached_message_list, name='cached_message_list'),
]
