from rest_framework import serializers
from School.models import Utilisateur, Cours, Materiel, Quiz, Question, ResultatQuiz, Forum, Discussion, Message

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'nom', 'role', 'date_joined']
        read_only_fields = ['date_joined']

class CoursSerializer(serializers.ModelSerializer):
    enseignant = UtilisateurSerializer(read_only=True)
    
    class Meta:
        model = Cours
        fields = ['id', 'titre', 'description', 'enseignant', 'materiels', 'etudiants', 'is_active', 'date_creation']
        read_only_fields = ['date_creation']
        depth = 1

class MaterielSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materiel
        fields = ['id', 'titre', 'contenu', 'type', 'fichier', 'date_creation', 'cours_principal']
        read_only_fields = ['date_creation']
        depth = 1

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'texte', 'reponses', 'reponse_correcte', 'quiz_parent']
        depth = 1

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'titre', 'cours', 'questions', 'date_creation']
        read_only_fields = ['date_creation']
        depth = 1

class ResultatQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultatQuiz
        fields = ['id', 'etudiant', 'quiz', 'score', 'date_completion']
        read_only_fields = ['date_completion']
        depth = 1

class MessageSerializer(serializers.ModelSerializer):
    expediteur = UtilisateurSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'contenu', 'expediteur', 'date_envoi', 'date_creation']
        read_only_fields = ['date_creation', 'date_envoi']
        depth = 1

class DiscussionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Discussion
        fields = ['id', 'participants', 'messages', 'date_creation']
        read_only_fields = ['date_creation']
        depth = 1

class ForumSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Forum
        fields = ['id', 'titre', 'messages', 'date_creation', 'cours']
        read_only_fields = ['date_creation']
        depth = 1 