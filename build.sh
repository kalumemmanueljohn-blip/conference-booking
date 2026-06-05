echo "🔧 Installation des dépendances..."
pip install -r requirements.txt

echo "🗄️ Migrations..."
python manage.py makemigrations
python manage.py migrate

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "✅ Build terminé !"
