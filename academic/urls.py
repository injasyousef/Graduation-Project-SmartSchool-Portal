from django.urls import path

from academic import views
from academic.views import DownloadFileView, DownloadFileViewInsert, get_classes_for_year, \
    teacher_insert_grades, get_sections_for_class_and_year, get_subjects_for_section, list_student, \
    teacher_new_assignment, get_subjects_for_class, teacher_add_new_assignment, teacher_view_assignments, \
    list_students_for_assignments, assignments_for_student, assignment_grading, DownloadFileSubmited, teacher_exams, \
    teacher_exams_list_students, teacher_exams_new_exam, exams_for_student, exam_grading, admin_record_attendenceI, \
    admin_record_attendenceII, admin_record_attendenceIII, admin_record_attendenceIIII, admin_record_attendence_edit, \
    admin_new_class, admin_new_section, admin_new_subject, admin_new_year, admin_edit_studentI, admin_edit_studentII, \
    admin_edit_employeeI, admin_edit_employeeII, secretary_record_attendenceI, secretary_record_attendenceII, \
    secretary_record_attendenceIII, secretary_record_attendenceIIII, secretary_record_attendence_edit, \
    secretaty_edit_studentI, secretaty_edit_studentII, secretary_new_class, secretary_new_section, secretary_new_subject

app_name = 'academic'

urlpatterns = [
    path('base_view_grades/', views.base_view_grades, name="base_view_grades"),
    path('view_attendance/', views.view_attendance, name="view_attendance"),
    path('see_assignments/', views.see_assignments, name="see_assignments"),
    path('parent_view_assignments/', views.parent_view_assignments, name="parent_view_assignments"),
    path('view_exams/', views.view_exams, name="view_exams"),
    path('parent_view_exams/', views.parent_view_exams, name="parent_view_exams"),
    path('view_assignment_details/<int:assignment_id>/', views.view_assignment_details, name="view_assignment_details"),
    path('view_weekly_schedule', views.view_weekly_schedule, name="view_weekly_schedule"),
    path('view_lecture_details/<int:lectureID>/', views.view_lecture_details, name="view_lecture_details"),
    path('parent_view_weekly_schedule', views.parent_view_weekly_schedule, name="parent_view_weekly_schedule"),
    path('parent_view_lecture_details/<int:lectureID>/', views.parent_view_lecture_details, name="parent_view_lecture_details"),
    path('download/<int:assignment_id>/', DownloadFileView.as_view(), name='download_file'),
    path('downloadI/<int:assignment_id>/', DownloadFileViewInsert.as_view(), name='download_fileI'),
    path('downloadII/<int:assignment_id>/', DownloadFileSubmited.as_view(), name='download_fileII'),
    path('teacher_insert_grades/', teacher_insert_grades, name='teacher_insert_grades'),
    path('ajax/get-classes-for-year/', get_classes_for_year, name='ajax-get-classes-for-year'),
    path('ajax/get-sections-for-class-and-year/', get_sections_for_class_and_year,
         name='ajax-get-sections-for-class-and-year'),
    path('ajax/get-subjects-for-section/', get_subjects_for_section, name='ajax-get-subjects-for-section'),
    path('list_student/', list_student, name='list_student'),
    path('student_details/<int:student_id>/<int:year_id>/<int:class_id>/<int:section_id>/<int:subject_id>/',
         views.student_grade, name='student_grade'),
    path('teacher_new_assignment/', teacher_new_assignment, name='teacher_new_assignment'),
    path('ajax/get_subjects_for_class/', views.get_subjects_for_class, name='ajax-get_subjects_for_class'),
    path('teacher_add_new_assignment/', teacher_add_new_assignment, name='teacher_add_new_assignment'),
    path('teacher_view_assignments/', teacher_view_assignments, name='teacher_view_assignments'),
    path('list_students_for_assignments/', list_students_for_assignments, name='list_students_for_assignments'),
    path('assignments_for_student/<int:student_id>/<int:year_id>/<int:class_id>/<int:section_id>/<int:subject_id>/',
         assignments_for_student, name='assignments_for_student'),
    path('assignment_grading/<int:assignment_id>/',assignment_grading, name='assignment_grading'),
    path('teacher_exams/', teacher_exams, name='teacher_exams'),
    path('teacher_exams_list_exams/<int:year_id>/<int:class_id>/<int:section_id>/<int:subject_id>/',
         teacher_exams_list_students, name='teacher_exams_list_exams'),
    path('teacher_exams_new_exam/<int:year_id>/<int:class_id>/<int:section_id>/<int:subject_id>/',
         teacher_exams_new_exam, name='teacher_exams_new_exam'),
    path('exams_for_student/<int:student_id>/<int:year_id>/<int:class_id>/<int:section_id>/<int:subject_id>/',
         exams_for_student, name='exams_for_student'),
    path('exam_grading/<int:exam_id>/', exam_grading, name='exam_grading'),
    path('admin_record_attendenceI/', admin_record_attendenceI, name='admin_record_attendenceI'),
    path('admin_record_attendenceII/<int:year_id>/<int:class_id>/<int:section_id>', admin_record_attendenceII, name='admin_record_attendenceII'),
    path('admin_record_attendenceIII/<int:student_id>/', admin_record_attendenceIII, name='admin_record_attendenceIII'),
    path('admin_record_attendenceIIII/<int:student_id>/', admin_record_attendenceIIII, name='admin_record_attendenceIIII'),
    path('admin_record_attendence_edit/<int:attendence_id>/', admin_record_attendence_edit,
         name='admin_record_attendence_edit'),
    path('secretary_record_attendenceI/', secretary_record_attendenceI, name='secretary_record_attendenceI'),
    path('secretary_record_attendenceII/<int:year_id>/<int:class_id>/<int:section_id>', secretary_record_attendenceII,
         name='secretary_record_attendenceII'),
    path('secretary_record_attendenceIII/<int:student_id>/', secretary_record_attendenceIII, name='secretary_record_attendenceIII'),
    path('secretary_record_attendenceIIII/<int:student_id>/', secretary_record_attendenceIIII,
         name='secretary_record_attendenceIIII'),
    path('secretary_record_attendence_edit/<int:attendence_id>/', secretary_record_attendence_edit,
         name='secretary_record_attendence_edit'),
    path('teacher_insert_grades2/', views.teacher_insert_grades2, name='teacher_insert_grades2'),
    path('save_grades/', views.save_grades, name='save_grades'),
    path('admin_new_class/', admin_new_class, name='admin_new_class'),
    path('admin_new_section/', admin_new_section, name='admin_new_section'),
    path('admin_new_subject/', admin_new_subject, name='admin_new_subject'),
    path('secretary_new_class/', secretary_new_class, name='secretary_new_class'),
    path('secretary_new_section/', secretary_new_section, name='secretary_new_section'),
    path('secretary_new_subject/', secretary_new_subject, name='secretary_new_subject'),
    path('admin_new_year/', admin_new_year, name='admin_new_year'),
    path('ajax/get-students-for-class-section-and-year/', views.get_students_for_class_section_and_year,
         name='ajax-get-students-for-class-section-and-year'),

    path('admin_edit_studentI/', admin_edit_studentI, name='admin_edit_studentI'),
    path('admin_edit_studentII/<int:student_id>/', admin_edit_studentII, name='admin_edit_studentII'),
    path('secretaty_edit_studentI/', secretaty_edit_studentI, name='secretaty_edit_studentI'),
    path('secretaty_edit_studentII/<int:student_id>/', secretaty_edit_studentII, name='secretaty_edit_studentII'),
    path('admin_edit_employeeI/', admin_edit_employeeI, name='admin_edit_employeeI'),
    path('edit-admin_edit_employeeII/<int:employee_id>/', admin_edit_employeeII, name='admin_edit_employeeII'),
    path('parent_view_grades/', views.parent_view_grades, name='parent_view_grades'),
    path('parent_view_attendance/', views.parent_view_attendance, name="parent_view_attendance"),

]
