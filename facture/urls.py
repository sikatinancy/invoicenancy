# from django.urls import path
# from.import views

# urlpattens = [
#     path('', views.home,name='home'),

# ]

# facture/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('add-customer', views.AddCustomerView.as_view(), name='add-customer'), 
    path('add-invoice',views.AddInvoiceView.as_view(), name='add-invoice'),
    # path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail')

    # Add more patterns as needed
]