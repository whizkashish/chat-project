from django.urls import path
from . import views as chat_views

urlpatterns = [
    path('create_group_chat/', chat_views.create_group_chat_room, name='create_group_chat'),
    path('create_one_to_one_chat/<slug:username>/', chat_views.create_one_to_one_chat_room, name='create_one_to_one_chat'),
    path('chat_room/<uuid:room_id>/', chat_views.chat_room, name='chat_room'),
]
