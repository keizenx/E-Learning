from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrateur'
    TEACHER = 'TEACHER', 'Enseignant'
    STUDENT = 'STUDENT', 'Étudiant'
    ACADEMIC = 'ACADEMIC', 'Responsable Scolarité'

class Utilisateur(AbstractUser):
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    def __str__(self):
        return f"{self.nom} ({self.get_role_display()})"

class StructureAcademique(models.Model):
    filieres = models.ManyToManyField('Filiere')
    classes = models.ManyToManyField('Classe')

    def ajouter_filiere(self, filiere):
        self.filieres.add(filiere)

    def ajouter_classe(self, classe):
        self.classes.add(classe)

    def affecter_enseignant(self, enseignant, classe):
        classe.enseignant = enseignant
        classe.save()

class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.nom

class Classe(models.Model):
    nom = models.CharField(max_length=100)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nom} - {self.filiere}"

class EmploiDuTemps(models.Model):
    creneaux = models.ManyToManyField('Creneau')

    def ajouter_creneau(self, creneau):
        self.creneaux.add(creneau)

    def supprimer_creneau(self, creneau):
        self.creneaux.remove(creneau)

    def modifier_creneau(self, creneau, **kwargs):
        for key, value in kwargs.items():
            setattr(creneau, key, value)
        creneau.save()

class Creneau(models.Model):
    debut = models.DateTimeField()
    fin = models.DateTimeField()
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)

class Discussion(models.Model):
    participants = models.ManyToManyField(Utilisateur)
    messages = models.ManyToManyField('Message')

    def envoyer_message(self, message):
        self.messages.add(message)

    def recevoir_message(self, message):
        self.messages.add(message)

class Message(models.Model):
    contenu = models.TextField()
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

class Forum(models.Model):
    titre = models.CharField(max_length=200)
    messages = models.ManyToManyField(Message)

    def creer_message(self, message):
        self.messages.add(message)

    def repondre(self, message):
        self.messages.add(message)

class Quiz(models.Model):
    titre = models.CharField(max_length=200)
    questions = models.ManyToManyField('Question')
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)

    def creer_quiz(self):
        pass

    def soumettre(self):
        pass

    def noter(self):
        pass

class Question(models.Model):
    texte = models.TextField()
    reponses = models.JSONField()  # Stocke les choix de réponses
    reponse_correcte = models.CharField(max_length=200)

class Cours(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    materiels = models.ManyToManyField('Materiel')
    enseignant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def ajouter_materiel(self, materiel):
        self.materiels.add(materiel)

    def supprimer_materiel(self, materiel):
        self.materiels.remove(materiel)

class Materiel(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    type = models.CharField(max_length=50)  # PDF, vidéo, etc.
    fichier = models.FileField(upload_to='materiels/', null=True, blank=True)
