# TourismeMaroc — Tourism Management System

Plateforme complète de gestion touristique pour le Maroc : site web (HTML/CSS/JS),
backend PHP + MySQL, et tableau de bord administrateur en Python Tkinter.

## 📁 Structure du projet

```
tourisme/
├── index.html              # Page d'accueil (navbar, hero, destinations, hôtels, restaurants, services, FAQ, chatbot)
├── inscription.html         # Page d'inscription
├── connexion.html           # Page de connexion
├── contact.html             # Page de contact (formulaire + carte Google Maps)
├── css/
│   └── style.css            # Design system complet (responsive, animations)
├── js/
│   └── script.js             # Navbar mobile, cartes dynamiques, accordéon FAQ,
│                              #   chatbot, validation de formulaires, convertisseur
├── php/
│   ├── connexion.php         # Connexion PDO à la base MySQL (à configurer)
│   ├── register.php          # Inscription (hash bcrypt, validation serveur)
│   ├── login.php              # Connexion + session
│   ├── logout.php             # Déconnexion
│   ├── contact.php            # Traitement du formulaire de contact
│   ├── get_destinations.php   # API JSON destinations
│   ├── get_hotels.php         # API JSON hôtels
│   ├── get_restaurants.php    # API JSON restaurants
│   └── admin.php              # Panneau admin web (CRUD)
├── database/
│   └── tourisme.sql           # Schéma + données de démonstration
├── images/                    # Placez vos images locales ici si besoin
└── admin.py                   # Admin desktop en Python Tkinter
```

## 🚀 Installation

### 1. Frontend
Le site fonctionne directement en ouvrant `index.html` dans un navigateur,
ou — pour profiter du PHP — en le plaçant dans un serveur local (XAMPP, WAMP, MAMP, ou `php -S`).

### 2. Base de données MySQL
1. Créez la base avec le script fourni :
   ```bash
   mysql -u root -p < database/tourisme.sql
   ```
   ou importez `database/tourisme.sql` via phpMyAdmin.
2. Modifiez les identifiants dans `php/connexion.php` si nécessaire :
   ```php
   define('DB_HOST', 'localhost');
   define('DB_NAME', 'tourisme');
   define('DB_USER', 'root');
   define('DB_PASS', '');
   ```

### 3. Lancer le serveur PHP
Depuis le dossier `tourisme/` :
```bash
php -S localhost:8000
```
Puis ouvrez `http://localhost:8000/index.html`.

Les formulaires (`inscription.html`, `connexion.html`, `contact.html`) envoient
leurs données vers les scripts du dossier `php/`.

### 4. Admin desktop (Python Tkinter)
1. Installez le connecteur MySQL :
   ```bash
   pip install mysql-connector-python
   ```
2. Vérifiez/ajustez les identifiants dans `admin.py` (`DB_CONFIG`).
3. Lancez l'application :
   ```bash
   python admin.py
   ```

L'admin desktop permet de consulter les utilisateurs inscrits et de gérer
(ajouter/supprimer) les destinations, hôtels et restaurants, avec un tableau
de statistiques.

Une alternative web légère est aussi disponible dans `php/admin.php`.

## 🔐 Sécurité

- Mots de passe hashés avec `password_hash()` (bcrypt) — jamais stockés en clair.
- Toutes les requêtes SQL utilisent des **requêtes préparées** (PDO) pour
  éviter les injections SQL.
- Validation des formulaires côté client (JavaScript) **et** côté serveur (PHP).

## 🎨 Design

Palette inspirée des zelliges marocains : bleu Majorelle, terracotta et sable,
avec un motif d'étoile à 8 branches utilisé comme séparateur visuel récurrent.
Polices : *Playfair Display* (titres) + *Outfit* (texte courant).

## 📝 Notes

- Les images utilisées dans `index.html`/`script.js` proviennent d'Unsplash à
  titre de démonstration ; remplacez-les par vos propres visuels dans `images/`
  pour la production.
- Le chatbot (`js/script.js`) est un assistant basé sur des règles (mots-clés),
  sans appel à une API externe.
