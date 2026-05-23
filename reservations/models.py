from django.db import models
import random
import string

class Reservation(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente de paiement'),
        ('paye', 'Payé et confirmé'),
        ('annule', 'Annulé'),
        ('expire', 'Expiré'),
    ]
    
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True, null=True)
    nombre_places = models.IntegerField(default=1)
    code_unique = models.CharField(max_length=10, unique=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_paiement = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.code_unique:
            self.code_unique = self.generer_code_unique()
        super().save(*args, **kwargs)
    
    def generer_code_unique(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    def __str__(self):
        return f"{self.nom} - {self.code_unique}"