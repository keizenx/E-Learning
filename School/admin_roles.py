from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.urls import path
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login
from .models import *
from .forms import RoleBasedAuthenticationForm

class AdminUtilisateurAdmin(UserAdmin):
    """Panel administrateur principal"""
    list_display = ('username', 'email', 'nom', 'role', 'is_active', 'last_login')
    list_filter = ('role', 'is_active', 'groups')
    search_fields = ('username', 'email', 'nom')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informations personnelles'), {'fields': ('email', 'nom', 'role')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Dates importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'nom', 'role'),
        }),
    )

class ResponsableScolariteAdmin(UserAdmin):
    """Panel responsable académique"""
    list_display = ('username', 'email', 'nom', 'role')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email', 'nom')
    ordering = ('username',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(role__in=['STUDENT', 'TEACHER'])
        return qs
    
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        
        return (
            (None, {'fields': ('username', 'password')}),
            (_('Informations personnelles'), {'fields': ('email', 'nom', 'role')}),
            (_('Statut'), {'fields': ('is_active',)}),
            (_('Affectations'), {
                'fields': ('classes_enseignees', 'cours_suivis'),
                'description': 'Affectation aux classes et cours'
            }),
        )
    
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.role == 'ACADEMIC'

class EnseignantAdmin(UserAdmin):
    """Panel enseignant"""
    list_display = ('username', 'email', 'nom', 'matieres_display', 'classes_display')
    list_filter = ('classes_enseignees', 'cours_enseignes')
    search_fields = ('username', 'email', 'nom')
    ordering = ('username',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.role == 'TEACHER':
            return qs.filter(cours_enseignes__enseignant=request.user).distinct()
        return qs
    
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        
        return (
            (None, {'fields': ('username', 'password')}),
            (_('Informations du cours'), {
                'fields': ('cours_enseignes', 'materiels'),
                'description': 'Gestion des cours et matériels'
            }),
            (_('Évaluation'), {
                'fields': ('quiz_crees', 'resultats_quiz'),
                'description': 'Gestion des évaluations'
            }),
        )
    
    def matieres_display(self, obj):
        return ", ".join([cours.titre for cours in obj.cours_enseignes.all()])
    matieres_display.short_description = "Matières enseignées"
    
    def classes_display(self, obj):
        return ", ".join([str(classe) for classe in obj.classes_enseignees.all()])
    classes_display.short_description = "Classes"
    
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.role == 'TEACHER'

class EtudiantAdmin(UserAdmin):
    """Panel étudiant"""
    list_display = ('username', 'email', 'nom', 'classe_display', 'moyenne_display')
    list_filter = ('cours_suivis', 'role')
    search_fields = ('username', 'email', 'nom')
    ordering = ('username',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.role == 'STUDENT':
            return qs.filter(id=request.user.id)
        return qs.filter(role='STUDENT')
    
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        
        return (
            (None, {'fields': ('username', 'password')}),
            (_('Informations personnelles'), {'fields': ('email', 'nom')}),
            (_('Cours'), {
                'fields': ('cours_suivis',),
                'description': 'Cours suivis'
            }),
            (_('Résultats'), {
                'fields': ('resultats_quiz',),
                'description': 'Résultats des évaluations'
            }),
        )
    
    def classe_display(self, obj):
        return ", ".join([str(cours) for cours in obj.cours_suivis.all()])
    classe_display.short_description = "Cours suivis"
    
    def moyenne_display(self, obj):
        resultats = obj.resultats_quiz.all()
        if not resultats:
            return "Pas de résultats"
        moyenne = sum(r.score for r in resultats) / len(resultats)
        return f"{moyenne:.2f}/20"
    moyenne_display.short_description = "Moyenne générale"
    
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.role in ['ACADEMIC', 'TEACHER'] or (request.user.role == 'STUDENT' and request.user.id == self.id)

# Configuration du site d'administration par rôle
class RoleBasedAdminSite(admin.AdminSite):
    site_header = "École en Ligne - Administration"
    site_title = "École en Ligne"
    index_title = "Administration de l'École en Ligne"
    login_form = RoleBasedAuthenticationForm

    def get_app_list(self, request):
        user = request.user
        if not user.is_authenticated:
            return []
        
        app_list = super().get_app_list(request)
        
        if user.role == 'ACADEMIC':
            # Filtrer les applications pour le responsable académique
            allowed_models = ['utilisateur', 'classe', 'cours']
            app_list = [
                app for app in app_list
                if any(model['object_name'].lower() in allowed_models
                      for model in app['models'])
            ]
        elif user.role == 'TEACHER':
            # Filtrer les applications pour l'enseignant
            allowed_models = ['cours', 'materiel', 'quiz']
            app_list = [
                app for app in app_list
                if any(model['object_name'].lower() in allowed_models
                      for model in app['models'])
            ]
        
        return app_list

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        if not request.user.is_authenticated:
            return redirect('admin:login')
            
        context = {
            'user': request.user,
            'role': request.user.get_role_display(),
            **self.each_context(request),
        }
        
        template_name = 'admin/base_dashboard.html'
        
        if request.user.role == 'ACADEMIC':
            template_name = 'admin/dashboard_academic.html'
            context.update({
                'total_students': Utilisateur.objects.filter(role='STUDENT').count(),
                'total_teachers': Utilisateur.objects.filter(role='TEACHER').count(),
                'total_courses': Cours.objects.count(),
            })
        elif request.user.role == 'TEACHER':
            template_name = 'admin/dashboard_teacher.html'
            context.update({
                'my_courses': Cours.objects.filter(enseignant=request.user),
                'my_students': Utilisateur.objects.filter(cours_suivis__enseignant=request.user).distinct(),
            })
        elif request.user.role == 'STUDENT':
            template_name = 'admin/dashboard_student.html'
            context.update({
                'my_courses': request.user.cours_suivis.all(),
                'my_results': request.user.resultats_quiz.all().order_by('-date_soumission'),
            })
            
        return TemplateResponse(request, template_name, context)

    def index(self, request, extra_context=None):
        return redirect('admin:dashboard')

    def login(self, request, extra_context=None):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin:index')
        
        context = {
            'title': 'Connexion',
            'subtitle': 'Administration',
            **(extra_context or {})
        }
        
        return super().login(request, extra_context=context)

# Création de l'instance d'administration
role_admin = RoleBasedAdminSite(name='role_admin')

# Désenregistrement des modèles du site d'administration par défaut
try:
    admin.site.unregister(Group)
    admin.site.unregister(Utilisateur)
except admin.sites.NotRegistered:
    pass

# Enregistrement des modèles avec leurs classes d'administration spécifiques
role_admin.register(Utilisateur, AdminUtilisateurAdmin)
role_admin.register(Group, GroupAdmin)

# Enregistrement des autres modèles
from .admin import (
    StructureAcademiqueAdmin, FiliereAdmin, ClasseAdmin,
    CoursAdmin, MaterielAdmin, QuizAdmin, QuestionAdmin,
    ResultatQuizAdmin, ForumAdmin, DiscussionAdmin,
    MessageAdmin, EmploiDuTempsAdmin
)

role_admin.register(StructureAcademique, StructureAcademiqueAdmin)
role_admin.register(Filiere, FiliereAdmin)
role_admin.register(Classe, ClasseAdmin)
role_admin.register(Cours, CoursAdmin)
role_admin.register(Materiel, MaterielAdmin)
role_admin.register(Quiz, QuizAdmin)
role_admin.register(Question, QuestionAdmin)
role_admin.register(ResultatQuiz, ResultatQuizAdmin)
role_admin.register(Forum, ForumAdmin)
role_admin.register(Discussion, DiscussionAdmin)
role_admin.register(Message, MessageAdmin)
role_admin.register(EmploiDuTemps, EmploiDuTempsAdmin) 