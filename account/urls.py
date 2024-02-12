from django.contrib import admin
from django.urls import path
from account import views

urlpatterns = [
    path('account/',views.account,name='account'),
    path('lifting/',views.lifting,name='lifting'),
    path('liftingcart/',views.display_lifting_cart,name='liftingcart'),
    path('liftingcart/', views.display_lifting_cart, name='liftingcart'),
    path('finalize/', views.finalize_lifting_cart, name='finalize'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),



    path('sales/',views.sales,name='sales'),
    path('salescart/',views.salescart,name='salescart'),
    path('final/', views.final, name='final'),

    path('damage/', views.damage, name='damage'),
    path('damagecart/', views.add_to_damage, name='damagecart'),
    path('remove_from_damage/<int:damage_id>/', views.remove_from_damage, name='remove_from_damage'),
    path('damagecart/<int:mem_number>/', views.damagecart, name='damagecart'),

    

    path('bank_manage/', views.bank_manage, name='bank_manage'),
    path('supplierspayment/', views.supplierspayment, name='supplierspayment'),


    path('acdiccount/', views.acdiccount, name='acdiccount'),
    path('dailycost/', views.dailycost, name='dailycost'),
    path('chack/', views.chack, name='chack'),
    path('collection/', views.collection, name='collection'),
    path('assets/', views.assets, name='assets'),
    path('success/', views.success_page_view, name='success_page'),

    
]