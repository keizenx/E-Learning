from django import views
from django.urls import path

from django.contrib.auth.views import LogoutView
from .views import (
    LoginView, DashboardView, 
    CoursListView, CoursDetailView, CoursCreateView,
    MaterielCreateView, QuizCreateView, QuizDetailView,
    ForumListView, ForumDetailView, ForumCreateView,
    MessageReplyView, DiscussionListView, DiscussionDetailView,
    DiscussionCreateView
)
from . import views

app_name = 'School'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='School:login'), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # Cours
    path('cours/', CoursListView.as_view(), name='cours_list'),
    path('cours/<uuid:pk>/', CoursDetailView.as_view(), name='cours_detail'),
    path('cours/create/', CoursCreateView.as_view(), name='cours_create'),
    
    # Matériels
    path('cours/<uuid:cours_id>/materiel/create/', MaterielCreateView.as_view(), name='materiel_create'),
    
    # Quiz
    path('cours/<uuid:cours_id>/quiz/create/', QuizCreateView.as_view(), name='quiz_create'),
    path('quiz/<uuid:pk>/', QuizDetailView.as_view(), name='quiz_detail'),

    # Forum
    path('forum/', ForumListView.as_view(), name='forum_list'),
    path('forum/create/', ForumCreateView.as_view(), name='forum_create'),
    path('forum/<uuid:pk>/', ForumDetailView.as_view(), name='forum_detail'),
    path('forum/<uuid:forum_id>/message/<uuid:message_id>/reply/', 
         MessageReplyView.as_view(), name='message_reply'),

    # Discussions privées
    path('discussions/', DiscussionListView.as_view(), name='discussion_list'),
    path('discussions/create/', DiscussionCreateView.as_view(), name='discussion_create'),
    path('discussions/<uuid:pk>/', DiscussionDetailView.as_view(), name='discussion_detail'),
] 