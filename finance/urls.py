from django.urls import path

from finance import views
from finance.views import admin_feesI, admin_feesII, admin_feesIII, admin_payments, secretary_feesI, secretary_feesII, \
    secretary_feesIII, secretary_payments

app_name = 'finance'
urlpatterns = [
    path('view_fees/', views.view_fees,name="view_fees"),
    path('view_fee_details/<int:yearID>/', views.view_fee_details,name="view_fee_details"),
    path('parent_view_fees/', views.parent_view_fees, name="parent_view_fees"),
    path('parent_view_fee_details/<int:yearID>/', views.parent_view_fee_details, name="parent_view_fee_details"),
    path('admin_feesI/', admin_feesI, name='admin_feesI'),
    path('admin_feesII/<int:year_id>/<int:class_id>/<int:section_id>', admin_feesII,
         name='admin_feesII'),
    path('admin_feesIII/<int:student_id>', admin_feesIII,
         name='admin_feesIII'),
    path('admin_payments/<int:student_id>', admin_payments,
         name='admin_payments'),

    path('secretary_feesI/', secretary_feesI, name='secretary_feesI'),
    path('secretary_feesII/<int:year_id>/<int:class_id>/<int:section_id>', secretary_feesII,
         name='secretary_feesII'),
    path('secretary_feesIII/<int:student_id>', secretary_feesIII,
         name='secretary_feesIII'),
    path('secretary_payments/<int:student_id>', secretary_payments,
         name='secretary_payments'),

]