from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    SEX_TYPES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )
    
    name = models.CharField(max_length=132)
    email = models.EmailField()
    phone = models.CharField(max_length=15)  # Ajusté pour un format de numéro de téléphone
    address = models.CharField(max_length=255)  # Augmenté pour permettre des adresses plus longues
    sex = models.CharField(max_length=1, choices=SEX_TYPES)
    age = models.CharField(max_length=10)  # Modifié pour être un CharField
    city = models.CharField(max_length=100)  # Augmenté pour des noms de ville plus longs
    zip_code = models.CharField(max_length=20)  # Ajusté pour différents formats de codes postaux
    created_date = models.DateTimeField(auto_now_add=True)
    save_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.name

class Invoice(models.Model):
    INVOICE_TYPE = (
        ('R', 'RECEIPT'),
        ('P', 'PROFORMA INVOICE'),
        ('I', 'INVOICE'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    save_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  
    invoice_date_time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Utilisation de Decimal pour une gestion précise
    last_updated_date = models.DateTimeField(null=True, blank=True)
    paid = models.BooleanField(default=True)
    invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE)
    comments = models.TextField(null=True, blank=True, max_length=1000)

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"

    def __str__(self):
        return f"{self.customer.name} - {self.invoice_date_time.strftime('%Y-%m-%d %H:%M')}"

class Article(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Augmenté pour des noms d'articles plus longs
    quantity = models.PositiveIntegerField()  # Utilisation de PositiveIntegerField
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    @property
    def total(self):
        return self.quantity * self.unit_price  # Calcul du total à la volée