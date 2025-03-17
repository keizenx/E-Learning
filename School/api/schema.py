from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="E-Learning API",
        default_version='v1',
        description="""
API de la plateforme E-Learning.

Cette API permet de gérer :
- Les utilisateurs (étudiants, enseignants, administrateurs)
- Les cours et leurs matériels
- Les quiz et leurs résultats
- Les forums et discussions

## Authentification

L'API utilise l'authentification par session et Basic Auth. Pour utiliser l'API :
1. Connectez-vous via le formulaire de connexion (/api-auth/login/)
2. Ou utilisez l'authentification Basic avec vos identifiants

## Permissions

- Les utilisateurs doivent être authentifiés pour accéder à l'API
- Les enseignants ont accès à leurs propres cours et ressources
- Les étudiants ont accès aux cours auxquels ils sont inscrits
- Les administrateurs ont accès à toutes les ressources
        """,
        terms_of_service="https://www.e-learning.com/terms/",
        contact=openapi.Contact(email="contact@e-learning.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] 