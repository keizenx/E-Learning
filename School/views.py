from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import View, ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
from django.db.models import Avg, Count
from .models import (
    Cours, Materiel, Quiz, Question, Utilisateur,
    Forum, Message, Discussion, ResultatQuiz
)
from datetime import datetime, date
from django.utils import timezone
import json

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
            login(request, user)
            return redirect('School:dashboard')
        return render(request, self.template_name, {'error': 'Identifiants invalides'})

@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'School/dashboard.html'

    def get(self, request):
        user = request.user
        context = {
            'user': user,
            'role': user.role
        }

        # Statistiques communes
        context['date_aujourdhui'] = date.today()

        if user.role == 'STUDENT':
            # Statistiques pour les étudiants
            cours_inscrits = Cours.objects.filter(etudiants=user, is_active=True)
            resultats_quiz = ResultatQuiz.objects.filter(etudiant=user)
            
            context.update({
                'cours_inscrits': cours_inscrits.count(),
                'quiz_a_faire': Quiz.objects.filter(cours__in=cours_inscrits).exclude(
                    resultats__etudiant=user
                ).count(),
                'moyenne_generale': resultats_quiz.aggregate(
                    avg=Avg('score')
                )['avg'] or 0,
            })

        elif user.role == 'TEACHER':
            # Statistiques pour les enseignants
            context.update({
                'total_cours': Cours.objects.filter(enseignant=user).count(),
                'total_etudiants': Utilisateur.objects.filter(
                    role='STUDENT',
                    cours_suivis__enseignant=user
                ).distinct().count(),
                'total_quiz': Quiz.objects.filter(cours__enseignant=user).count(),
            })

        elif user.role in ['ADMIN', 'ACADEMIC']:
            # Statistiques pour les administrateurs
            context.update({
                'total_etudiants': Utilisateur.objects.filter(role='STUDENT').count(),
                'total_enseignants': Utilisateur.objects.filter(role='TEACHER').count(),
                'total_cours': Cours.objects.all().count(),
            })

        # Activités récentes (pour tous les rôles)
        activites = []
        
        # Nouveaux cours
        nouveaux_cours = Cours.objects.filter(
            is_active=True
        ).order_by('-date_creation')[:3]
        for cours in nouveaux_cours:
            activites.append({
                'type': 'cours',
                'message': f'Nouveau cours disponible : "{cours.titre}"',
                'date': cours.date_creation
            })

        # Quiz complétés (pour les étudiants)
        if user.role == 'STUDENT':
            quiz_completes = Quiz.objects.filter(
                resultats__etudiant=user
            ).order_by('-resultats__date_completion')[:3]
            for quiz in quiz_completes:
                activites.append({
                    'type': 'quiz',
                    'message': f'Quiz "{quiz.titre}" complété',
                    'date': quiz.resultats.get(etudiant=user).date_completion
                })

        # Trier les activités par date
        activites.sort(key=lambda x: x['date'], reverse=True)
        context['activites'] = activites[:5]  # Garder les 5 plus récentes

        # Emploi du temps
        emploi_du_temps = [
            {
                'debut': '09:00',
                'fin': '10:30',
                'cours': 'Mathématiques',
                'salle': 'Salle 101'
            },
            {
                'debut': '11:00',
                'fin': '12:30',
                'cours': 'Physique',
                'salle': 'Salle 203'
            },
            {
                'debut': '14:00',
                'fin': '15:30',
                'cours': 'Informatique',
                'salle': 'Salle Info 1'
            }
        ]
        context['emploi_du_temps'] = emploi_du_temps

        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class CoursListView(ListView):
    model = Cours
    template_name = 'School/cours_list.html'
    context_object_name = 'cours_list'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'STUDENT':
            # Pour les étudiants, montrer seulement les cours actifs
            return Cours.objects.filter(is_active=True)
        elif user.role == 'TEACHER':
            # Pour les enseignants, montrer leurs cours
            return Cours.objects.filter(enseignant=user)
        else:
            # Pour les admins et responsables académiques, montrer tous les cours
            return Cours.objects.all()

@method_decorator(login_required, name='dispatch')
class CoursDetailView(DetailView):
    model = Cours
    template_name = 'School/cours_detail.html'
    context_object_name = 'cours'

@method_decorator(login_required, name='dispatch')
class CoursCreateView(View):
    def post(self, request):
        if request.user.role not in ['TEACHER', 'ADMIN']:
            messages.error(request, "Vous n'avez pas la permission de créer un cours.")
            return redirect('School:cours_list')

        titre = request.POST.get('titre')
        description = request.POST.get('description')
        is_active = request.POST.get('is_active') == 'on'

        cours = Cours.objects.create(
            titre=titre,
            description=description,
            enseignant=request.user,
            is_active=is_active
        )

        messages.success(request, 'Cours créé avec succès!')
        return redirect('School:cours_detail', pk=cours.id)

@method_decorator(login_required, name='dispatch')
class MaterielCreateView(View):
    def post(self, request, cours_id):
        cours = get_object_or_404(Cours, id=cours_id)
        
        if request.user != cours.enseignant and request.user.role != 'ADMIN':
            messages.error(request, "Vous n'avez pas la permission d'ajouter du matériel à ce cours.")
            return redirect('School:cours_detail', pk=cours_id)

        materiel = Materiel.objects.create(
            titre=request.POST.get('titre'),
            contenu=request.POST.get('contenu'),
            type=request.POST.get('type'),
            fichier=request.FILES.get('fichier')
        )
        cours.materiels.add(materiel)

        messages.success(request, 'Matériel ajouté avec succès!')
        return redirect('School:cours_detail', pk=cours_id)

@method_decorator(login_required, name='dispatch')
class QuizCreateView(View):
    def post(self, request, cours_id):
        cours = get_object_or_404(Cours, id=cours_id)
        
        if request.user != cours.enseignant and request.user.role != 'ADMIN':
            messages.error(request, "Vous n'avez pas la permission de créer un quiz pour ce cours.")
            return redirect('School:cours_detail', pk=cours_id)

        # Créer le quiz
        quiz = Quiz.objects.create(
            titre=request.POST.get('titre'),
            cours=cours
        )

        # Créer les questions
        questions = request.POST.getlist('questions[]')
        reponses = request.POST.getlist('reponses[]')
        reponses_correctes = request.POST.getlist('reponse_correcte[]')

        for q, r, rc in zip(questions, reponses, reponses_correctes):
            Question.objects.create(
                quiz=quiz,
                texte=q,
                reponses=json.dumps(r.split(',')),
                reponse_correcte=rc
            )

        messages.success(request, 'Quiz créé avec succès!')
        return redirect('School:cours_detail', pk=cours_id)

@method_decorator(login_required, name='dispatch')
class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'School/quiz_detail.html'
    context_object_name = 'quiz'

    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        score = 0
        total_questions = quiz.questions.count()

        for question in quiz.questions.all():
            reponse_utilisateur = request.POST.get(f'question_{question.id}')
            if reponse_utilisateur == question.reponse_correcte:
                score += 1

        pourcentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        # Créer ou mettre à jour le résultat
        ResultatQuiz.objects.update_or_create(
            quiz=quiz,
            etudiant=request.user,
            defaults={'score': pourcentage}
        )
        
        context = self.get_context_data(object=quiz)
        context['score'] = score
        context['total_questions'] = total_questions
        context['pourcentage'] = pourcentage
        context['quiz_complete'] = True
        
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class ForumListView(ListView):
    model = Forum
    template_name = 'School/forum/list.html'
    context_object_name = 'forums'
    ordering = ['-date_creation']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_messages'] = Message.objects.all().order_by('-date_envoi')[:5]
        return context

@method_decorator(login_required, name='dispatch')
class ForumDetailView(DetailView):
    model = Forum
    template_name = 'School/forum/detail.html'
    context_object_name = 'forum'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.messages.all().order_by('-date_envoi')
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
    fields = ['titre']

    def form_valid(self, form):
        forum = form.save(commit=False)
        forum.save()
        messages.success(self.request, 'Forum créé avec succès!')
        return redirect('School:forum_detail', pk=forum.id)

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