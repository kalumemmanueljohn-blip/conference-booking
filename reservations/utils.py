from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from django.core.mail import EmailMessage
from django.conf import settings
from io import BytesIO
import os
import qrcode
import tempfile
from datetime import datetime

# ====================
# WHATSAPP DÉSACTIVÉ (pour éviter les timeouts)
# ====================
WHATSAPP_ENABLED = False

# ====================
# GÉNÉRATION DU PDF ET ENVOI
# ====================
def envoyer_pdf(r):
    """Génère un PDF professionnel et l'envoie par email"""
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # ========== COULEURS ==========
    noir = HexColor('#000000')
    jaune = HexColor('#FFD700')
    gris_fonce = HexColor('#333333')
    
    # ========== FOND JAUNE EN HAUT ==========
    p.setFillColor(jaune)
    p.rect(0, height - 200, width, 200, fill=1, stroke=0)
    
    # ========== LOGO ==========
    logo_path = os.path.join(settings.BASE_DIR, 'static/images/logo.png')
    logo_placee = False
    if os.path.exists(logo_path):
        try:
            logo_width = 90
            logo_height = 70
            logo_x = (width - logo_width) / 2
            logo_y = height - 160
            p.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')
            logo_placee = True
        except:
            pass
    
    # ========== TITRE ==========
    titre_y = height - 75 if logo_placee else height - 50
    p.setFont("Helvetica-Bold", 28)
    p.setFillColor(noir)
    p.drawCentredString(width/2, titre_y, "CONFIRMATION DE RÉSERVATION")
    
    # ========== LIGNE DE SÉPARATION ==========
    p.setStrokeColor(jaune)
    p.setLineWidth(3)
    p.line(50, height - 220, width - 50, height - 220)
    
    # ========== CADRE PRINCIPAL ==========
    p.setFillColor(white)
    p.setStrokeColor(jaune)
    p.setLineWidth(2)
    p.roundRect(40, height - 580, width - 80, 400, 15, fill=1, stroke=1)
    
    # ========== BONJOUR ==========
    p.setFont("Helvetica-Bold", 20)
    p.setFillColor(noir)
    p.drawString(60, height - 250, f"Bonjour {r.nom} !")
    
    p.setFont("Helvetica", 12)
    p.setFillColor(gris_fonce)
    p.drawString(60, height - 275, "Votre réservation a été confirmée avec succès.")
    
    # ========== INFORMATIONS ==========
    y = height - 320
    
    # Code
    p.setFillColor(jaune)
    p.rect(50, y - 5, width - 100, 25, fill=1, stroke=0)
    p.setFont("Helvetica-Bold", 11)
    p.setFillColor(noir)
    p.drawString(60, y + 2, "CODE DE RÉSERVATION")
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(jaune)
    p.drawString(60, y - 25, f"{r.code_unique}")
    
    y -= 55
    
    # Grille d'informations
    infos = [
        ("👥 Nombre de places", f"{r.nombre_places} personne(s)"),
        ("💰 Prix total", f"{r.nombre_places * 7}$ USD"),
        ("📍 Lieu", "SILIKIN VILLAGE (Kinshasa)"),
        ("📅 Date", "26 Juin 2026"),
        ("⏰ Horaire", "11H00 - 15H00"),
    ]
    
    for label, value in infos:
        p.setFont("Helvetica-Bold", 10)
        p.setFillColor(noir)
        p.drawString(60, y, label)
        p.setFont("Helvetica", 10)
        p.setFillColor(gris_fonce)
        p.drawString(180, y, value)
        y -= 25
    
    # Statut
    p.setFillColor(jaune)
    p.roundRect(50, y - 5, 120, 22, 5, fill=1, stroke=0)
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(noir)
    p.drawCentredString(110, y + 2, "✅ STATUT : CONFIRMÉ")
    
    y -= 45
    
    # Message
    p.setFont("Helvetica-Oblique", 10)
    p.setFillColor(gris_fonce)
    p.drawString(60, y, "Merci de présenter ce document ou le QR code à l'entrée.")
    
    # ========== QR CODE ==========
    qr_y = y - 80
    try:
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        qr.add_data(f"Code: {r.code_unique}\nNom: {r.nom}\nPlaces: {r.nombre_places}")
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            qr_image.save(tmp_file.name, 'PNG')
            tmp_file_path = tmp_file.name
        
        qr_size = 120
        qr_x = (width - qr_size) / 2
        p.drawImage(tmp_file_path, qr_x, qr_y - qr_size, width=qr_size, height=qr_size)
        p.setFont("Helvetica", 9)
        p.setFillColor(gris_fonce)
        p.drawCentredString(width/2, qr_y - qr_size - 10, "Scannez ce QR code à l'entrée")
        os.unlink(tmp_file_path)
    except:
        pass
    
    # ========== PIED DE PAGE ==========
    p.setFillColor(noir)
    p.rect(0, 0, width, 60, fill=1, stroke=0)
    
    p.setFont("Helvetica", 8)
    p.setFillColor(jaune)
    p.drawCentredString(width/2, 35, "© 2026 BANTONDO'S GENERATION - Tous droits réservés")
    p.drawCentredString(width/2, 20, f"Ticket généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
    
    p.save()
    buffer.seek(0)
    
    # ========== SAUVEGARDE PDF ==========
    pdf_filename = f"Ticket_{r.code_unique}.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)
    with open(pdf_path, 'wb') as f:
        f.write(buffer.getvalue())
    
    # ========== GÉNÉRATION DES URLS ==========
    site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
    
    # URL directe du PDF
    pdf_url = f"{site_url}{settings.MEDIA_URL}{pdf_filename}"
    
    # URL de la page de téléchargement
    ticket_page_url = f"{site_url}/ticket/{r.code_unique}/"
    
    # ========== WHATSAPP DÉSACTIVÉ ==========
    whatsapp_envoye = False
    print("ℹ️ WhatsApp désactivé - seul l'email est envoyé")
    
    # ========== EMAIL HTML ==========
    email_html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirmation de réservation</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; }}
        .container {{ max-width: 600px; margin: 30px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%); color: #FFD700; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; letter-spacing: 2px; }}
        .content {{ padding: 30px; }}
        .info-card {{ background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; padding: 20px; margin: 20px 0; border-left: 5px solid #FFD700; }}
        .code-box {{ background: #000; color: #FFD700; padding: 15px; text-align: center; border-radius: 10px; margin: 15px 0; font-family: monospace; font-size: 28px; letter-spacing: 3px; }}
        .detail-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e0e0e0; }}
        .detail-label {{ font-weight: bold; color: #000; }}
        .detail-value {{ color: #555; }}
        .status-badge {{ background: #FFD700; color: #000; padding: 8px 20px; border-radius: 50px; display: inline-block; font-weight: bold; margin: 15px 0; }}
        .btn-ticket {{ display: inline-block; background: #000; border: 2px solid #FFD700; color: #FFD700; padding: 12px 30px; text-decoration: none; border-radius: 50px; font-weight: bold; margin: 15px 0; transition: transform 0.3s; }}
        .btn-ticket:hover {{ transform: scale(1.05); background: #FFD700; color: #000; }}
        .footer {{ background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #999; border-top: 1px solid #eee; }}
        .highlight {{ color: #FFD700; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎟️ CONFIRMATION DE RÉSERVATION</h1>
            <p>Conférence Annuelle ELENGE ZWA MAYELE</p>
        </div>
        <div class="content">
            <div class="greeting">
                <h2>Bonjour {r.nom} ! 👋</h2>
                <p>Votre réservation a été <strong class="highlight">confirmée avec succès</strong>.</p>
            </div>
            <div class="info-card">
                <div class="detail-row">
                    <span class="detail-label">🎫 Code de réservation</span>
                    <span class="detail-value"><strong> {r.code_unique}</strong></span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">👥 Nombre de places</span>
                    <span class="detail-value"> {r.nombre_places} personne(s)</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">💰 Prix total</span>
                    <span class="detail-value"> {r.nombre_places * 7}$ USD</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">📍 Lieu</span>
                    <span class="detail-value"> SILIKIN VILLAGE (Kinshasa)</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">📅 Date</span>
                    <span class="detail-value"> 26 Juin 2026</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">⏰ Horaire</span>
                    <span class="detail-value"> 11H00 - 15H00</span>
                </div>
            </div>
            <div style="text-align: center;">
                <span class="status-badge">✅ STATUT : CONFIRMÉ</span>
            </div>
            <div class="code-box">
                {r.code_unique}
            </div>
            <p style="text-align: center; margin: 20px 0;">
                📄 <strong>Votre ticket est prêt</strong><br>
                <small>Cliquez sur le bouton ci-dessous pour le télécharger</small>
            </p>
            <div style="text-align: center;">
                <a href="{pdf_url}" class="btn-ticket">📥 Télécharger mon ticket (PDF)</a>
            </div>
            <p style="text-align: center; margin-top: 15px;">
                <small>Ou utilisez ce lien : <a href="{pdf_url}">{pdf_url[:50]}...</a></small>
            </p>
        </div>
        <div class="footer">
            <p>© 2026 BANTONDO'S GENERATION - Tous droits réservés</p>
            <p>Cet email est généré automatiquement, merci de ne pas y répondre.</p>
        </div>
    </div>
</body>
</html>
    """
    
    email = EmailMessage(
        subject=f"🎟️ Confirmation de réservation - Code: {r.code_unique}",
        body=email_html,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[r.email]
    )
    email.content_subtype = "html"
    
    with open(pdf_path, 'rb') as f:
        email.attach(pdf_filename, f.read(), "application/pdf")
    
    try:
        email.send()
        print(f"✅ Email envoyé à {r.email}")
    except Exception as e:
        print(f"❌ Erreur email: {e}")
    
    return whatsapp_envoye
