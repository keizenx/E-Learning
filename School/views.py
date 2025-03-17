from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import View, ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db.models import Avg, Count
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import (
    Cours, Materiel, Quiz, Question, Utilisateur,
    Forum, Message, Discussion, ResultatQuiz, Classe
)
from datetime import datetime, date
from django.utils import timezone
import json
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponseRedirect

class LoginView(View):
    template_name = 'School/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('School:dashboard')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.role == 'TEACHER' and not user.is_approved:
                return render(request, self.template_name, {
                    'error': 'Votre compte est en attente d\'approbation par un administrateur.'
                })
            login(request, user)
            return redirect('School:dashboard')
        return render(request, self.template_name, {'error': 'Identifiants invalides'})

class RegisterView(View):
    template_name = 'School/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('School:dashboard')
        return render(request, self.template_name)

    def post(self, request):
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            nom = request.POST.get('nom')
            role = request.POST.get('role')

            # Validation
            if password1 != password2:
                messages.error(request, 'Les mots de passe ne correspondent pas')
                return render(request, self.template_name)

            if Utilisateur.objects.filter(username=username).exists():
                messages.error(request, 'Ce nom d\'utilisateur est déjà pris')
                return render(request, self.template_name)

            if Utilisateur.objects.filter(email=email).exists():
                messages.error(request, 'Cette adresse email est déjà utilisée')
                return render(request, self.template_name)

            # Création de l'utilisateur
            user = Utilisateur(
                username=username,
                email=email,
                nom=nom,
                role=role
            )
            user.set_password(password1)
            user.save()

            if role in ['TEACHER', 'ACADEMIC']:
                # Envoyer un email aux administrateurs
                admins = Utilisateur.objects.filter(role='ADMIN')
                if admins.exists():
                    admin_emails = [admin.email for admin in admins]
                    
                    subject = f'Nouvelle demande d\'inscription {user.get_role_display().lower()}'
                    context = {
                        'user': user,
                        'role': user.get_role_display(),
                        'approval_url': request.build_absolute_uri(
                            reverse('School:approve_user', kwargs={'user_id': str(user.id)})
                        )
                    }
                    message = render_to_string('School/email/user_approval_request.html', context)
                    
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        admin_emails,
                        fail_silently=True,
                    )
                    
                    messages.success(request, 'Votre compte a été créé avec succès! Un administrateur doit approuver votre compte avant que vous puissiez vous connecter.')
                    return redirect('School:login')
                else:
                    # Si aucun admin n'existe, approuver automatiquement
                    user.is_approved = True
                    user.save()
                    messages.success(request, 'Votre compte a été créé et approuvé automatiquement car aucun administrateur n\'est disponible.')
                    login(request, user)
                    return redirect('School:dashboard')

            # Connexion automatique pour les étudiants
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès!')
            return redirect('School:dashboard')

        except Exception as e:
            messages.error(request, f'Une erreur est survenue lors de la création du compte: {str(e)}')
            return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')
class ApproveUserView(View):
    def get(self, request, user_id):
        if request.user.role != 'ADMIN':
            messages.error(request, "Vous n'avez pas la permission d'approuver les utilisateurs.")
            return redirect('School:dashboard')
        
        user = get_object_or_404(Utilisateur, id=user_id)
        if user.role not in ['TEACHER', 'ACADEMIC']:
            messages.error(request, "Ce type d'utilisateur ne nécessite pas d'approbation.")
            return redirect('School:dashboard')

        user.is_approved = True
        user.save()
        
        # Envoyer un email à l'utilisateur
        subject = 'Votre compte a été approuvé'
        context = {
            'user': user,
            'role': user.get_role_display(),
            'login_url': request.build_absolute_uri(reverse('School:login'))
        }
        message = render_to_string('School/email/user_approved.html', context)
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
        
        messages.success(request, f"Le compte de {user.nom} ({user.get_role_display()}) a été approuvé avec succès.")
        return redirect('School:dashboard')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'School/password_reset.html'
    email_template_name = 'School/password_reset_email.html'
    success_url = reverse_lazy('School:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if not Utilisateur.objects.filter(email=email).exists():
            messages.error(self.request, 'Aucun compte n\'est associé à cette adresse email.')
            return self.form_invalid(form)

        user = Utilisateur.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = self.request.build_absolute_uri(
            reverse('School:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        )

        context = {
            'user': user,
            'reset_url': reset_url,
            'site_name': 'École en Ligne'
        }

        send_mail(
            'Réinitialisation de votre mot de passe - École en Ligne',
            render_to_string(self.email_template_name, context),
            'noreply@ecoleenligne.com',
            [email],
            fail_silently=False,
        )

        messages.success(self.request, 'Un email contenant les instructions de réinitialisation a été envoyé.')
        return redirect(self.success_url)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'School/password_reset_confirm.html'
    success_url = reverse_lazy('School:login')

    def form_valid(self, form):
        messages.success(self.request, 'Votre mot de passe a été réinitialisé avec succès.')
        return super().form_valid(form)

class DashboardView(LoginRequiredMixin, View):
    template_name = 'School/dashboard.html'

    def get(self, request):
        context = {}
        
        if request.user.role == 'ADMIN':
            # Récupérer les enseignants en attente d'approbation
            context['pending_teachers'] = Utilisateur.objects.filter(
                role='TEACHER',
                is_approved=False
            ).order_by('-date_joined')
            
            # Statistiques générales
            context['total_students'] = Utilisateur.objects.filter(role='STUDENT').count()
            context['total_teachers'] = Utilisateur.objects.filter(role='TEACHER', is_approved=True).count()
            context['total_courses'] = Cours.objects.count()
            
        elif request.user.role == 'TEACHER':
            if not request.user.is_approved:
                messages.warning(request, "Votre compte est en attente d'approbation par un administrateur.")
            context['my_courses'] = Cours.objects.filter(enseignant=request.user)
            context['total_students'] = sum(course.etudiants.count() for course in context['my_courses'])
            
        elif request.user.role == 'STUDENT':
            context['enrolled_courses'] = Cours.objects.filter(etudiants=request.user)
            context['available_courses'] = Cours.objects.exclude(etudiants=request.user).filter(is_active=True)
        
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class CoursListView(ListView):
    model = Cours
    template_name = 'School/cours_list.html'
    context_object_name = 'cours_list'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'STUDENT':
            return Cours.objects.filter(etudiants=user)
        elif user.role == 'TEACHER':
            return Cours.objects.filter(enseignant=user)
        return Cours.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Debug information
        print(f"User role: {user.role}")
        print(f"User ID: {user.id}")
        print(f"User name: {user.nom}")
        
        if user.role == 'TEACHER':
            # Récupérer les classes où l'utilisateur est enseignant
            classes = user.classes_enseignees.all()
            print(f"Teacher's classes count: {classes.count()}")
            print("Classes assigned to teacher:")
            for classe in classes:
                print(f"- {classe.nom} (ID: {classe.id})")
            context['classes'] = classes
        elif user.role == 'ADMIN':
            classes = Classe.objects.all()
            print(f"Total classes in system: {classes.count()}")
            print("All classes:")
            for classe in classes:
                print(f"- {classe.nom} (ID: {classe.id})")
            context['classes'] = classes
        else:
            context['classes'] = []
            print("User is a student, no classes to display")
        
        return context

@method_decorator(login_required, name='dispatch')
class CoursDetailView(DetailView):
    model = Cours
    template_name = 'School/cours/detail.html'
    context_object_name = 'cours'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = (
            self.request.user == self.object.enseignant or 
            self.request.user.role == 'ADMIN'
        )
        return context

@method_decorator(login_required, name='dispatch')
class CoursUpdateView(UpdateView):
    model = Cours
    template_name = 'School/cours/edit.html'
    fields = ['titre', 'description', 'classe']
    
    def get_success_url(self):
        return reverse('School:cours_detail', kwargs={'pk': self.object.id})
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.role == 'TEACHER':
            form.fields['classe'].queryset = self.request.user.classes_enseignees.all()
        return form

    def form_valid(self, form):
        if self.request.user != self.object.enseignant and self.request.user.role != 'ADMIN':
            messages.error(self.request, "Vous n'avez pas la permission de modifier ce cours.")
            return redirect('School:cours_detail', pk=self.object.id)
        messages.success(self.request, 'Cours modifié avec succès!')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class CoursDeleteView(DeleteView):
    model = Cours
    template_name = 'School/cours/delete.html'
    success_url = reverse_lazy('School:cours_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.enseignant and request.user.role != 'ADMIN':
            messages.error(request, "Vous n'avez pas la permission de supprimer ce cours.")
            return redirect('School:cours_detail', pk=self.object.id)
        messages.success(request, 'Cours supprimé avec succès!')
        return super().delete(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class CoursCreateView(CreateView):
    model = Cours
    template_name = 'School/cours/create.html'
    fields = ['titre', 'description', 'classe', 'image', 'video_url', 'is_active']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        
        # Debug pour voir les classes disponibles
        print(f"[DEBUG] User role: {user.role}")
        print(f"[DEBUG] User ID: {user.id}")
        print(f"[DEBUG] User name: {user.nom}")
        
        # Filtrer les classes en fonction du rôle de l'utilisateur
        if user.role == 'TEACHER':
            classes = user.classes_enseignees.all()
            print(f"[DEBUG] Classes enseignées ({classes.count()}):")
            for classe in classes:
                print(f"[DEBUG] - {classe.nom} (ID: {classe.id})")
            form.fields['classe'].queryset = classes
        elif user.role == 'ADMIN':
            classes = Classe.objects.all()
            print(f"[DEBUG] Toutes les classes ({classes.count()}):")
            for classe in classes:
                print(f"[DEBUG] - {classe.nom} (ID: {classe.id})")
            form.fields['classe'].queryset = classes
        else:
            form.fields['classe'].queryset = Classe.objects.none()
            print("[DEBUG] Aucune classe disponible (rôle non autorisé)")
        
        return form

    def form_valid(self, form):
        form.instance.enseignant = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Le cours a été créé avec succès!')
        return response

    def get_success_url(self):
        return reverse('School:cours_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Ajouter les classes au contexte en fonction du rôle de l'utilisateur
        if user.role == 'TEACHER':
            context['classes'] = user.classes_enseignees.all()
        elif user.role == 'ADMIN':
            context['classes'] = Classe.objects.all()
        else:
            context['classes'] = []
        
        return context

@method_decorator(login_required, name='dispatch')
class MaterielCreateView(View):
    template_name = 'School/materiel/create.html'

    def get(self, request, cours_id):
        cours = get_object_or_404(Cours, id=cours_id)
        
        if request.user != cours.enseignant and request.user.role != 'ADMIN':
            messages.error(request, "Vous n'avez pas la permission d'ajouter du matériel à ce cours.")
            return redirect('School:cours_detail', pk=cours_id)
            
        return render(request, self.template_name, {'cours': cours})

    def post(self, request, cours_id):
        cours = get_object_or_404(Cours, id=cours_id)
        
        if request.user != cours.enseignant and request.user.role != 'ADMIN':
            messages.error(request, "Vous n'avez pas la permission d'ajouter du matériel à ce cours.")
            return redirect('School:cours_detail', pk=cours_id)

        try:
            materiel = Materiel(
                titre=request.POST.get('titre'),
                description=request.POST.get('description', ''),
                cours_principal=cours,
                type=request.POST.get('type'),
                contenu=request.POST.get('contenu', '')
            )

            if request.FILES.get('fichier'):
                materiel.fichier = request.FILES['fichier']
            
            materiel.save()
            messages.success(request, 'Matériel ajouté avec succès!')
            return redirect('School:cours_detail', pk=cours_id)
            
        except Exception as e:
            messages.error(request, f"Erreur lors de l'ajout du matériel: {str(e)}")
            return render(request, self.template_name, {'cours': cours})

@method_decorator(login_required, name='dispatch')
class QuizCreateView(View):
    template_name = 'School/quiz/create.html'

    def get(self, request, cours_id):
        cours = get_object_or_404(Cours, id=cours_id)
        
        if request.user != cours.enseignant and request.user.role != 'ADMIN':
            messages.error(request, "Vous n'avez pas la permission de créer un quiz pour ce cours.")
            return redirect('School:cours_detail', pk=cours_id)
            
        return render(request, self.template_name, {'cours': cours})

    def post(self, request, cours_id):
        cours = get_object_or_404(Cours, id=cours_id)
        
        if request.user != cours.enseignant and request.user.role != 'ADMIN':
            messages.error(request, "Vous n'avez pas la permission de créer un quiz pour ce cours.")
            return redirect('School:cours_detail', pk=cours_id)

        quiz = Quiz.objects.create(
            titre=request.POST.get('titre'),
            description=request.POST.get('description', ''),
            cours=cours,
            date_limite=request.POST.get('date_limite', timezone.now() + timezone.timedelta(days=7)),
            duree=timezone.timedelta(minutes=int(request.POST.get('duree', 30)))
        )

        # Créer les questions
        questions_data = zip(
            request.POST.getlist('questions[]'),
            request.POST.getlist('reponses[]'),
            request.POST.getlist('reponse_correcte[]'),
            request.POST.getlist('type[]'),
            request.POST.getlist('points[]', [1] * len(request.POST.getlist('questions[]')))
        )

        for texte, reponses, reponse_correcte, type_question, points in questions_data:
            Question.objects.create(
                quiz_parent=quiz,
                texte=texte,
                reponses=reponses,
                reponse_correcte=reponse_correcte,
                type=type_question,
                points=points
            )

        messages.success(request, 'Quiz créé avec succès!')
        return redirect('School:cours_detail', pk=cours_id)

@method_decorator(login_required, name='dispatch')
class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'School/quiz_detail.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'score'):
            context['score'] = self.score
            context['total_questions'] = self.total_questions
            context['pourcentage'] = self.pourcentage
            context['quiz_complete'] = True
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        score = 0
        total_questions = self.object.questions.count()

        for question in self.object.questions.all():
            reponse_utilisateur = request.POST.get(f'question_{question.id}')
            if reponse_utilisateur == question.reponse_correcte:
                score += 1

        pourcentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        # Créer ou mettre à jour le résultat
        ResultatQuiz.objects.update_or_create(
            quiz=self.object,
            etudiant=request.user,
            defaults={'score': pourcentage}
        )
        
        # Stocker les résultats pour le contexte
        self.score = score
        self.total_questions = total_questions
        self.pourcentage = pourcentage
        
        return self.render_to_response(self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ForumListView(ListView):
    model = Forum
    template_name = 'School/forum/list.html'
    context_object_name = 'forums'
    ordering = ['-date_creation']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupérer les messages récents avec leurs forums associés
        context['recent_messages'] = Message.objects.filter(forum__isnull=False).prefetch_related('forum').select_related('expediteur').order_by('-date_envoi')[:5]
        return context

@method_decorator(login_required, name='dispatch')
class ForumDetailView(DetailView):
    model = Forum
    template_name = 'School/forum/detail.html'
    context_object_name = 'forum'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = self.object.messages.all().order_by('-date_envoi')
        context['messages'] = messages
        # Calculer le nombre de participants uniques
        participants = set(message.expediteur for message in messages)
        context['participants_count'] = len(participants)
        return context

    def post(self, request, *args, **kwargs):
        forum = self.get_object()
        contenu = request.POST.get('contenu')
        if contenu:
            forum.creerMessage(contenu=contenu, expediteur=request.user)
            messages.success(request, 'Message posté avec succès!')
        return redirect('School:forum_detail', pk=forum.id)

@method_decorator(login_required, name='dispatch')
class ForumCreateView(CreateView):
    model = Forum
    template_name = 'School/forum/create.html'
    fields = ['titre', 'description', 'cours']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        if user.role == 'STUDENT':
            # Les étudiants ne peuvent associer que les cours auxquels ils sont inscrits
            form.fields['cours'].queryset = Cours.objects.filter(etudiants=user)
        elif user.role == 'TEACHER':
            # Les enseignants ne peuvent associer que leurs propres cours
            form.fields['cours'].queryset = Cours.objects.filter(enseignant=user)
        elif user.role == 'ADMIN':
            # Les administrateurs peuvent voir tous les cours
            form.fields['cours'].queryset = Cours.objects.all()
        return form

    def form_valid(self, form):
        form.instance.createur = self.request.user
        messages.success(self.request, 'Le forum a été créé avec succès!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('School:forum_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class MessageReplyView(View):
    def post(self, request, forum_id, message_id):
        forum = get_object_or_404(Forum, id=forum_id)
        message_parent = get_object_or_404(Message, id=message_id)
        contenu = request.POST.get('contenu')
        
        if contenu:
            forum.repondre(
                message_parent=message_parent,
                contenu=contenu,
                expediteur=request.user
            )
            messages.success(request, 'Réponse postée avec succès!')
        
        return redirect('School:forum_detail', pk=forum_id)

@method_decorator(login_required, name='dispatch')
class DiscussionListView(ListView):
    model = Discussion
    template_name = 'School/forum/discussions.html'
    context_object_name = 'discussions'

    def get_queryset(self):
        return Discussion.objects.filter(participants=self.request.user)

@method_decorator(login_required, name='dispatch')
class DiscussionDetailView(DetailView):
    model = Discussion
    template_name = 'School/forum/discussion_detail.html'
    context_object_name = 'discussion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.messages.all().order_by('date_envoi')
        return context

    def post(self, request, *args, **kwargs):
        discussion = self.get_object()
        contenu = request.POST.get('contenu')
        if contenu:
            message = Message.objects.create(
                contenu=contenu,
                expediteur=request.user
            )
            discussion.envoyerMessage(message)
            messages.success(request, 'Message envoyé avec succès!')
        return redirect('School:discussion_detail', pk=discussion.id)

@method_decorator(login_required, name='dispatch')
class DiscussionCreateView(View):
    def post(self, request):
        participant_ids = request.POST.getlist('participants')
        if participant_ids:
            discussion = Discussion.objects.create()
            discussion.participants.add(request.user)
            discussion.participants.add(*Utilisateur.objects.filter(id__in=participant_ids))
            messages.success(request, 'Discussion créée avec succès!')
            return redirect('School:discussion_detail', pk=discussion.id)
        messages.error(request, 'Veuillez sélectionner au moins un participant.')
        return redirect('School:discussion_list')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('School:login')
    http_method_names = ['get', 'post']  # Allow both GET and POST methods

class HomeView(TemplateView):
    template_name = 'School/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['role'] = self.request.user.role
        return context 

@method_decorator(login_required, name='dispatch')
class MaterielUpdateView(UpdateView):
    model = Materiel
    template_name = 'School/materiel/edit.html'
    fields = ['titre', 'description', 'type', 'contenu', 'fichier']

    def get_success_url(self):
        return reverse('School:cours_detail', kwargs={'pk': self.object.cours_principal.id})

    def form_valid(self, form):
        if self.request.user != self.object.cours_principal.enseignant and self.request.user.role != 'ADMIN':
            messages.error(self.request, "Vous n'avez pas la permission de modifier ce matériel.")
            return redirect('School:cours_detail', pk=self.object.cours_principal.id)
        messages.success(self.request, 'Matériel modifié avec succès!')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class MaterielDeleteView(DeleteView):
    model = Materiel
    template_name = 'School/materiel/delete.html'

    def get_success_url(self):
        return reverse('School:cours_detail', kwargs={'pk': self.object.cours_principal.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.cours_principal.enseignant and request.user.role != 'ADMIN':
            messages.error(request, "Vous n'avez pas la permission de supprimer ce matériel.")
            return redirect('School:cours_detail', pk=self.object.cours_principal.id)
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Matériel supprimé avec succès!')
        return HttpResponseRedirect(success_url)

@method_decorator(login_required, name='dispatch')
class QuizUpdateView(UpdateView):
    model = Quiz
    template_name = 'School/quiz/edit.html'
    fields = ['titre', 'description', 'date_limite', 'duree']

    def get_success_url(self):
        return reverse('School:cours_detail', kwargs={'pk': self.object.cours.id})

    def form_valid(self, form):
        if self.request.user != self.object.cours.enseignant and self.request.user.role != 'ADMIN':
            messages.error(self.request, "Vous n'avez pas la permission de modifier ce quiz.")
            return redirect('School:cours_detail', pk=self.object.cours.id)
        messages.success(self.request, 'Quiz modifié avec succès!')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class QuizDeleteView(DeleteView):
    model = Quiz
    template_name = 'School/quiz/delete.html'

    def get_success_url(self):
        return reverse('School:cours_detail', kwargs={'pk': self.object.cours.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.cours.enseignant and request.user.role != 'ADMIN':
            messages.error(request, "Vous n'avez pas la permission de supprimer ce quiz.")
            return redirect('School:cours_detail', pk=self.object.cours.id)
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Quiz supprimé avec succès!')
        return HttpResponseRedirect(success_url)

@method_decorator(login_required, name='dispatch')
class ForumUpdateView(UpdateView):
    model = Forum
    template_name = 'School/forum/edit.html'
    fields = ['titre', 'description', 'cours']

    def get_success_url(self):
        return reverse('School:forum_detail', kwargs={'pk': self.object.id})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.role == 'TEACHER':
            form.fields['cours'].queryset = Cours.objects.filter(enseignant=self.request.user)
        return form

    def form_valid(self, form):
        if self.request.user.role not in ['TEACHER', 'ADMIN']:
            messages.error(self.request, "Vous n'avez pas la permission de modifier ce forum.")
            return redirect('School:forum_detail', pk=self.object.id)
        messages.success(self.request, 'Forum modifié avec succès!')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class ForumDeleteView(DeleteView):
    model = Forum
    template_name = 'School/forum/delete.html'
    success_url = reverse_lazy('School:forum_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.role not in ['TEACHER', 'ADMIN']:
            messages.error(request, "Vous n'avez pas la permission de supprimer ce forum.")
            return redirect('School:forum_detail', pk=self.object.id)
        messages.success(request, 'Forum supprimé avec succès!')
        return super().delete(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ProfileView(UpdateView):
    model = Utilisateur
    template_name = 'School/profile.html'
    fields = ['nom', 'email']
    success_url = reverse_lazy('School:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profil mis à jour avec succès!')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class TeacherClassesView(View):
    template_name = 'School/teacher_classes.html'

    def get(self, request):
        if request.user.role != 'TEACHER':
            messages.error(request, "Vous n'avez pas accès à cette page.")
            return redirect('School:dashboard')

        classes = request.user.classes_enseignees.all()
        print(f"\nClasses de l'enseignant {request.user.nom}:")
        for classe in classes:
            print(f"- {classe.nom} (ID: {classe.id})")
            print(f"  Enseignants de cette classe:")
            for enseignant in classe.enseignants.all():
                print(f"    * {enseignant.nom} (ID: {enseignant.id})")

        context = {
            'classes': classes
        }
        return render(request, self.template_name, context)

class CoursInscriptionView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cours = get_object_or_404(Cours, id=pk)
        if request.user.role == 'STUDENT':
            cours.etudiants.add(request.user)
            messages.success(request, f'Vous êtes maintenant inscrit au cours "{cours.titre}"')
        else:
            messages.error(request, 'Seuls les étudiants peuvent s\'inscrire aux cours')
        return redirect('School:dashboard') 