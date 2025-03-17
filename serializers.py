from rest_framework import serializers
from .models import (
    StructureAcademique, Filiere, Classe, Utilisateur, Discussion,
    Message, Forum, Quiz, Question, Cours, Materiel, EmploiDuTemps, ResultatQuiz
)
from django.contrib.auth.hashers import make_password


class UtilisateurSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'nom', 'role', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
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
    
    def create(self, validated_data):
        expediteur_id = validated_data.pop('expediteur_id', None)
        if expediteur_id:
            validated_data['expediteur_id'] = expediteur_id
        return super().create(validated_data)


class DiscussionSerializer(serializers.ModelSerializer):
    participants = UtilisateurBasicSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Discussion
        fields = ['id', 'participants', 'messages', 'participant_ids', 'date_creation']
    
    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        discussion = Discussion.objects.create(**validated_data)
        
        if participant_ids:
            participants = Utilisateur.objects.filter(id__in=participant_ids)
            discussion.participants.set(participants)
        
        return discussion
    
    def update(self, instance, validated_data):
        participant_ids = validated_data.pop('participant_ids', None)
        
        if participant_ids is not None:
            participants = Utilisateur.objects.filter(id__in=participant_ids)
            instance.participants.set(participants)
        
        return super().update(instance, validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'texte', 'reponses', 'reponse_correcte']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    question_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Quiz
        fields = ['id', 'titre', 'questions', 'question_ids', 'cours', 'date_creation']
    
    def create(self, validated_data):
        question_ids = validated_data.pop('question_ids', [])
        quiz = Quiz.objects.create(**validated_data)
        
        if question_ids:
            questions = Question.objects.filter(id__in=question_ids)
            quiz.questions.set(questions)
        
        return quiz
    
    def update(self, instance, validated_data):
        question_ids = validated_data.pop('question_ids', None)
        
        if question_ids is not None:
            questions = Question.objects.filter(id__in=question_ids)
            instance.questions.set(questions)
        
        return super().update(instance, validated_data)


class MaterielSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materiel
        fields = ['id', 'titre', 'contenu', 'type', 'fichier', 'date_creation']


class CoursSerializer(serializers.ModelSerializer):
    enseignant = UtilisateurBasicSerializer(read_only=True)
    enseignant_id = serializers.UUIDField(write_only=True)
    materiels = MaterielSerializer(many=True, read_only=True)
    etudiants = UtilisateurBasicSerializer(many=True, read_only=True)
    materiel_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    etudiant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Cours
        fields = ['id', 'titre', 'description', 'enseignant', 'enseignant_id',
                 'materiels', 'materiel_ids', 'etudiants', 'etudiant_ids',
                 'is_active', 'date_creation']
    
    def create(self, validated_data):
        materiel_ids = validated_data.pop('materiel_ids', [])
        etudiant_ids = validated_data.pop('etudiant_ids', [])
        
        cours = Cours.objects.create(**validated_data)
        
        if materiel_ids:
            materiels = Materiel.objects.filter(id__in=materiel_ids)
            cours.materiels.set(materiels)
        
        if etudiant_ids:
            etudiants = Utilisateur.objects.filter(id__in=etudiant_ids)
            cours.etudiants.set(etudiants)
        
        return cours
    
    def update(self, instance, validated_data):
        materiel_ids = validated_data.pop('materiel_ids', None)
        etudiant_ids = validated_data.pop('etudiant_ids', None)
        
        if materiel_ids is not None:
            materiels = Materiel.objects.filter(id__in=materiel_ids)
            instance.materiels.set(materiels)
        
        if etudiant_ids is not None:
            etudiants = Utilisateur.objects.filter(id__in=etudiant_ids)
            instance.etudiants.set(etudiants)
        
        return super().update(instance, validated_data)


class ForumSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Forum
        fields = ['id', 'titre', 'messages', 'date_creation']


class EmploiDuTempsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploiDuTemps
        fields = ['id', 'creneaux', 'date_creation']


class ResultatQuizSerializer(serializers.ModelSerializer):
    etudiant = UtilisateurBasicSerializer(read_only=True)
    quiz = QuizSerializer(read_only=True)
    etudiant_id = serializers.UUIDField(write_only=True)
    quiz_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = ResultatQuiz
        fields = ['id', 'quiz', 'quiz_id', 'etudiant', 'etudiant_id', 'score', 'date_completion']
    
    def validate(self, data):
        if ResultatQuiz.objects.filter(
            quiz_id=data['quiz_id'],
            etudiant_id=data['etudiant_id']
        ).exists():
            raise serializers.ValidationError(
                "Ce résultat existe déjà pour cet étudiant et ce quiz."
            )
        return data


class ClasseSerializer(serializers.ModelSerializer):
    filiere = serializers.PrimaryKeyRelatedField(queryset=Filiere.objects.all(), required=False)
    structure = serializers.PrimaryKeyRelatedField(queryset=StructureAcademique.objects.all(), required=False)
    enseignants = UtilisateurBasicSerializer(many=True, read_only=True)
    enseignant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Classe
        fields = ['id', 'nom', 'niveau', 'filiere', 'structure', 'enseignants', 'enseignant_ids']
    
    def create(self, validated_data):
        enseignant_ids = validated_data.pop('enseignant_ids', [])
        classe = Classe.objects.create(**validated_data)
        
        if enseignant_ids:
            enseignants = Utilisateur.objects.filter(id__in=enseignant_ids, role='TEACHER')
            classe.enseignants.set(enseignants)
        
        return classe
    
    def update(self, instance, validated_data):
        enseignant_ids = validated_data.pop('enseignant_ids', None)
        
        if enseignant_ids is not None:
            enseignants = Utilisateur.objects.filter(id__in=enseignant_ids, role='TEACHER')
            instance.enseignants.set(enseignants)
        
        return super().update(instance, validated_data)


class FiliereSerializer(serializers.ModelSerializer):
    structure = serializers.PrimaryKeyRelatedField(queryset=StructureAcademique.objects.all(), required=False)
    classes = ClasseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Filiere
        fields = ['id', 'nom', 'description', 'structure', 'classes', 'date_creation']
    
    def create(self, validated_data):
        # Si aucune structure n'est spécifiée, utiliser la première structure
        if 'structure' not in validated_data:
            structure = StructureAcademique.objects.first()
            if not structure:
                structure = StructureAcademique.objects.create()
            validated_data['structure'] = structure
        return super().create(validated_data)


class StructureAcademiqueSerializer(serializers.ModelSerializer):
    filieres = FiliereSerializer(many=True, read_only=True)
    classes = ClasseSerializer(many=True, read_only=True)
    
    class Meta:
        model = StructureAcademique
        fields = ['id', 'nom', 'filieres', 'classes', 'date_creation']
