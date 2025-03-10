from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class SchoolAdminSite(AdminSite):
    site_header = _("Administration - École en Ligne")
    site_title = _("École en Ligne")
    index_title = _("Tableau de bord administratif")

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # Réorganiser les applications dans l'ordre souhaité
        app_order = [
            'auth',  # Authentication and Authorization
            'School',  # Votre application
        ]
        
        # Trier les applications selon l'ordre défini
        app_list.sort(key=lambda x: app_order.index(x['app_label']) if x['app_label'] in app_order else len(app_order))
        return app_list

# Créer une instance du site d'administration personnalisé
admin_site = SchoolAdminSite(name='school_admin') 