from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from School.models import (
    StructureAcademique, Filiere, Classe, Utilisateur,
    Cours, Materiel, Quiz, Question, ResultatQuiz,
    Forum, Message, Discussion, EmploiDuTemps
)

class Command(BaseCommand):
    help = 'Configure les groupes et leurs permissions'

    def handle(self, *args, **options):
        # Création des groupes
        admin_group, _ = Group.objects.get_or_create(name='ADMIN')
        teacher_group, _ = Group.objects.get_or_create(name='TEACHER')
        student_group, _ = Group.objects.get_or_create(name='STUDENT')
        academic_group, _ = Group.objects.get_or_create(name='ACADEMIC')

        # Permissions pour ADMIN
        admin_models = [
            StructureAcademique, Filiere, Classe, Utilisateur,
            Cours, Materiel, Quiz, Question, ResultatQuiz,
            Forum, Message, Discussion, EmploiDuTemps
        ]
        admin_perms = []
        for model in admin_models:
            content_type = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=content_type)
            admin_perms.extend(perms)
        admin_group.permissions.set(admin_perms)

        # Permissions pour TEACHER
        teacher_models = {
            Cours: ['add', 'change', 'view'],
            Materiel: ['add', 'change', 'delete', 'view'],
            Quiz: ['add', 'change', 'delete', 'view'],
            Question: ['add', 'change', 'delete', 'view'],
            ResultatQuiz: ['add', 'change', 'view'],
            Forum: ['add', 'change', 'view'],
            Message: ['add', 'change', 'delete', 'view'],
            Discussion: ['add', 'change', 'view']
        }
        teacher_perms = []
        for model, actions in teacher_models.items():
            content_type = ContentType.objects.get_for_model(model)
            for action in actions:
                perm = Permission.objects.get(
                    codename=f'{action}_{model._meta.model_name}',
                    content_type=content_type
                )
                teacher_perms.append(perm)
        teacher_group.permissions.set(teacher_perms)

        # Permissions pour STUDENT
        student_models = {
            Cours: ['view'],
            Materiel: ['view'],
            Quiz: ['view'],
            ResultatQuiz: ['view'],
            Forum: ['view'],
            Message: ['add', 'view'],
            Discussion: ['add', 'view']
        }
        student_perms = []
        for model, actions in student_models.items():
            content_type = ContentType.objects.get_for_model(model)
            for action in actions:
                perm = Permission.objects.get(
                    codename=f'{action}_{model._meta.model_name}',
                    content_type=content_type
                )
                student_perms.append(perm)
        student_group.permissions.set(student_perms)

        # Permissions pour ACADEMIC
        academic_models = {
            StructureAcademique: ['view'],
            Filiere: ['add', 'change', 'view'],
            Classe: ['add', 'change', 'view'],
            Cours: ['view'],
            EmploiDuTemps: ['add', 'change', 'view']
        }
        academic_perms = []
        for model, actions in academic_models.items():
            content_type = ContentType.objects.get_for_model(model)
            for action in actions:
                perm = Permission.objects.get(
                    codename=f'{action}_{model._meta.model_name}',
                    content_type=content_type
                )
                academic_perms.append(perm)
        academic_group.permissions.set(academic_perms)

        self.stdout.write(self.style.SUCCESS('Groupes et permissions configurés avec succès')) 