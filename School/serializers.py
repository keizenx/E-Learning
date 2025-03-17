from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import (
    StructureAcademique, Filiere, Classe, Utilisateur, Discussion, Message,
    Forum, Quiz, Question, Cours, Materiel, EmploiDuTemps, ResultatQuiz
)

class UtilisateurSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'nom', 'role', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password', ''))
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class UtilisateurBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'nom', 'role']

class MessageSerializer(serializers.ModelSerializer):
    expediteur = UtilisateurBasicSerializer(read_only=True)
    expediteur_id = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = Message
        fields = ['id', 'contenu', 'date_envoi', 'expediteur', 'expediteur_id', 'date_creation']

class DiscussionSerializer(serializers.ModelSerializer):
    participants = UtilisateurBasicSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)
    
    class Meta:
        model = Discussion
        fields = ['id', 'participants', 'messages', 'participant_ids', 'date_creation']
    
    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        discussion = super().create(validated_data)
        discussion.participants.set(Utilisateur.objects.filter(id__in=participant_ids))
        return discussion
    
    def update(self, instance, validated_data):
        participant_ids = validated_data.pop('participant_ids', None)
        if participant_ids is not None:
            instance.participants.set(Utilisateur.objects.filter(id__in=participant_ids))
        return super().update(instance, validated_data)

class QuizSerializer(serializers.ModelSerializer):
    question_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)
    
    class Meta:
        model = Quiz
        fields = ['id', 'titre', 'question_ids', 'cours', 'date_creation']
    
    def create(self, validated_data):
        question_ids = validated_data.pop('question_ids', [])
        quiz = super().create(validated_data)
        quiz.questions.set(Question.objects.filter(id__in=question_ids))
        return quiz
    
    def update(self, instance, validated_data):
        question_ids = validated_data.pop('question_ids', None)
        if question_ids is not None:
            instance.questions.set(Question.objects.filter(id__in=question_ids))
        return super().update(instance, validated_data)

class CoursSerializer(serializers.ModelSerializer):
    enseignant_id = serializers.UUIDField(write_only=True)
    materiel_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)
    etudiant_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)
    
    class Meta:
        model = Cours
        fields = ['id', 'titre', 'description', 'enseignant_id', 'materiel_ids', 'etudiant_ids', 'is_active', 'date_creation']
    
    def create(self, validated_data):
        materiel_ids, etudiant_ids = validated_data.pop('materiel_ids', []), validated_data.pop('etudiant_ids', [])
        cours = super().create(validated_data)
        cours.materiels.set(Materiel.objects.filter(id__in=materiel_ids))
        cours.etudiants.set(Utilisateur.objects.filter(id__in=etudiant_ids))
        return cours
    
    def update(self, instance, validated_data):
        materiel_ids, etudiant_ids = validated_data.pop('materiel_ids', None), validated_data.pop('etudiant_ids', None)
        if materiel_ids is not None:
            instance.materiels.set(Materiel.objects.filter(id__in=materiel_ids))
        if etudiant_ids is not None:
            instance.etudiants.set(Utilisateur.objects.filter(id__in=etudiant_ids))
        return super().update(instance, validated_data)

class ClasseSerializer(serializers.ModelSerializer):
    enseignant_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)
    
    class Meta:
        model = Classe
        fields = ['id', 'nom', 'niveau', 'enseignant_ids']
    
    def create(self, validated_data):
        enseignant_ids = validated_data.pop('enseignant_ids', [])
        classe = super().create(validated_data)
        classe.enseignants.set(Utilisateur.objects.filter(id__in=enseignant_ids, role='TEACHER'))
        return classe
    
    def update(self, instance, validated_data):
        enseignant_ids = validated_data.pop('enseignant_ids', None)
        if enseignant_ids is not None:
            instance.enseignants.set(Utilisateur.objects.filter(id__in=enseignant_ids, role='TEACHER'))
        return super().update(instance, validated_data)
