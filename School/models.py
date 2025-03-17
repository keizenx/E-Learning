from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

class StructureAcademique(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=200, default="Structure Principale")
    date_creation = models.DateTimeField(default=timezone.now)
    description = CKEditor5Field(config_name='default', default="Description de la structure académique")
    responsable = models.ForeignKey('Utilisateur', on_delete=models.SET_NULL, null=True, blank=True, related_name='structures_gerees')

    class Meta:
        verbose_name = _('structure académique')
        verbose_name_plural = _('structures académiques')

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not StructureAcademique.objects.exists():
            self.pk = uuid.uuid4()
        super().save(*args, **kwargs)

    def ajouterFiliere(self, filiere):
        filiere.structure = self
        filiere.save()

    def ajouterClasse(self, classe):
        classe.structure = self
        classe.save()

    def affecterEnseignant(self, enseignant, classe):
        if enseignant.role == 'TEACHER':
            classe.enseignants.add(enseignant)

class Filiere(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, default="Nouvelle filière")
    description = CKEditor5Field(config_name='default', default="Description de la filière")
    structure = models.ForeignKey(StructureAcademique, on_delete=models.SET_NULL, null=True, blank=True, related_name='filieres')
    date_creation = models.DateTimeField(default=timezone.now)
    responsable = models.ForeignKey('Utilisateur', on_delete=models.SET_NULL, null=True, blank=True, related_name='filieres_gerees')

    class Meta:
        verbose_name = _('filière')
        verbose_name_plural = _('filières')

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.structure:
            self.structure = StructureAcademique.objects.first() or StructureAcademique.objects.create()
        super().save(*args, **kwargs)

class Classe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, default="Nouvelle classe")
    niveau = models.IntegerField(default=1)
    description = CKEditor5Field(config_name='default', default="Description de la classe")
    filiere = models.ForeignKey(Filiere, on_delete=models.SET_NULL, null=True, blank=True, related_name='classes')
    structure = models.ForeignKey(StructureAcademique, on_delete=models.SET_NULL, null=True, blank=True, related_name='classes')
    enseignants = models.ManyToManyField('Utilisateur', related_name='classes_enseignees', blank=True)
    annee_scolaire = models.CharField(max_length=9, default=f"{timezone.now().year}-{timezone.now().year + 1}")

    class Meta:
        verbose_name = _('classe')
        verbose_name_plural = _('classes')

    def __str__(self):
        return f"{self.nom} - Niveau {self.niveau}"

class Utilisateur(AbstractUser):
    ROLES = [
        ('ADMIN', 'Administrateur'),
        ('TEACHER', 'Enseignant'),
        ('STUDENT', 'Étudiant'),
        ('ACADEMIC', 'Responsable académique'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLES, default='STUDENT')
    nom = models.CharField(max_length=100, blank=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def save(self, *args, **kwargs):
        # Si c'est le premier utilisateur, le définir comme admin
        if not Utilisateur.objects.exists():
            self.role = 'ADMIN'
            self.is_superuser = True
            self.is_staff = True
            self.is_approved = True
        # Définir l'approbation automatique pour les étudiants
        elif self.role == 'STUDENT':
            self.is_approved = True
        # Définir le nom s'il n'est pas fourni
        if not self.nom:
            self.nom = self.get_full_name() or self.username
        # S'assurer que l'ID est un UUID valide
        if not self.id:
            self.id = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def seConnecter(self):
        pass

    def seDeconnecter(self):
        pass

class Discussion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(Utilisateur, related_name='discussions', blank=True)
    messages = models.ManyToManyField('Message', related_name='discussions_associees', blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    titre = models.CharField(max_length=200, default="Nouvelle discussion")
    contenu = CKEditor5Field(config_name='extends', default="Contenu de la discussion")
    forum = models.ForeignKey('Forum', on_delete=models.SET_NULL, null=True, blank=True, related_name='discussions')
    auteur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True, related_name='discussions_creees')
    is_resolved = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('discussion')
        verbose_name_plural = _('discussions')

    def __str__(self):
        return f"{self.titre}"

    def envoyerMessage(self, message):
        self.messages.add(message)

    def recevoirMessage(self, message):
        pass

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contenu = CKEditor5Field(config_name='extends', default="Nouveau message")
    date_envoi = models.DateTimeField(default=timezone.now)
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages_envoyes')
    date_creation = models.DateTimeField(default=timezone.now)
    discussion_parent = models.ForeignKey(Discussion, on_delete=models.CASCADE, null=True, blank=True, related_name='messages_discussion')

    class Meta:
        ordering = ['-date_envoi']
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    def __str__(self):
        return f"Message de {self.expediteur.username if self.expediteur else 'Utilisateur inconnu'}"

class Forum(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=200, default="Nouveau forum")
    messages = models.ManyToManyField(Message, related_name='forum', blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    description = CKEditor5Field(config_name='default', default="Description du forum")
    cours = models.ForeignKey('Cours', on_delete=models.SET_NULL, null=True, blank=True, related_name='forums')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.titre

    def creerMessage(self, contenu, expediteur):
        message = Message.objects.create(
            contenu=contenu,
            expediteur=expediteur
        )
        self.messages.add(message)
        return message

    def repondre(self, message_parent, contenu, expediteur):
        reponse = self.creerMessage(contenu, expediteur)
        return reponse

class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=200, default="Nouveau quiz")
    questions = models.ManyToManyField('Question', related_name='quiz_associes', blank=True)
    cours = models.ForeignKey('Cours', on_delete=models.SET_NULL, null=True, blank=True, related_name='quiz')
    date_creation = models.DateTimeField(default=timezone.now)
    description = CKEditor5Field(config_name='default', default="Description du quiz")
    date_limite = models.DateTimeField(default=timezone.now)
    duree = models.DurationField(default=timezone.timedelta(minutes=30))
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('quiz')
        verbose_name_plural = _('quiz')

    def __str__(self):
        return self.titre

    def creerQuiz(self):
        pass

    def soumettre(self):
        pass

    def noter(self):
        pass

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    texte = CKEditor5Field(config_name='extends', default="Question")
    reponses = CKEditor5Field(config_name='default', default="Option 1;Option 2;Option 3", help_text="Pour les QCM, séparez les réponses par des points-virgules")
    reponse_correcte = models.TextField(default="Option 1")
    type = models.CharField(max_length=5, choices=[
        ('QCM', 'Choix multiple'),
        ('LIBRE', 'Réponse libre'),
        ('VF', 'Vrai/Faux'),
    ], default='QCM')
    points = models.PositiveIntegerField(default=1)
    quiz_parent = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True, related_name='questions_quiz')

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return self.texte[:50]

class Cours(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=200, default="Nouveau cours")
    description = CKEditor5Field(config_name='extends', default="Description du cours")
    enseignant = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True, related_name='cours_enseignes')
    materiels = models.ManyToManyField('Materiel', related_name='cours_associes', blank=True)
    etudiants = models.ManyToManyField(Utilisateur, related_name='cours_suivis', blank=True)
    is_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True, blank=True, related_name='cours')
    image = models.ImageField(upload_to='cours/images/', null=True, blank=True)
    video_url = models.URLField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('cours')
        verbose_name_plural = _('cours')

    def __str__(self):
        return self.titre

    def ajouterMateriel(self, materiel):
        self.materiels.add(materiel)

    def supprimerMateriel(self, materiel):
        self.materiels.remove(materiel)

class Materiel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TYPE_CHOICES = [
        ('PDF', 'Document PDF'),
        ('VIDEO', 'Vidéo'),
        ('AUDIO', 'Audio'),
        ('AUTRE', 'Autre'),
    ]
    
    titre = models.CharField(max_length=200, default="Nouveau matériel")
    description = CKEditor5Field(config_name='default', default="Description du matériel")
    cours_principal = models.ForeignKey(Cours, on_delete=models.SET_NULL, null=True, blank=True, related_name='materiels_cours')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='AUTRE')
    contenu = CKEditor5Field(config_name='extends', default="Contenu du matériel")
    fichier = models.FileField(upload_to='materiels/', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('matériel')
        verbose_name_plural = _('matériels')

    def __str__(self):
        return self.titre

class EmploiDuTemps(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creneaux = models.JSONField(default=dict)
    date_creation = models.DateTimeField(default=timezone.now)
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True, blank=True, related_name='emplois_du_temps')
    cours = models.ForeignKey(Cours, on_delete=models.SET_NULL, null=True, blank=True, related_name='creneaux')
    jour = models.CharField(max_length=10, default='Lundi')
    heure_debut = models.TimeField(default='08:00')
    heure_fin = models.TimeField(default='09:00')
    salle = models.CharField(max_length=50, default='Salle non assignée')

    class Meta:
        verbose_name = _('emploi du temps')
        verbose_name_plural = _('emplois du temps')

    def __str__(self):
        return f"EDT: {self.classe} - {self.jour} {self.heure_debut}-{self.heure_fin}"

class ResultatQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='resultats')
    etudiant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='resultats_quiz')
    score = models.FloatField(default=0.0)
    date_completion = models.DateTimeField(default=timezone.now)
    reponses = models.JSONField(default=dict)
    date_soumission = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['quiz', 'etudiant']
        verbose_name = _('résultat de quiz')
        verbose_name_plural = _('résultats de quiz')

    def __str__(self):
        return f"{self.etudiant.username} - {self.quiz.titre} - {self.score}%" 