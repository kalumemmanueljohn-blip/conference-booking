from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'email', 'telephone', 'nombre_places', 'code_unique', 'statut', 'date_creation']
    list_filter = ['statut', 'date_creation']
    search_fields = ['nom', 'email', 'code_unique', 'telephone']
    list_editable = ['statut']
    readonly_fields = ['code_unique', 'date_creation']