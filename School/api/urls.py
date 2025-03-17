from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

router = DefaultRouter()
router.register(r'utilisateurs', views.UtilisateurViewSet, basename='utilisateur')
router.register(r'cours', views.CoursViewSet, basename='cours')
router.register(r'materiels', views.MaterielViewSet, basename='materiel')
router.register(r'quiz', views.QuizViewSet, basename='quiz')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'resultats-quiz', views.ResultatQuizViewSet, basename='resultat-quiz')
router.register(r'forums', views.ForumViewSet, basename='forum')
router.register(r'discussions', views.DiscussionViewSet, basename='discussion')
router.register(r'messages', views.MessageViewSet, basename='message')

# URLs de base de l'API
urlpatterns = [
    # API Routes
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # JWT Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] 