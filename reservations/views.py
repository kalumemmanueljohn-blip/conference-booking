import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from .forms import ReservationForm
from .models import Reservation
from .utils import envoyer_pdf
import urllib.parse
from datetime import datetime
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

# ====================
# PAGE D'ACCUEIL
# ====================
def home(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            r = form.save()
            messages.success(request, f"✅ Réservation créée ! Code: {r.code_unique}")
            return redirect('waiting', r.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"❌ {field}: {error}")
    else:
        form = ReservationForm()
    return render(request, 'client/home.html', {'form': form})

# ====================
# PAGE D'ATTENTE APRÈS RÉSERVATION
# ====================
def waiting(request, id):
    r = get_object_or_404(Reservation, id=id)
    
    message_whatsapp = f"""Bonjour ! Je souhaite finaliser ma réservation.

📌 MES INFORMATIONS :
• Nom : {r.nom}
• Code : {r.code_unique}
• Places : {r.nombre_places}
• Email : {r.email}

Merci de me confirmer la procédure de paiement."""
    
    context = {
        'r': r,
        'message_whatsapp': message_whatsapp,
    }
    return render(request, 'client/waiting.html', context)

# ====================
# REDIRECTION WHATSAPP
# ====================
def whatsapp(request, id):
    r = get_object_or_404(Reservation, id=id)
    msg = f"Nom: {r.nom} | Places: {r.nombre_places} | Code: {r.code_unique}"
    encoded_msg = urllib.parse.quote(msg)
    return redirect(f"https://wa.me/243859323184?text={encoded_msg}")

def download_ticket(request, code_unique):
    """Page de téléchargement du ticket à partir du code unique"""
    
    reservation = get_object_or_404(Reservation, code_unique=code_unique)
    
    pdf_filename = f"Ticket_{reservation.code_unique}.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)
    
    if not os.path.exists(pdf_path):
        from .utils import envoyer_pdf
        envoyer_pdf(reservation)
    
    pdf_url = f"{settings.SITE_URL}{settings.MEDIA_URL}{pdf_filename}"
    
    context = {
        'reservation': reservation,
        'pdf_url': pdf_url,
    }
    return render(request, 'client/download_ticket.html', context)

# ====================
# CONNEXION ADMIN
# ====================
def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "❌ Nom d'utilisateur ou mot de passe incorrect"
    return render(request, 'auth/login.html', {'error': error})

# ====================
# DÉCONNEXION
# ====================
def logout_view(request):
    logout(request)
    messages.info(request, "🔓 Vous avez été déconnecté")
    return redirect('login')

# ====================
# DASHBOARD ADMIN
# ====================
@login_required
@user_passes_test(is_admin, login_url='login')
def dashboard(request):
    reservations = Reservation.objects.all().order_by('-id')
    paginator = Paginator(reservations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    stats = {
        'total': reservations.count(),
        'en_attente': reservations.filter(statut='en_attente').count(),
        'payes': reservations.filter(statut='paye').count(),
    }
    return render(request, 'admin/dashboard.html', {'page_obj': page_obj, 'stats': stats})

# ====================
# VALIDER UNE RÉSERVATION
# ====================
@login_required
@user_passes_test(is_admin, login_url='login')
def valider(request, id):
    r = get_object_or_404(Reservation, id=id)
    if r.statut == "paye":
        messages.warning(request, f"⚠️ Réservation #{r.id} déjà validée")
    else:
        r.statut = "paye"
        r.date_paiement = datetime.now()
        r.save()
        envoyer_pdf(r)
        messages.success(request, f"✅ Réservation #{r.id} validée !")
    return redirect('dashboard')

# ====================
# STATISTIQUES
# ====================
@login_required
@user_passes_test(is_admin, login_url='login')
def stats(request):
    reservations = Reservation.objects.all()
    total = reservations.count()
    payes = reservations.filter(statut="paye").count()
    en_attente = reservations.filter(statut="en_attente").count()
    revenus = sum(r.nombre_places for r in reservations.filter(statut="paye")) * 7
    
    taux_conversion = round((payes / total * 100), 2) if total > 0 else 0
    
    return render(request, 'admin/stats.html', {
        "total": total,
        "payes": payes,
        "en_attente": en_attente,
        "revenus": revenus,
        "taux_conversion": taux_conversion,
    })

# ====================
# VIDER TOUT LE DASHBOARD
# ====================
@login_required
@user_passes_test(is_admin, login_url='login')
def vider_dashboard(request):
    if request.method == "POST":
        Reservation.objects.all().delete()
        messages.success(request, "🗑️ Toutes les réservations ont été supprimées")
    return redirect('dashboard')

# ====================
# SUPPRIMER UNE SÉLECTION DE RÉSERVATIONS
# ====================
@login_required
@user_passes_test(is_admin, login_url='login')
def supprimer_selection(request):
    if request.method == "POST":
        ids = request.POST.getlist('reservation_ids')
        if ids:
            count = len(ids)
            Reservation.objects.filter(id__in=ids).delete()
            messages.success(request, f"✅ {count} réservation(s) supprimée(s)")
        else:
            messages.warning(request, "⚠️ Aucune réservation sélectionnée")
    return redirect('dashboard')

# ====================
# PAGE CONTACT
# ====================
def contact(request):
    if request.method == "POST":
        nom = request.POST.get('nom', '').strip()
        email = request.POST.get('email', '').strip()
        sujet = request.POST.get('sujet', '').strip()
        message = request.POST.get('message', '').strip()
        
        if not nom or not email or not sujet or not message:
            messages.error(request, "❌ Tous les champs sont obligatoires")
            return redirect('contact')
        
        if '@' not in email or '.' not in email:
            messages.error(request, "❌ Veuillez entrer un email valide")
            return redirect('contact')
        
        try:
            email_body = f"""

            
            
📧 NOUVEAU MESSAGE DE CONTACT
━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Nom:  {nom}
📧 Email: {email}
📝 Sujet: {sujet}

💬 MESSAGE:
{message}
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            send_mail(
                subject=f"[Conference Booking] Contact - {sujet}",
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(request, "✅ Votre message a été envoyé avec succès !")
        except Exception as e:
            print(f"Erreur envoi email: {e}")
            messages.error(request, "❌ Erreur lors de l'envoi. Réessayez plus tard.")
        
        return redirect('contact')
    
    return render(request, 'contact.html')

# ====================
# TEST EMAIL (Ajoutez À LA FIN du fichier, hors de contact)
# ====================
@csrf_exempt
def test_email(request):
    try:
        send_mail(
            'Test Email depuis Render',
            'Ceci est un test de votre configuration email',
            'johnkalumeemmanuel9@gmail.com',
            ['johnkalumeemmanuel9@gmail.com'],
            fail_silently=False,
        )
        return HttpResponse("✅ Email envoyé avec succès!")
    except Exception as e:
        return HttpResponse(f"❌ Erreur: {e}")

# ====================
# PAGE MENTIONS LÉGALES
# ====================
def mentions(request):
    return render(request, 'mentions.html')
