
from django.urls import path

from communication import views
from communication.views import DownloadFileViewInsert

app_name = 'communication'

urlpatterns = [
    path('send_message/', views.send_message,name="send_message"),
    path('send_parent_message/', views.send_parent_message, name="send_parent_message"),
    path('view_messages/', views.view_messages, name="view_messages"),
    path('message_details/<int:message_id>', views.message_details, name="message_details"),
    path('parent_view_messages/', views.parent_view_messages, name="parent_view_messages"),
    path('parent_message_details/<int:message_id>', views.parent_message_details, name="parent_message_details"),
    path('downloadI/<int:message_id>/', DownloadFileViewInsert.as_view(), name='download_fileI'),
    path('teacher_view_messages/', views.teacher_view_messages, name="teacher_view_messages"),
    path('teacher_view_message_details/<int:message_id>', views.teacher_view_message_details, name="teacher_view_message_details"),
    path('teacher_send_message/', views.teacher_send_message, name="teacher_send_message"),
    path('teacher_message_list_students/<int:year_id>/<int:class_id>/<int:section_id>/<int:subject_id>/',
         views.teacher_message_list_students, name='teacher_message_list_students'),
    path('teacher_send_message_student/<int:student_id>', views.teacher_send_message_student, name="teacher_send_message_student"),
    path('teacher_send_message_section/<int:year_id>/<int:class_id>/<int:section_id>/<int:subject_id>', views.teacher_send_message_section,
         name="teacher_send_message_section"),
    path('teacher_send_message_class/<int:year_id>/<int:class_id>/<int:subject_id>', views.teacher_send_message_class,
         name="teacher_send_message_class"),
    path('admin_view_messages/', views.admin_view_messages, name="admin_view_messages"),
    path('admin_view_message_details/<int:message_id>', views.admin_view_message_details,
         name="admin_view_message_details"),
    path('secretary_view_messages/', views.secretary_view_messages, name="secretary_view_messages"),
    path('secretary_view_message_details/<int:message_id>', views.secretary_view_message_details,
         name="secretary_view_message_details"),
    path('admin_post_adv/', views.admin_post_adv, name="admin_post_adv"),
    path('admin_view_adv/', views.admin_view_adv, name="admin_view_adv"),
    path('secretary_view_adv/', views.secretary_view_adv, name="secretary_view_adv"),
    path('teacher_view_adv/', views.teacher_view_adv, name="teacher_view_adv"),
    path('student_view_adv/', views.student_view_adv, name="student_view_adv"),
    path('parent_view_adv/', views.parent_view_adv, name="parent_view_adv"),

    path('admin_send_message/', views.admin_send_message, name="admin_send_message"),
    path('admin_send_message_employee/<int:employee_id>', views.admin_send_message_employee, name="admin_send_message_employee"),
    path('admin_send_message_employees', views.admin_send_message_employees,
         name="admin_send_message_employees"),

    path('admin_message_list_students/<int:year_id>/<int:class_id>/<int:section_id>',
         views.admin_message_list_students, name='admin_message_list_students'),
    path('admin_send_message_student/<int:student_id>', views.admin_send_message_student,
         name="admin_send_message_student"),
    path('admin_send_message_section/<int:year_id>/<int:class_id>/<int:section_id>',
         views.admin_send_message_section,
         name="admin_send_message_section"),
    path('admin_send_message_class/<int:year_id>/<int:class_id>', views.admin_send_message_class,
         name="admin_send_message_class"),
    path('admin_send_message_users/', views.admin_send_message_users,
         name="admin_send_message_users"),

    path('secretary_send_message/', views.secretary_send_message, name="secretary_send_message"),
    path('secretary_send_message_employee/<int:employee_id>', views.secretary_send_message_employee,
         name="secretary_send_message_employee"),
    path('secretary_message_list_students/<int:year_id>/<int:class_id>/<int:section_id>',
         views.secretary_message_list_students, name='secretary_message_list_students'),
    path('secretary_send_message_student/<int:student_id>', views.secretary_send_message_student,
         name="secretary_send_message_student"),
    path('secretary_send_message_section/<int:year_id>/<int:class_id>/<int:section_id>',
         views.secretary_send_message_section,
         name="secretary_send_message_section"),
    path('secretary_send_message_class/<int:year_id>/<int:class_id>', views.secretary_send_message_class,
         name="secretary_send_message_class"),
    path('secretary_send_message_users/', views.secretary_send_message_users,
         name="secretary_send_message_users"),

]