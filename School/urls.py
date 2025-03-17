from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    LoginView, DashboardView, HomeView,
    CoursListView, CoursDetailView, CoursCreateView, CoursUpdateView, CoursDeleteView,
    MaterielCreateView, MaterielUpdateView, MaterielDeleteView,
    QuizCreateView, QuizDetailView, QuizUpdateView, QuizDeleteView,
    ForumListView, ForumDetailView, ForumCreateView, ForumUpdateView, ForumDeleteView,
    MessageReplyView, DiscussionListView, DiscussionDetailView,
    DiscussionCreateView, CustomLogoutView, RegisterView,
    CustomPasswordResetView, CustomPasswordResetConfirmView,
    ApproveUserView, ProfileView, TeacherClassesView, CoursInscriptionView
)

app_name = 'School'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('approve-user/<uuid:user_id>/', ApproveUserView.as_view(), name='approve_user'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # Cours
    path('cours/', CoursListView.as_view(), name='cours_list'),
    path('cours/create/', CoursCreateView.as_view(), name='cours_create'),
    path('cours/<uuid:pk>/', CoursDetailView.as_view(), name='cours_detail'),
    path('cours/<uuid:pk>/edit/', CoursUpdateView.as_view(), name='cours_edit'),
    path('cours/<uuid:pk>/delete/', CoursDeleteView.as_view(), name='cours_delete'),
    path('cours/<uuid:pk>/inscription/', CoursInscriptionView.as_view(), name='cours_inscription'),
    
    # Matériels
    path('cours/<uuid:cours_id>/materiel/create/', MaterielCreateView.as_view(), name='materiel_create'),
    path('materiel/<uuid:pk>/edit/', MaterielUpdateView.as_view(), name='materiel_edit'),
    path('materiel/<uuid:pk>/delete/', MaterielDeleteView.as_view(), name='materiel_delete'),
    
    # Quiz
    path('cours/<uuid:cours_id>/quiz/create/', QuizCreateView.as_view(), name='quiz_create'),
    path('quiz/<uuid:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('quiz/<uuid:pk>/edit/', QuizUpdateView.as_view(), name='quiz_edit'),
    path('quiz/<uuid:pk>/delete/', QuizDeleteView.as_view(), name='quiz_delete'),
    
    # Forum
    path('forum/', ForumListView.as_view(), name='forum_list'),
    path('forum/create/', ForumCreateView.as_view(), name='forum_create'),
    path('forum/<uuid:pk>/', ForumDetailView.as_view(), name='forum_detail'),
    path('forum/<uuid:pk>/edit/', ForumUpdateView.as_view(), name='forum_edit'),
    path('forum/<uuid:pk>/delete/', ForumDeleteView.as_view(), name='forum_delete'),
    path('forum/<uuid:forum_id>/message/<uuid:message_id>/reply/', MessageReplyView.as_view(), name='message_reply'),

    # Discussion
    path('discussion/', DiscussionListView.as_view(), name='discussion_list'),
    path('discussion/create/', DiscussionCreateView.as_view(), name='discussion_create'),
    path('discussion/<uuid:pk>/', DiscussionDetailView.as_view(), name='discussion_detail'),

    # Profile URL
    path('profile/', ProfileView.as_view(), name='profile'),

    # Teacher Classes
    path('classes/', TeacherClassesView.as_view(), name='teacher_classes'),
] 