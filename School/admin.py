from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    Utilisateur, StructureAcademique, Filiere, Classe,
    Cours, Materiel, Quiz, Question, ResultatQuiz,
    Forum, Discussion, Message, EmploiDuTemps
)

# Configuration de l'administrateur d'utilisateurs
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'nom')}),
        (_('Role'), {'fields': ('role',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email', 'nom')
    ordering = ('username',)

# Structure académique
class StructureAcademiqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_creation')
    search_fields = ('nom',)
    list_per_page = 20

class FiliereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'structure', 'date_creation')
    list_filter = ('structure',)
    search_fields = ('nom',)
    list_per_page = 20

class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'niveau', 'filiere', 'structure')
    list_filter = ('niveau', 'filiere', 'structure')
    search_fields = ('nom',)
    filter_horizontal = ('enseignants',)
    list_per_page = 20

# Gestion des cours
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'enseignant', 'is_active', 'date_creation')
    list_filter = ('enseignant', 'is_active')
    search_fields = ('titre', 'description')
    filter_horizontal = ('materiels', 'etudiants')
    list_per_page = 20

class MaterielAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type', 'date_creation')
    list_filter = ('type',)
    search_fields = ('titre',)
    list_per_page = 20

# Évaluation
class QuizAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cours', 'date_creation')
    list_filter = ('cours',)
    search_fields = ('titre',)
    filter_horizontal = ('questions',)
    list_per_page = 20

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('texte', 'reponse_correcte')
    search_fields = ('texte',)
    list_per_page = 20

class ResultatQuizAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'quiz', 'score')
    list_filter = ('quiz', 'etudiant')
    search_fields = ('etudiant__username', 'quiz__titre')
    list_per_page = 20

# Communication
class ForumAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_creation')
    search_fields = ('titre',)
    filter_horizontal = ('messages',)
    list_per_page = 20

class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_creation')
    filter_horizontal = ('participants', 'messages')
    list_per_page = 20

class MessageAdmin(admin.ModelAdmin):
    list_display = ('expediteur', 'contenu', 'date_envoi')
    list_filter = ('expediteur', 'date_envoi')
    search_fields = ('contenu', 'expediteur__username')
    list_per_page = 20

# Planning
class EmploiDuTempsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_creation')
    list_per_page = 20

# Enregistrement des modèles avec leurs configurations
# AUTHENTICATION AND AUTHORIZATION
admin.site.register(Utilisateur, CustomUserAdmin)

# STRUCTURE ACADÉMIQUE
admin.site.register(StructureAcademique, StructureAcademiqueAdmin)
admin.site.register(Filiere, FiliereAdmin)
admin.site.register(Classe, ClasseAdmin)

# GESTION DES COURS
admin.site.register(Cours, CoursAdmin)
admin.site.register(Materiel, MaterielAdmin)

# ÉVALUATION
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(ResultatQuiz, ResultatQuizAdmin)

# COMMUNICATION
admin.site.register(Forum, ForumAdmin)
admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Message, MessageAdmin)

# PLANNING
admin.site.register(EmploiDuTemps, EmploiDuTempsAdmin)

# Configuration des groupes de modèles pour Jazzmin
admin.site.site_header = "École en Ligne"
admin.site.site_title = "École en Ligne Admin"
admin.site.index_title = "Administration" 