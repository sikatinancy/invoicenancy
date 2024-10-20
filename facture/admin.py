from django.contrib import admin
from .models import Customer, Invoice, Article  # Importation explicite des modèles

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'sex', 'age', 'city', 'zip_code')  # Affichage des champs
    search_fields = ('name', 'email')  # Ajout d'une fonctionnalité de recherche

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'saved_by', 'invoice_date_time', 'total', 'last_updated_date', 'paid')  # Affichage des champs
    list_filter = ('paid', 'invoice_date_time')  # Ajout de filtres pour faciliter la recherche

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'name', 'quantity', 'unit_price')  # Affichage des champs
    list_filter = ('invoice',)  # Filtres basés sur la facture

# Enregistrement des modèles avec leurs classes d'administration
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Article, ArticleAdmin)  # Enregistrement avec la classe ArticleAdmin