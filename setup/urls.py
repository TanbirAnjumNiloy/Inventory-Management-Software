
from django.contrib import admin
from django.urls import path
from setup import views

urlpatterns = [
    path('setup/',views.setup,name='setup'),
    
    path('suppliers_setup/', views.suppliers_setup, name='suppliers_setup'),

    path('brand_setup/', views.brand_setup, name='brand_setup'),

    path('group_name/', views.group_name, name='group_name'),

    path('product_name/', views.product_name, name='product_name'),

    path('market_setup/', views.market_setup, name='market_setup'),

    path('bank_setup/', views.bank_setup, name='bank_setup'),

    path('dsr_setup/', views.dsr_setup, name='dsr_setup'),

    path('do_setup/', views.do_setup, name='do_setup'),

    path('sell_setup/', views.sell_setup, name='sell_setup'),

    path('salesmanager/', views.salesmanager, name='salesmanager'),

    path('discountsetup/', views.discountsetup, name='discountsetup'),

    path('collectionsetup/', views.collectionsetup, name='collectionsetup'),

    path('grams/', views.grams, name='grams'),


    
    
]
