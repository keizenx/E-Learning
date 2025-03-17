from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import *

# Structure académique
@admin.register(StructureAcademique)
class StructureAcademiqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_creation')
    search_fields = ('nom',)
    list_per_page = 20

    def has_module_permission(self, request):
        # Vérifier si l'utilisateur est authentifié avant d'accéder à role
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.role == 'ACADEMIC'

@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'structure', 'date_creation')
    list_filter = ('structure',)
    search_fields = ('nom',)
    list_per_page = 20

    def has_module_permission(self, request):
        # Vérifier si l'utilisateur est authentifié avant d'accéder à role
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.role == 'ACADEMIC'

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'niveau', 'filiere', 'structure')
    list_filter = ('niveau', 'filiere', 'structure')
    search_fields = ('nom',)
    filter_horizontal = ('enseignants',)
    list_per_page = 20

    def has_module_permission(self, request):
        # Vérifier si l'utilisateur est authentifié avant d'accéder à role
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.role in ['ACADEMIC', 'TEACHER']

# Gestion des cours
@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'enseignant', 'is_active', 'date_creation')
    list_filter = ('enseignant', 'is_active')
    search_fields = ('titre', 'description')
    filter_horizontal = ('materiels', 'etudiants')
    list_per_page = 20

    def has_module_permission(self, request):
        # Vérifier si l'utilisateur est authentifié avant d'accéder à role
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.role in ['TEACHER', 'ACADEMIC']

@admin.register(Materiel)
class MaterielAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type', 'date_creation')
    list_filter = ('type',)
    search_fields = ('titre',)
    list_per_page = 20

    def has_module_permission(self, request):
        # Vérifier si l'utilisateur est authentifié avant d'accéder à role
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.role == 'TEACHER'

# Évaluation
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cours', 'date_creation')
    list_filter = ('cours',)
    search_fields = ('titre',)
    filter_horizontal = ('questions',)
    list_per_page = 20

    def has_module_permission(self, request):
        # Vérifier si l'utilisateur est authentifié avant d'accéder à role
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.role == 'TEACHER'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('texte', 'reponse_correcte')
    search_fields = ('texte',)
    list_per_page = 20

    def has_module_permission(self, request):
        # Vérifier si l'utilisateur est authentifié avant d'accéder à role
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.role == 'TEACHER'

@admin.register(ResultatQuiz)
class ResultatQuizAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'quiz', 'score')
    list_filter = ('quiz', 'etudiant')
    search_fields = ('etudiant__username', 'quiz__titre')
    list_per_page = 20

    def has_module_permission(self, request):
        # Vérifier si l'utilisateur est authentifié avant d'accéder à role
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.role in ['TEACHER', 'ACADEMIC']

# Communication
@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_creation')
    search_fields = ('titre',)
    filter_horizontal = ('messages',)
    list_per_page = 20

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_creation')
    filter_horizontal = ('participants', 'messages')
    list_per_page = 20

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('expediteur', 'contenu', 'date_envoi')
    list_filter = ('expediteur', 'date_envoi')
    search_fields = ('contenu', 'expediteur__username')
    list_per_page = 20

# Planning
@admin.register(EmploiDuTemps)
class EmploiDuTempsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_creation')
    list_per_page = 20

    def has_module_permission(self, request):
        # Vérifier si l'utilisateur est authentifié avant d'accéder à role
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.role in ['ACADEMIC', 'TEACHER'] 