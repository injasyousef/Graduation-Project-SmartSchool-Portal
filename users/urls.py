from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView
from django.urls import path

from users import views
from users.views import welcome, user_login, user_logout, CustomPasswordResetView, admin_add_employee, \
    admin_add_user_employee, admin_add_student, admin_add_user_student, secretary_add_student, \
    secretary_add_user_student

app_name = 'users'
urlpatterns = [
    path('welcome/', welcome, name='welcome'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('view_settings/', views.view_settings, name='view_settings'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('teacher_change_password/', views.teacher_change_password, name='teacher_change_password'),
    path('teacher_view_settings/', views.teacher_view_settings, name='teacher_view_settings'),
    path('teacher_view_profile/', views.teacher_view_profile, name='teacher_view_profile'),
    path('admin_add_employee/', admin_add_employee, name='admin_add_employee'),
    path('admin_add_user_employee/<int:employee_id>', admin_add_user_employee, name='admin_add_user_employee'),
    path('admin_add_student/', admin_add_student, name='admin_add_student'),
    path('admin_add_user_student/<int:student_id>', admin_add_user_student, name='admin_add_user_student'),
    path('secretary_add_student/', secretary_add_student, name='secretary_add_student'),
    path('secretary_add_user_student/<int:student_id>', secretary_add_user_student, name='secretary_add_user_student'),
    path('admin_change_password/', views.admin_change_password, name='admin_change_password'),
    path('admin_view_settings/', views.admin_view_settings, name='admin_view_settings'),
    path('admin_view_profile/', views.admin_view_profile, name='admin_view_profile'),
    path('parent_view_settings/', views.parent_view_settings, name='parent_view_settings'),
    path('parent_view_profile/', views.parent_view_profile, name='parent_view_profile'),
    path('parent_change_password/', views.parent_change_password, name='parent_change_password'),
    path('secretary_change_password/', views.secretary_change_password, name='secretary_change_password'),
    path('secretary_view_settings/', views.secretary_view_settings, name='secretary_view_settings'),
    path('secretary_view_profile/', views.secretary_view_profile, name='secretary_view_profile'),


]
