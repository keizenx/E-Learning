#!/usr/bin/env python
"""
Utilitaire de ligne de commande pour les tâches administratives de Django.
"""

import os
import sys


def main():
    """
    Exécute les tâches administratives de Django.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossible d'importer Django. Vérifiez qu'il est bien installé et "
            "disponible dans votre variable d'environnement PYTHONPATH. "
            "Avez-vous activé votre environnement virtuel ?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
