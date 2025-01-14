from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from .models import Customer, Invoice, Article
from django.contrib import messages
from django.db import transaction
from .utils import pagination

class HomeView(View):
    """Vue principale"""
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        invoices = Invoice.objects.select_related('customer', 'saved_by').all()
        customers = Customer.objects.select_related('saved_by').all()

        # Appliquer la pagination
        items = pagination(request, invoices)

        # Créer le contexte
        context = {
            'invoices': items,
            'customers': customers
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Modification de la facture
        if request.POST.get('id_modify'):
            paid = request.POST.get('modify')
            try:
                invoice = Invoice.objects.get(id=request.POST.get('id_modify'))
                invoice.paid = paid == 'True'  # Convertir en booléen
                invoice.save()
                messages.success(request, "Changement effectué avec succès.")
            except Invoice.DoesNotExist:
                messages.error(request, "La facture n'existe pas.")
            except Exception as e:
                messages.error(request, f"Désolé, une erreur est survenue : {e}.")

        # Récupérer à nouveau les factures et les clients
        invoices = Invoice.objects.select_related('customer', 'saved_by').all()
        customers = Customer.objects.select_related('saved_by').all()
        items = pagination(request, invoices)

        context = {
            'invoices': items,
            'customers': customers
        }

        return render(request, self.template_name, context)

class AddCustomerView(View):
    """Ajouter un nouveau client"""
    template_name = 'add_customer.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

    
    def post(self, request, *args, **kwargs):
        # Collecter les données du POST
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'sex': request.POST.get('sex'),
            'age': request.POST.get('age'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip'),
            'saved_by': request.user if request.user.is_authenticated else None,  # Utilisateur authentifié ou None
        }
        
        try:
            # Créer le nouveau client
            customer = Customer.objects.create(**data)
            messages.success(request, "Client enregistré avec succès.")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Désolé, notre système a détecté les problèmes suivants : {e}")
            return render(request, self.template_name, {'data': data})


class AddInvoiceView(View):
    """Ajouter une nouvelle facture"""
    template_name = 'add_invoice.html'

    def get(self, request, *args, **kwargs):
        # Récupérer les clients pour l'affichage du formulaire
        customers = Customer.objects.all()
        return render(request, self.template_name, {'customers': customers})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            # Collecter les données de la facture depuis le POST
            customer_id = request.POST.get('customer')
            invoice_type = request.POST.get('invoice_type')
            articles = request.POST.getlist('article')
            qties = request.POST.getlist('qty')
            units = request.POST.getlist('unit')
            total_a = request.POST.getlist('total-a')
            comment = request.POST.get('comment')

            # Valider que toutes les informations nécessaires sont présentes
            if not all([customer_id, invoice_type, articles, qties, units, total_a]):
                messages.error(request, "Erreur : Tous les champs sont nécessaires.")
                return redirect('add_invoice')

            # Calculer le total à partir des articles
            total = sum(float(total_a[i]) for i in range(len(total_a)))

            # Préparer les données de la facture
            invoice_data = {
                'customer_id': customer_id,
                'invoice_type': invoice_type,
                'total': total,  # Calculé dynamiquement ici
                'comments': comment,
                'saved_by': request.user if request.user.is_authenticated else None  # Utilisateur authentifié ou None
            }

            # Créer la facture
            invoice = Invoice.objects.create(**invoice_data)

            # Créer les articles associés à la facture
            items = []
            for index, article in enumerate(articles):
                quantity = float(qties[index])
                unit_price = float(units[index])
                total_price = float(total_a[index])

                # Créer l'objet Article pour chaque article
                item = Article(
                    invoice_id=invoice.id,
                    name=article,
                    quantity=quantity,
                    unit_price=unit_price,
                    total=total_price,
                )
                items.append(item)

            # Enregistrer les articles dans la base de données
            Article.objects.bulk_create(items)

            messages.success(request, "Facture enregistrée avec succès.")
            return redirect('home')  # Rediriger vers la page d'accueil ou une autre page

        except Exception as e:
            messages.error(request, f"Désolé, une erreur est survenue : {e}")
            return redirect('add_invoice')  # Rediriger vers la même page pour corriger l'erreur
