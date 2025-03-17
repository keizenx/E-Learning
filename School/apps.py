from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class SchoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'School'
    verbose_name = _("École en Ligne")

    def ready(self):
        from django.contrib import admin
        # Configuration de l'interface d'administration
        admin.site.site_header = "Administration - École en Ligne"
        admin.site.site_title = "École en Ligne"
        admin.site.index_title = "Tableau de bord administratif"
        
        # Définition des groupes de modèles
        self.verbose_name_plural = _("École en Ligne")
        
        # Noms des groupes
        self.admin_groups = {
            'auth': _("Authentification et autorisation"),
            'structure': _("Structure académique"),
            'pedagogie': _("Pédagogie"),
            'evaluation': _("Évaluation"),
            'communication': _("Communication"),
            'planning': _("Planning"),
        } 