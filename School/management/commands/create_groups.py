from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from School.models import Cours, Materiel, Quiz, Question, Forum, Message

class Command(BaseCommand):
    help = 'Crée les groupes d\'utilisateurs avec leurs permissions'

    def handle(self, *args, **kwargs):
        # Création des groupes
        admin_group, _ = Group.objects.get_or_create(name='ADMIN')
        teacher_group, _ = Group.objects.get_or_create(name='TEACHER')
        student_group, _ = Group.objects.get_or_create(name='STUDENT')
        academic_group, _ = Group.objects.get_or_create(name='ACADEMIC')

        # Permissions pour les modèles
        cours_ct = ContentType.objects.get_for_model(Cours)
        materiel_ct = ContentType.objects.get_for_model(Materiel)
        quiz_ct = ContentType.objects.get_for_model(Quiz)
        question_ct = ContentType.objects.get_for_model(Question)
        forum_ct = ContentType.objects.get_for_model(Forum)
        message_ct = ContentType.objects.get_for_model(Message)

        # Permissions pour les enseignants
        teacher_permissions = [
            Permission.objects.get(codename='add_cours', content_type=cours_ct),
            Permission.objects.get(codename='change_cours', content_type=cours_ct),
            Permission.objects.get(codename='add_materiel', content_type=materiel_ct),
            Permission.objects.get(codename='change_materiel', content_type=materiel_ct),
            Permission.objects.get(codename='add_quiz', content_type=quiz_ct),
            Permission.objects.get(codename='change_quiz', content_type=quiz_ct),
            Permission.objects.get(codename='add_question', content_type=question_ct),
            Permission.objects.get(codename='change_question', content_type=question_ct),
        ]
        teacher_group.permissions.set(teacher_permissions)

        # Permissions pour les étudiants
        student_permissions = [
            Permission.objects.get(codename='view_cours', content_type=cours_ct),
            Permission.objects.get(codename='view_materiel', content_type=materiel_ct),
            Permission.objects.get(codename='view_quiz', content_type=quiz_ct),
            Permission.objects.get(codename='add_message', content_type=message_ct),
        ]
        student_group.permissions.set(student_permissions)

        # Permissions pour les responsables académiques
        academic_permissions = [
            Permission.objects.get(codename='view_cours', content_type=cours_ct),
            Permission.objects.get(codename='view_materiel', content_type=materiel_ct),
            Permission.objects.get(codename='view_quiz', content_type=quiz_ct),
            Permission.objects.get(codename='add_forum', content_type=forum_ct),
            Permission.objects.get(codename='change_forum', content_type=forum_ct),
        ]
        academic_group.permissions.set(academic_permissions)

        # Les administrateurs ont toutes les permissions
        admin_permissions = Permission.objects.filter(
            content_type__in=[cours_ct, materiel_ct, quiz_ct, question_ct, forum_ct, message_ct]
        )
        admin_group.permissions.set(admin_permissions)

        self.stdout.write(self.style.SUCCESS('Groupes et permissions créés avec succès')) 