from rest_framework import viewsets, permissions
from School.models import Utilisateur, Cours, Materiel, Quiz, Question, ResultatQuiz, Forum, Discussion, Message
from .serializers import (
    UtilisateurSerializer, CoursSerializer, MaterielSerializer,
    QuizSerializer, QuestionSerializer, ResultatQuizSerializer,
    ForumSerializer, DiscussionSerializer, MessageSerializer
)

class UtilisateurViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les utilisateurs.
    
    list:
    Retourne la liste des utilisateurs (admin) ou les informations de l'utilisateur connecté.
    
    create:
    Crée un nouvel utilisateur.
    
    retrieve:
    Retourne les détails d'un utilisateur spécifique.
    
    update:
    Met à jour les informations d'un utilisateur.
    
    partial_update:
    Met à jour partiellement les informations d'un utilisateur.
    
    delete:
    Supprime un utilisateur.
    """
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Utilisateur.objects.none()
        if self.request.user.is_superuser:
            return Utilisateur.objects.all()
        return Utilisateur.objects.filter(id=self.request.user.id)

class CoursViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les cours.
    
    list:
    Retourne la liste des cours de l'enseignant connecté ou tous les cours pour les étudiants.
    
    create:
    Crée un nouveau cours (enseignants uniquement).
    
    retrieve:
    Retourne les détails d'un cours spécifique.
    
    update:
    Met à jour les informations d'un cours.
    
    partial_update:
    Met à jour partiellement les informations d'un cours.
    
    delete:
    Supprime un cours.
    """
    serializer_class = CoursSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cours.objects.none()
        user = self.request.user
        if user.role == 'TEACHER':
            return Cours.objects.filter(enseignant=user).order_by('titre')
        return Cours.objects.all().order_by('titre')

    def perform_create(self, serializer):
        serializer.save(enseignant=self.request.user)

class MaterielViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les matériels de cours.
    
    list:
    Retourne la liste des matériels des cours de l'enseignant.
    
    create:
    Ajoute un nouveau matériel à un cours.
    
    retrieve:
    Retourne les détails d'un matériel spécifique.
    
    update:
    Met à jour un matériel.
    
    partial_update:
    Met à jour partiellement un matériel.
    
    delete:
    Supprime un matériel.
    """
    serializer_class = MaterielSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Materiel.objects.none()
        return Materiel.objects.filter(cours_principal__enseignant=self.request.user).order_by('titre')

class QuizViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les quiz.
    
    list:
    Retourne la liste des quiz créés par l'enseignant ou disponibles pour l'étudiant.
    
    create:
    Crée un nouveau quiz.
    
    retrieve:
    Retourne les détails d'un quiz spécifique.
    
    update:
    Met à jour un quiz.
    
    partial_update:
    Met à jour partiellement un quiz.
    
    delete:
    Supprime un quiz.
    """
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Quiz.objects.none()
        user = self.request.user
        if user.role == 'TEACHER':
            return Quiz.objects.filter(cours__enseignant=user).order_by('titre')
        return Quiz.objects.filter(cours__in=user.cours_suivis.all()).order_by('titre')

class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les questions des quiz.
    
    list:
    Retourne la liste des questions des quiz de l'enseignant.
    
    create:
    Crée une nouvelle question.
    
    retrieve:
    Retourne les détails d'une question spécifique.
    
    update:
    Met à jour une question.
    
    partial_update:
    Met à jour partiellement une question.
    
    delete:
    Supprime une question.
    """
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Question.objects.none()
        return Question.objects.filter(quiz_parent__cours__enseignant=self.request.user).order_by('id')

class ResultatQuizViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les résultats des quiz.
    
    list:
    Retourne la liste des résultats (enseignant: ses quiz, étudiant: ses résultats).
    
    create:
    Enregistre un nouveau résultat de quiz.
    
    retrieve:
    Retourne les détails d'un résultat spécifique.
    
    update:
    Met à jour un résultat.
    
    partial_update:
    Met à jour partiellement un résultat.
    
    delete:
    Supprime un résultat.
    """
    serializer_class = ResultatQuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ResultatQuiz.objects.none()
        user = self.request.user
        if user.role == 'TEACHER':
            return ResultatQuiz.objects.filter(quiz__cours__enseignant=user).order_by('-date_completion')
        return ResultatQuiz.objects.filter(etudiant=user).order_by('-date_completion')

    def perform_create(self, serializer):
        serializer.save(etudiant=self.request.user)

class ForumViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les forums.
    
    list:
    Retourne la liste des forums.
    
    create:
    Crée un nouveau forum.
    
    retrieve:
    Retourne les détails d'un forum spécifique.
    
    update:
    Met à jour un forum.
    
    partial_update:
    Met à jour partiellement un forum.
    
    delete:
    Supprime un forum.
    """
    serializer_class = ForumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Forum.objects.none()
        return Forum.objects.all().order_by('-date_creation')

class DiscussionViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les discussions des forums.
    
    list:
    Retourne la liste des discussions.
    
    create:
    Crée une nouvelle discussion.
    
    retrieve:
    Retourne les détails d'une discussion spécifique.
    
    update:
    Met à jour une discussion.
    
    partial_update:
    Met à jour partiellement une discussion.
    
    delete:
    Supprime une discussion.
    """
    serializer_class = DiscussionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Discussion.objects.none()
        return Discussion.objects.filter(participants=self.request.user).order_by('-date_creation')

    def perform_create(self, serializer):
        discussion = serializer.save()
        discussion.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les messages des discussions.
    
    list:
    Retourne la liste des messages.
    
    create:
    Crée un nouveau message.
    
    retrieve:
    Retourne les détails d'un message spécifique.
    
    update:
    Met à jour un message.
    
    partial_update:
    Met à jour partiellement un message.
    
    delete:
    Supprime un message.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Message.objects.none()
        return Message.objects.filter(expediteur=self.request.user).order_by('-date_creation')

    def perform_create(self, serializer):
        serializer.save(expediteur=self.request.user) 