# Conference Booking System

Système de réservation pour conférence avec génération de tickets PDF et QR codes.

## Installation

```bash
# Cloner le projet
git clone https://github.com//conference-booking.git
cd conference-booking

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditez .env avec vos informations

# Migrations
python manage.py migrate
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver