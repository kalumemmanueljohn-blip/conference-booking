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

import requests

import urllib.parse

 

# ====================

# CONFIGURATION TIMELINESAI

# ====================

TIMELINES_API_URL = "https://waapi.app/api/v1/instances/ID/client/action/send-message"

TIMELINES_API_KEY = "rFBXhMILLU4naah2bsCT5uAsjeGukQJWe2KzL0Brecb54d2c"

WHATSAPP_ACCOUNT_PHONE = "243859323184"  # Mon numéro WhatsApp

 

def envoyer_whatsapp_timelines(telephone, message):

    """Envoie un message via l'API TimelinesAI"""

    

    if not telephone:

        print("❌ Pas de numéro de téléphone")

        return False

    

    # Nettoyer le numéro (enlever espaces, +, -)

    telephone = telephone.replace(' ', '').replace('+', '').replace('-', '')

    if not telephone.startswith('243') and len(telephone) == 9:

        telephone = '243' + telephone

    

    # Construction de la requête

    url = TIMELINES_API_URL

    

    headers = {

        "Authorization": f"Bearer {TIMELINES_API_KEY}",

        "Content-Type": "application/json",

        "Accept": "application/json",

    }

    

    # Format JSON selon la documentation

    payload = {

        "phone": telephone,

        "text": message

    }

    

    # Ajouter le numéro WhatsApp account si configuré (optionnel)

    if WHATSAPP_ACCOUNT_PHONE:

        payload["whatsapp_account_phone"] = WHATSAPP_ACCOUNT_PHONE

    

    print(f"📱 Envoi WhatsApp Timelines à: {telephone}")

    print(f"📡 URL: {url}")

    

    try:

        response = requests.post(url, json=payload, headers=headers, timeout=30)

        print(f"📡 Status TimelinesAI: {response.status_code}")

        

        if response.status_code in [200, 201, 202]:

            print(f"✅ WhatsApp envoyé à {telephone}")

            return True

        else:

            print(f"❌ Erreur TimelinesAI: {response.status_code}")

            print(f"   Réponse: {response.text[:500]}")

            return False

    except requests.exceptions.ConnectionError:

        print("❌ Impossible de se connecter à TimelinesAI. Vérifie ta connexion internet.")

        return False

    except Exception as e:

        print(f"❌ Exception: {e}")

        return False

 

def envoyer_whatsapp_lien_direct(telephone, message):

    """Méthode de secours : lien WhatsApp direct (gratuit, sans API)"""

    encoded = urllib.parse.quote(message)

    whatsapp_link = f"https://wa.me/{telephone}?text={encoded}"

    print(f"🔗 Lien WhatsApp généré: {whatsapp_link[:100]}...")

    return whatsapp_link

 

def envoyer_whatsapp(telephone, nom, code_unique, nombre_places, site_url, ticket_page_url):

    """Envoie un message WhatsApp avec lien de téléchargement"""

    

    if not telephone:

        print("❌ Pas de numéro de téléphone")

        return False

    

    # Nettoyer le numéro telephone

