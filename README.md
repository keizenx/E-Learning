# Django Online School Management System

Un système de gestion scolaire complet développé avec Django, offrant une plateforme moderne pour la gestion des établissements d'enseignement.

## 🌟 Fonctionnalités

### 👥 Gestion des Utilisateurs
- Multi-rôles (Admin, Enseignant, Étudiant, Responsable Scolarité)
- Authentification sécurisée
- Gestion des permissions

### 📚 Gestion Académique
- Structure académique (filières, niveaux, classes)
- Affectation des enseignants
- Emplois du temps
- Suivi des cours

### 📊 Suivi Pédagogique
- Gestion des notes
- Création de quiz
- Suivi des devoirs
- Rapports de progression

### 💬 Communication
- Forums de discussion
- Messagerie instantanée
- Notifications

## 🛠 Technologies Utilisées

- **Backend:**
  - Django
  - Django REST Framework
  - SQLite (développement)

## 🚀 Installation

1. Cloner le repository
```bash
git clone https://github.com/keizenx/E-Learning.git
cd E-Learning
```

2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Appliquer les migrations
```bash
python manage.py migrate
```

5. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

6. Lancer le serveur
```bash
python manage.py runserver
```

## 📁 Structure du Projet

```
core/
├── models/              # Modèles de données
├── views/               # Vues et logique métier
├── templates/           # Templates HTML
└── static/             # Fichiers statiques

school_management/      # Configuration du projet
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

## 📞 Contact

Franck Bello - [@keizensberg](https://X.com/keizensberg) - franckbello0@gmail.com

Lien du projet: [https://github.com/keizenx/E-Learning](https://github.com/keizenx/E-Learning)
