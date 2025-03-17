from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    Utilisateur, StructureAcademique, Filiere, Classe,
    Cours, Materiel, Quiz, Question, ResultatQuiz,
    Forum, Discussion, Message, EmploiDuTemps
)

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
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('username', 'password1', 'password2', 'role')}),)
    search_fields = ('username', 'first_name', 'last_name', 'email', 'nom')
    ordering = ('username',)

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ('nom',)

class CoursAdmin(BaseAdmin):
    list_display = ('titre', 'enseignant', 'is_active', 'date_creation')
    list_filter = ('enseignant', 'is_active')
    filter_horizontal = ('materiels', 'etudiants')

class QuizAdmin(BaseAdmin):
    list_display = ('titre', 'cours', 'date_creation')
    list_filter = ('cours',)
    filter_horizontal = ('questions',)

class ResultatQuizAdmin(BaseAdmin):
    list_display = ('etudiant', 'quiz', 'score')
    list_filter = ('quiz', 'etudiant')
    search_fields = ('etudiant__username', 'quiz__titre')

class MessageAdmin(BaseAdmin):
    list_display = ('expediteur', 'contenu', 'date_envoi')
    list_filter = ('expediteur', 'date_envoi')
    search_fields = ('contenu', 'expediteur__username')

MODELS_ADMINS = {
    Utilisateur: CustomUserAdmin,
    StructureAcademique: BaseAdmin,
    Filiere: BaseAdmin,
    Classe: BaseAdmin,
    Cours: CoursAdmin,
    Materiel: BaseAdmin,
    Quiz: QuizAdmin,
    Question: BaseAdmin,
    ResultatQuiz: ResultatQuizAdmin,
    Forum: BaseAdmin,
    Discussion: BaseAdmin,
    Message: MessageAdmin,
    EmploiDuTemps: BaseAdmin
}

for model, admin_class in MODELS_ADMINS.items():
    admin.site.register(model, admin_class)

admin.site.site_header = "École en Ligne"
admin.site.site_title = "École en Ligne Admin"
admin.site.index_title = "Administration"