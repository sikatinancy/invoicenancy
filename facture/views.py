from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from .models import Customer, Invoice, Article
from django.contrib import messages
from django.db import transaction
from .utils import pagination

class HomeView(View):
    """Main view"""
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        invoices = Invoice.objects.select_related('customer', 'saved_by').all()
        customers = Customer.objects.select_related('saved_by').all()

        # Apply pagination
        items = pagination(request, invoices)

        # Create the context
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
            'saved_by': request.user,
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
        customers = Customer.objects.select_related('saved_by').all()
        context = {
            'customers': customers  
        }
        return render(request, self.template_name, context)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            customer_id = request.POST.get('customer')
            invoice_type = request.POST.get('invoice_type')
            articles = request.POST.getlist('article')
            qties = request.POST.getlist('qty')
            units = request.POST.getlist('unit')
            total_a = request.POST.getlist('total_a')

            # Calculer le total avec vérification des valeurs
            total = 0.0
            for t in total_a:
                try:
                    total += float(t)  # Ajoute chaque total à la somme
                except ValueError:
                    messages.error(request, f"Erreur dans la valeur totale : '{t}' n'est pas un nombre valide.")
                    return redirect('home')  # Redirige si une erreur se produit

            comment = request.POST.get('comment')

            # Créer la facture
            invoice_data = {
                'customer_id': customer_id,
                'saved_by': request.user,  # Assurez-vous que c'est une instance de User
                'total': total,
                'invoice_type': invoice_type,
                'comments': comment,
            }

            invoice = Invoice.objects.create(**invoice_data)

            # Liste pour les articles
            items = []
            for index, article in enumerate(articles):
                quantity = int(qties[index])
                unit_price = float(units[index])
                total_price = float(total_a[index])

                data = Article(
                    invoice_id=invoice.id,
                    name=article,
                    quantity=quantity,
                    unit_price=unit_price,
                    total=total_price,
                )
                items.append(data)

            # Enregistrer les articles
            Article.objects.bulk_create(items)
            messages.success(request, "Données enregistrées avec succès.")

        except Exception as e:
            messages.error(request, f"Désolé, l'erreur suivante s'est produite : {e}")

        return redirect('home')  # Redirige vers la page d'accueil après la création