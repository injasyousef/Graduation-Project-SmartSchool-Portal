from django.urls import path

from health_and_behavioral import views
from health_and_behavioral.views import admin_behavioral_recordI, admin_behavioral_recordII, admin_behavioral_recordIII, \
    admin_behavioral_recordIIII, admin_behavioral_record_edit, admin_health_recordI, admin_health_recordII, \
    admin_health_recordIII, admin_health_recordIIII, admin_health_record_edit, secretary_behavioral_recordI, \
    secretary_behavioral_recordII, secretary_behavioral_recordIII, secretary_behavioral_recordIIII, \
    secretary_behavioral_record_edit, seretary_health_recordI, seretary_health_recordII, seretary_health_recordIII, \
    seretary_health_recordIIII, seretary_health_record_edit

app_name = 'health_and_behavioral'
urlpatterns = [
    path('view_health_records/', views.view_health_records,name="view_health_records"),
    path('view_behaviour_evaluation/', views.view_behaviour_evaluation, name="view_behaviour_evaluation"),
    path('admin_behavioral_recordI/', admin_behavioral_recordI, name='admin_behavioral_recordI'),
    path('admin_behavioral_recordII/<int:year_id>/<int:class_id>/<int:section_id>', admin_behavioral_recordII,
         name='admin_behavioral_recordII'),
    path('admin_behavioral_recordIII/<int:student_id>/', admin_behavioral_recordIII, name='admin_behavioral_recordIII'),
    path('admin_behavioral_recordIIII/<int:student_id>/', admin_behavioral_recordIIII, name='admin_behavioral_recordIIII'),
    path('admin_behavioral_record_edit/<int:behavioral_id>/', admin_behavioral_record_edit,
         name='admin_behavioral_record_edit'),
    path('admin_health_recordI/', admin_health_recordI, name='admin_health_recordI'),
    path('admin_health_recordII/<int:year_id>/<int:class_id>/<int:section_id>', admin_health_recordII,
         name='admin_health_recordII'),
    path('admin_health_recordIII/<int:student_id>/', admin_health_recordIII, name='admin_health_recordIII'),
    path('admin_health_recordIIII/<int:student_id>/', admin_health_recordIIII,
         name='admin_health_recordIIII'),
    path('admin_health_record_edit/<int:health_id>/', admin_health_record_edit,
         name='admin_health_record_edit'),

    path('parent_view_health_records/', views.parent_view_health_records,name="parent_view_health_records"),
    path('parent_view_behaviour_evaluation/', views.parent_view_behaviour_evaluation, name="parent_view_behaviour_evaluation"),

    path('secretary_behavioral_recordI/', secretary_behavioral_recordI, name='secretary_behavioral_recordI'),
    path('secretary_behavioral_recordII/<int:year_id>/<int:class_id>/<int:section_id>', secretary_behavioral_recordII,
         name='secretary_behavioral_recordII'),
    path('secretary_behavioral_recordIII/<int:student_id>/', secretary_behavioral_recordIII, name='secretary_behavioral_recordIII'),
    path('secretary_behavioral_recordIIII/<int:student_id>/', secretary_behavioral_recordIIII,
         name='secretary_behavioral_recordIIII'),
    path('secretary_behavioral_record_edit/<int:behavioral_id>/', secretary_behavioral_record_edit,
         name='secretary_behavioral_record_edit'),

    path('seretary_health_recordI/', seretary_health_recordI, name='seretary_health_recordI'),
    path('seretary_health_recordII/<int:year_id>/<int:class_id>/<int:section_id>', seretary_health_recordII,
         name='seretary_health_recordII'),
    path('seretary_health_recordIII/<int:student_id>/', seretary_health_recordIII, name='seretary_health_recordIII'),
    path('seretary_health_recordIIII/<int:student_id>/', seretary_health_recordIIII,
         name='seretary_health_recordIIII'),
    path('seretary_health_record_edit/<int:health_id>/', seretary_health_record_edit,
         name='seretary_health_record_edit'),

]