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

## 👥 Comment Collaborer

1. Fork le projet sur GitHub
2. Cloner votre fork
```bash
git clone https://github.com/VOTRE-USERNAME/E-Learning.git
```

3. Ajouter le dépôt original comme remote
```bash
git remote add upstream https://github.com/keizenx/E-Learning.git
```

4. Créer une branche pour vos modifications
```bash
git checkout -b feature/ma-nouvelle-fonctionnalite
```

5. Faire vos modifications et commits
```bash
git add .
git commit -m "Description de vos modifications"
```

6. Pousser vers votre fork
```bash
git push origin feature/ma-nouvelle-fonctionnalite
```

7. Créer une Pull Request sur GitHub

### 🔄 Maintenir votre fork à jour
```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 🌿 Branches Principales
- `main` : Code de production stable
- `develop` : Branche de développement principal
- `feature/*` : Branches pour les nouvelles fonctionnalités
- `bugfix/*` : Branches pour les corrections de bugs

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
