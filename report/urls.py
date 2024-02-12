
from django.contrib import admin
from django.urls import path
from report import views

urlpatterns = [
    path('report/',views.report,name='report'),
    path('stockreport/',views.stockreport,name='stockreport'),
    path('liftingreport/', views.liftingreport, name='liftingreport'),

    path('salesreport/', views.salesreport, name='salesreport'),
    path('salesreportresult/', views.sales_report_result, name='salesreportresult'),
    path('dsrsalesreport/', views.dsrsalesreport, name='dsrsalesreport'),
    path('market_salesreport/', views.market_salesreport, name='market_salesreport'),
    path('dsrsalesreportinvoice/', views.dsrsalesreportinvoice, name='dsrsalesreportinvoice'),




    path('damagereport/', views.damagereport, name='damagereport'),
    path('damagereportwithinvoivce/', views.damagereportwithinvoivce, name='damagereportwithinvoivce'),
    path('damagewithtable/<str:mem_number>/', views.damagewithtable, name='damagewithtable'),


    path('damagereportresult/', views.damage_report_result, name='damagereportresult'),


    path('supplierledgerreport/', views.supplier_ledger_report, name='supplierledgerreport'),
    path('supplierledgerresult/', views.supplier_ledger_result, name='supplierledgerresult'),
   

    path('profitlossreport/', views.profit_loss_report, name='profitlossreport'),
    path('profitlossreportresult/', views.profit_loss_result, name='profitlossreportresult'), 


    path('calculation/', views.calculate_profit_loss_and_commission, name='calculation'), 

    path('discountreport/', views.discountreport, name='discountreport'), 
    path('discountreportresult/', views.discountreportresult, name='discountreportresult'), 


    path('costreport/', views.costreport, name='costreport'),  
    path('costreportresult/', views.costreportresult, name='costreportresult'),
    
    path('statement/', views.statement, name='statement'),  
    path('statementreportresult/', views.statementreportresult, name='statementreportresult'),
     path('statementreportresultall/', views.statementreportresultall, name='statementreportresultall'),
     path('searchkg/', views.searchkg, name='searchkg'),
    path('findkg/', views.findkg, name='findkg'),
    
    path('assetview/', views.assetview, name='assetview'),  
    
    path('assetviewrs/', views.assetviewrs, name='assetviewrs'), 
    

    
]