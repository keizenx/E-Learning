"""
URL configuration for school_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.models import User
from School.models import Utilisateur
from rest_framework import routers, serializers, viewsets
from School.viewsets import (
    StructureAcademiqueViewSet, FiliereViewSet, ClasseViewSet, UtilisateurViewSet, 
    DiscussionViewSet, MessageViewSet, ForumViewSet, QuizViewSet, QuestionViewSet, 
    CoursViewSet, MaterielViewSet, EmploiDuTempsViewSet, ResultatQuizViewSet
)
from rest_framework.permissions import IsAuthenticated
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuration du routeur DRF
router = routers.DefaultRouter()
router.register(r'structures', StructureAcademiqueViewSet)
router.register(r'filieres', FiliereViewSet)
router.register(r'classes', ClasseViewSet)
router.register(r'utilisateurs', UtilisateurViewSet)
router.register(r'discussions', DiscussionViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'forums', ForumViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'cours', CoursViewSet)
router.register(r'materiels', MaterielViewSet)
router.register(r'emplois-du-temps', EmploiDuTempsViewSet)
router.register(r'resultats-quizz', ResultatQuizViewSet)

# Vue pour générer la documentation Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API School Management",
        default_version='v1',
        description="Documentation de l'API pour la gestion scolaire",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@school.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(IsAuthenticated,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('School.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
