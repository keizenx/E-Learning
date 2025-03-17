from rest_framework import viewsets
from .models import (
    StructureAcademique, Filiere, Classe, Utilisateur, Discussion, Message,
    Forum, Quiz, Question, Cours, Materiel, EmploiDuTemps, ResultatQuiz
)
from .serializers import (
    StructureAcademiqueSerializer, FiliereSerializer, ClasseSerializer, UtilisateurSerializer,
    DiscussionSerializer, MessageSerializer, ForumSerializer, QuizSerializer, QuestionSerializer,
    CoursSerializer, MaterielSerializer, EmploiDuTempsSerializer, ResultatQuizSerializer
)

class StructureAcademiqueViewSet(viewsets.ModelViewSet):
    queryset = StructureAcademique.objects.all()
    serializer_class = StructureAcademiqueSerializer

class FiliereViewSet(viewsets.ModelViewSet):
    queryset = Filiere.objects.all()
    serializer_class = FiliereSerializer

class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer

class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

class DiscussionViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all()
    serializer_class = CoursSerializer

class MaterielViewSet(viewsets.ModelViewSet):
    queryset = Materiel.objects.all()
    serializer_class = MaterielSerializer

class EmploiDuTempsViewSet(viewsets.ModelViewSet):
    queryset = EmploiDuTemps.objects.all()
    serializer_class = EmploiDuTempsSerializer

class ResultatQuizViewSet(viewsets.ModelViewSet):
    queryset = ResultatQuiz.objects.all()
    serializer_class = ResultatQuizSerializer

