from django.urls import path , include
from chat.views import *

urlpatterns = [
    path('chat_view/', view=chat_view, name = "chat_view"),
    path('chat/<str:username>/', view=chat_room, name='chat')
]