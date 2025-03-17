from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class SchoolAdminSite(admin.AdminSite):
    site_header = _("École en Ligne")
    site_title = _("École en Ligne")
    index_title = _("Administration")

    def get_app_list(self, request):
        """
        Retourne une liste d'applications organisée par groupes fonctionnels
        """
        app_dict = self._build_app_dict(request)
        app_list = []

        # Définition des groupes
        groups = {
            'auth': {
                'name': _("Authentification et autorisation"),
                'models': ['Utilisateur', 'Group'],
                'icon': 'fas fa-users-cog'
            },
            'structure': {
                'name': _("Structure académique"),
                'models': ['StructureAcademique', 'Filiere', 'Classe'],
                'icon': 'fas fa-university'
            },
            'pedagogie': {
                'name': _("Pédagogie"),
                'models': ['Cours', 'Materiel'],
                'icon': 'fas fa-book'
            },
            'evaluation': {
                'name': _("Évaluation"),
                'models': ['Quiz', 'Question', 'ResultatQuiz'],
                'icon': 'fas fa-tasks'
            },
            'communication': {
                'name': _("Communication"),
                'models': ['Forum', 'Discussion', 'Message'],
                'icon': 'fas fa-comments'
            },
            'planning': {
                'name': _("Planning"),
                'models': ['EmploiDuTemps'],
                'icon': 'fas fa-calendar'
            }
        }

        # Organisation des modèles par groupe
        for group_name, group_config in groups.items():
            group_models = []
            for app_label in app_dict:
                app = app_dict[app_label]
                for model in app['models']:
                    if model['object_name'] in group_config['models']:
                        model_dict = {
                            'name': model['name'],
                            'object_name': model['object_name'],
                            'perms': model['perms'],
                            'admin_url': model['admin_url'],
                            'add_url': model['add_url'],
                            'icon': self.get_model_icon(model['object_name'])
                        }
                        group_models.append(model_dict)

            if group_models:
                app_list.append({
                    'name': group_config['name'],
                    'app_label': group_name,
                    'app_url': f'/admin/{group_name}/',
                    'has_module_perms': True,
                    'models': sorted(group_models, key=lambda x: group_config['models'].index(x['object_name'])),
                    'icon': group_config['icon']
                })

        return app_list

    def get_model_icon(self, model_name):
        """
        Retourne l'icône correspondant au modèle
        """
        icons = {
            'Utilisateur': 'fas fa-user-graduate',
            'Group': 'fas fa-users',
            'StructureAcademique': 'fas fa-university',
            'Filiere': 'fas fa-graduation-cap',
            'Classe': 'fas fa-chalkboard',
            'Cours': 'fas fa-book',
            'Materiel': 'fas fa-file-alt',
            'Quiz': 'fas fa-question-circle',
            'Question': 'fas fa-question',
            'ResultatQuiz': 'fas fa-chart-bar',
            'Forum': 'fas fa-comments',
            'Discussion': 'fas fa-comment-dots',
            'Message': 'fas fa-envelope',
            'EmploiDuTemps': 'fas fa-calendar-alt'
        }
        return icons.get(model_name, 'fas fa-circle')

# Créer une instance du site d'administration personnalisé
admin_site = SchoolAdminSite(name='school_admin') 