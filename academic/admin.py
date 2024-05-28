from django.contrib import admin

from academic.models import StudyYear, Class, Section, Subject, ClassSubject, SchoolSittings, Grade, Assignment, Exam, \
    Attendance, Lecture, StudentSubject

admin.site.register(StudyYear)
admin.site.register(Class)
admin.site.site_header = 'SmartSchool Portal'
class SectionAdmin(admin.ModelAdmin):
    exclude = ('sectionID',)

admin.site.register(Section, SectionAdmin)
admin.site.register(Subject)
admin.site.register(ClassSubject)
admin.site.register(SchoolSittings)
admin.site.register(Grade)
admin.site.register(Assignment)
admin.site.register(Exam)
admin.site.register(Attendance)
admin.site.register(Lecture)
admin.site.register(StudentSubject)
