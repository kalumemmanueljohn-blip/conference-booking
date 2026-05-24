from django.urls import path
from reservations.views import test_email

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('waiting/<int:id>/', views.waiting, name='waiting'),
    path('whatsapp/<int:id>/', views.whatsapp, name='whatsapp'),
    path('valider/<int:id>/', views.valider, name='valider'),
    path('stats/', views.stats, name='stats'),
    path('vider-dashboard/', views.vider_dashboard, name='vider_dashboard'),
    path('supprimer-selection/', views.supprimer_selection, name='supprimer_selection'),
    path('contact/', views.contact, name='contact'),
    path('mentions-legales/', views.mentions, name='mentions'),
    path('mentions/', views.mentions, name='mentions_court'),
    path('ticket/<str:code_unique>/', views.download_ticket), 
    path('test-email/', test_email, name='test_email'),     
]
