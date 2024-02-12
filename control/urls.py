
from django.contrib import admin
from django.urls import path
from control import views

urlpatterns = [
    path('control/',views.control,name='control'),
    path('supplieredit/',views.supplieredit,name='supplieredit'),
    path('brandedit/',views.brandedit,name='brandedit'),



    path('marketedit/<int:market_id>/', views.marketedit, name='marketedit'),
    path('market_list/', views.market_list, name='market_list'),

    #-----------------Dsr Edit Url---------------------------------------------#

    path('dsredit/<int:dsr_id>/', views.dsredit, name='dsredit'),
    path('dsr_list/', views.dsr_list, name='dsr_list'),

    #-----------------Dsr Edit Url end---------------------------------------------#

    path('bankedit/',views.bankedit,name='bankedit'),
#-----------------Product Edit Url---------------------------------------------#
    path('productedit/<int:product_id>/', views.productedit, name='productedit'),
    path('productlist/', views.product_list, name='product_list'),
#-----------------Product Edit Url End -----------------------------------------#

#----------------------------------Lifting Update  -----------------------------------------#
    path('lifting_update/',views.lifting_update,name='lifting_update'),
    path('update_lifting/', views.update_lifting, name='update_lifting'),
#----------------------------------Lifting Update End -----------------------------------------#

#----------------------------------All  Backdate  -----------------------------------------#
     path('lifting_backdate/', views.lifting_backdate, name='lifting_backdate'),
     path('sales_backdate/', views.sales_backdate, name='sales_backdate'),
     path('damage_backdate/', views.damage_backdate, name='damage_backdate'),
#---------------------------------- Backdate End  -----------------------------------------#


     path('lifting_delate/', views.lifting_delate, name='lifting_delate'),
     path('sales_delate/', views.sales_delate, name='sales_delate'),
     path('damage_delate/', views.damage_delate, name='damage_delate'),
     path('damage_delete_success/', views.damage_delete_success, name='damage_delete_success'),
     path('supplierpaymentupadte/', views.supplierpaymentupadte, name='supplierpaymentupadte'),
     path('update_supplier_payment/', views.update_supplier_payment, name='update_supplier_payment'),
     path('damagealldelate/', views.damagealldelate, name='damagealldelate'),
     
    


]