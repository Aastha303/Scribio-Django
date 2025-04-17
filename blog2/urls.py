from django.urls import path
from . import views

app_name = 'profiles'  # <-- Add this line for namespacing

# blog2/urls.py
urlpatterns = [
    path('<str:username>/followers/', views.FollowersListView.as_view(), name='followers-list'),
    path('<str:username>/following/', views.FollowingListView.as_view(), name='following-list'),
    path('<str:username>/follow/', views.follow_toggle, name='follow-toggle'),
    path('chatbot', views.chatbot_view, name='chatbot'),
    path('chat/', views.chat_page, name='chat_page'),
]
