#!/usr/bin/env python
import os
import sys

def check_deployment():
    print("🔍 Vérification avant déploiement...\n")
    
    errors = []
    warnings = []
    
    # 1. Vérifier Django
    try:
        import django
        print(f"✅ Django {django.get_version()} installé")
    except ImportError:
        errors.append("❌ Django non installé")
    
    # 2. Vérifier requirements.txt
    if os.path.exists("requirements.txt"):
        print("✅ requirements.txt trouvé")
    else:
        errors.append("❌ requirements.txt manquant")
    
    # 3. Vérifier .env
    if os.path.exists(".env"):
        print("✅ .env trouvé")
    else:
        warnings.append("⚠️ .env manquant (créez-le)")
    
    # 4. Vérifier static
    if os.path.exists("static"):
        print("✅ Dossier static trouvé")
        if not os.path.exists("static/css/bootstrap.min.css"):
            warnings.append("⚠️ bootstrap.min.css manquant")
        if not os.path.exists("static/js/bootstrap.bundle.min.js"):
            warnings.append("⚠️ bootstrap.bundle.min.js manquant")
        if not os.path.exists("static/images/logo1.png"):
            warnings.append("⚠️ logo1.png manquant")
    else:
        errors.append("❌ Dossier static manquant")
    
    # 5. Vérifier templates
    if os.path.exists("templates"):
        print("✅ Dossier templates trouvé")
    else:
        errors.append("❌ Dossier templates manquant")
    
    # 6. Vérifier la base de données
    if os.path.exists("db.sqlite3"):
        print("✅ Base de données trouvée")
    else:
        warnings.append("⚠️ Base de données non trouvée")
    
    # Résumé
    print("\n" + "="*50)
    if errors:
        print("❌ ERREURS à corriger:")
        for error in errors:
            print(f"   {error}")
    else:
        print("✅ Aucune erreur critique")
    
    if warnings:
        print("\n⚠️ AVERTISSEMENTS:")
        for warning in warnings:
            print(f"   {warning}")
    
    print("\n🎯 Commandes à exécuter:")
    print("   - python manage.py collectstatic")
    print("   - python manage.py check --deploy")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = check_deployment()
    sys.exit(0 if success else 1)