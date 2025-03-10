from django.apps import AppConfig

class SchoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'School'
    verbose_name = 'École en Ligne'

    def ready(self):
        from django.contrib import admin
        # Configuration de l'interface d'administration
        admin.site.site_header = "Administration - École en Ligne"
        admin.site.site_title = "École en Ligne"
        admin.site.index_title = "Tableau de bord administratif" 