# Application d’authentification sécurisée en Flask – Projet DevSecOps

Cette application web propose un système d'inscription et de connexion développé avec Flask. Le projet suit des principes de sécurité dès la conception et s’intègre dans une chaîne d’intégration continue orientée DevSecOps. Il sert de support d’apprentissage et de démonstration de compétences en sécurité applicative.

L’application permet de créer un compte, de se connecter et d’accéder à un espace protégé. Les mots de passe sont stockés sous forme hachée. Les formulaires utilisent une protection CSRF. Une politique de mot de passe impose une longueur minimale ainsi que la présence de différents types de caractères. Le système limite le nombre de requêtes afin de réduire les tentatives de force brute. Les en-têtes HTTP renforcent la sécurité côté navigateur. Un contrôle d’accès distingue les utilisateurs standards et les administrateurs.

La base de données repose sur SQLite et SQLAlchemy. L’initialisation des tables se fait automatiquement au démarrage. Une commande en ligne permet de créer un compte administrateur pour les tests ou le déploiement local.

Le projet inclut une chaîne CI/CD exécutée avec GitHub Actions. Le pipeline vérifie le code source, les dépendances et l’image Docker. Il lance ensuite l’application et réalise un scan dynamique. Le processus s’arrête si une vulnérabilité critique apparaît. Les rapports de sécurité restent disponibles après l’exécution.

Pour exécuter l’application en local, il suffit de cloner le dépôt, de définir les variables d’environnement dans un fichier `.env`, puis de lancer `docker compose up --build`. L’application devient alors accessible sur le port 8080. Un compte administrateur peut être créé avec la commande `flask create-admin` dans le conteneur.

Des tests automatisés vérifient les éléments essentiels du système d’authentification. Ils couvrent la protection CSRF, le flux complet de connexion, le contrôle d’accès administrateur et la validation des données utilisateur.

Ce projet a pour objectif de mettre en pratique des méthodes de développement sécurisé et d’illustrer une démarche DevSecOps simple et complète. Il peut servir de base de travail ou d’exemple dans un portfolio orienté cybersécurité.

Projet réalisé dans un cadre pédagogique.
