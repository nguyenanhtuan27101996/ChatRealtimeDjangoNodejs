from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.show_index_page, name='show_index_page'),
    path('accounts/signup/', views.signup_account, name='sign_up'),
    path('accounts/login/', views.login_account, name='login'),
    path('home/', views.show_home_page, name='show_home_page'),
    path('accounts/logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('ajax/create-room-chat', views.create_room_chat, name='create_room_chat'),
    path('show-roow-chat/<int:id>/', views.show_room_chat, name='show_room_chat'),
    path('ajax/exit_room_chat', views.exit_room_chat, name='exit_room_chat'),
    path('ajax/create_reply_of_room_chat/', views.create_reply_of_room_chat, name='create_reply_of_room_chat'),
    path('<str:username>/', views.show_personal_page, name='show_personal_page'),
    path('ajax/create_conversation_reply/', views.create_conversation_reply, name='create_conversation_reply'),
]
