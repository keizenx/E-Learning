from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

class StructureAcademique(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=200, default="Structure Principale")
    date_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Structure Académique"
        verbose_name_plural = "Structures Académiques"

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
    nom = models.CharField(max_length=100)
    description = models.TextField(default="")
    structure = models.ForeignKey(
        StructureAcademique,
        on_delete=models.SET_NULL,
        related_name='filieres',
        null=True,
        blank=True,
        default=None
    )
    date_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.structure:
            self.structure = StructureAcademique.objects.first() or StructureAcademique.objects.create()
        super().save(*args, **kwargs)

class Classe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    niveau = models.IntegerField(default=1)
    filiere = models.ForeignKey(
        Filiere,
        on_delete=models.CASCADE,
        related_name='classes',
        null=True,
        blank=True
    )
    structure = models.ForeignKey(
        StructureAcademique,
        on_delete=models.CASCADE,
        related_name='classes',
        null=True,
        blank=True
    )
    enseignants = models.ManyToManyField('Utilisateur', related_name='classes_enseignees', blank=True)

    class Meta:
        verbose_name = "Classe"
        verbose_name_plural = "Classes"

    def __str__(self):
        return f"{self.nom} - Niveau {self.niveau}"

class Utilisateur(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrateur'),
        ('TEACHER', 'Enseignant'),
        ('STUDENT', 'Étudiant'),
        ('ACADEMIC', 'Responsable Académique')
    )

    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100, default="")
    role = models.CharField(max_length=10, choices=ROLES, default='STUDENT')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def seConnecter(self):
        pass

    def seDeconnecter(self):
        pass

class Discussion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(Utilisateur, related_name='discussions', blank=True)
    messages = models.ManyToManyField('Message', related_name='discussion', blank=True)
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Discussion {self.id}"

    def envoyerMessage(self, message):
        self.messages.add(message)

    def recevoirMessage(self, message):
        pass

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(default=timezone.now)
    expediteur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        related_name='messages_envoyes',
        null=True,
        blank=True
    )
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message de {self.expediteur.username if self.expediteur else 'Utilisateur inconnu'}"

    class Meta:
        ordering = ['-date_envoi']

class Forum(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=200)
    messages = models.ManyToManyField(Message, related_name='forum', blank=True)
    date_creation = models.DateTimeField(default=timezone.now)

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
    titre = models.CharField(max_length=200)
    questions = models.ManyToManyField('Question', related_name='quiz', blank=True)
    cours = models.ForeignKey(
        'Cours',
        on_delete=models.CASCADE,
        related_name='quiz',
        null=True,
        blank=True
    )
    date_creation = models.DateTimeField(default=timezone.now)

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
    texte = models.TextField()
    reponses = models.JSONField(default=dict)
    reponse_correcte = models.CharField(max_length=200)

    def __str__(self):
        return self.texte[:50]

class Cours(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=200)
    description = models.TextField(default="")
    enseignant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='cours_enseignes'
    )
    materiels = models.ManyToManyField('Materiel', related_name='cours', blank=True)
    etudiants = models.ManyToManyField(Utilisateur, related_name='cours_suivis', blank=True)
    is_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titre

    def ajouterMateriel(self, materiel):
        self.materiels.add(materiel)

    def supprimerMateriel(self, materiel):
        self.materiels.remove(materiel)

class Materiel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=200)
    contenu = models.TextField(default="")
    type = models.CharField(max_length=50, default='document')
    fichier = models.FileField(upload_to='materiels/', null=True, blank=True)
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titre

class EmploiDuTemps(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creneaux = models.JSONField(default=dict)
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Emploi du temps {self.id}"

    def ajouterCreneau(self, creneau):
        creneaux = self.creneaux or {}
        if 'items' not in creneaux:
            creneaux['items'] = []
        creneaux['items'].append(creneau)
        self.creneaux = creneaux
        self.save()

    def supprimerCreneau(self, creneau_id):
        if 'items' in self.creneaux:
            self.creneaux['items'] = [c for c in self.creneaux['items'] if c.get('id') != creneau_id]
            self.save()

    def modifierCreneau(self, creneau_id, nouvelles_donnees):
        if 'items' in self.creneaux:
            for i, creneau in enumerate(self.creneaux['items']):
                if creneau.get('id') == creneau_id:
                    self.creneaux['items'][i].update(nouvelles_donnees)
                    break
            self.save()

class ResultatQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='resultats')
    etudiant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='resultats_quiz')
    score = models.FloatField()
    date_completion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['quiz', 'etudiant']
        verbose_name = "Résultat de quiz"
        verbose_name_plural = "Résultats de quiz"

    def __str__(self):
        return f"{self.etudiant.username} - {self.quiz.titre} - {self.score}%" 