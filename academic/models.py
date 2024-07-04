# academic/models.py
from django.db import models

from times.models import Time, Day
from users.models import Employee, Student, UserEmployee


class StudyYear(models.Model):
    yearID = models.AutoField(primary_key=True)
    yearName = models.CharField(max_length=255)

    def __str__(self):
        return self.yearName


class Class(models.Model):
    classID = models.AutoField(primary_key=True)
    className = models.CharField(max_length=255)
    classNameOther = models.CharField(max_length=255)
    isActive = models.BooleanField()
    next_class = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='previous_class')

    def __str__(self):
        return self.className


class Section(models.Model):
    year = models.ForeignKey(StudyYear, on_delete=models.CASCADE)
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    sectionID = models.IntegerField(unique=True)
    sectionSymbol = models.CharField(max_length=255)
    description = models.TextField()
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.sectionID:
            last_section = Section.objects.order_by('-sectionID').first()
            if last_section:
                self.sectionID = last_section.sectionID + 1
            else:
                self.sectionID = 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['sectionID']

    # def __str__(self):
    #     return f"{self.sectionSymbol} - {self.year.yearName}"
    def __str__(self):
        return self.sectionSymbol


class Subject(models.Model):
    subjectID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    subjectTextBook = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class StudentSubject(models.Model):
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    subjectID = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('studentID', 'subjectID')

    def __str__(self):
        return f"{self.subjectID.name} - {self.studentID.fullName}"


class ClassSubject(models.Model):
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.ForeignKey(StudyYear, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subject', 'school_class','year')

    def __str__(self):
        return f"{self.subject} - {self.school_class.className} ({self.year})"


class SchoolSittings(models.Model):
    year = models.OneToOneField(StudyYear, primary_key=True, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()


class Grade(models.Model):
    year = models.ForeignKey(StudyYear, on_delete=models.CASCADE)
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    gradeID = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Employee, on_delete=models.CASCADE)
    firstQuarter = models.FloatField(null=True, blank=True)
    secondQuarter = models.FloatField(null=True, blank=True)
    firstSemester = models.FloatField(null=True, blank=True)
    thirdQuarter = models.FloatField(null=True, blank=True)
    fourthQuarter = models.FloatField(null=True, blank=True)
    secondSemester = models.FloatField(null=True, blank=True)
    finalAvg = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('year', 'school_class', 'section', 'student', 'subject', 'gradeID')

    def save(self, *args, **kwargs):
        if self.firstQuarter is not None and self.secondQuarter is not None:
            self.firstSemester = self.firstQuarter + self.secondQuarter
        if self.thirdQuarter is not None and self.fourthQuarter is not None:
            self.secondSemester = self.thirdQuarter + self.fourthQuarter

        if self.firstSemester is not None and self.secondSemester is not None:
            self.finalAvg = self.firstSemester + self.secondSemester

        super().save(*args, **kwargs)


class Assignment(models.Model):
    assignmentID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    dueDate = models.DateField()
    fileInsert = models.FileField(upload_to='assignments_inserted/', null=True, blank=True)
    teacher = models.ForeignKey(Employee, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    year = models.ForeignKey(StudyYear, on_delete=models.CASCADE)
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    fileSubmit = models.FileField(upload_to='assignments_submit/', null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    linkInsert = models.URLField(null=True, blank=True)
    assignmentGrade = models.FloatField(null=True, blank=True)
    assignmentFinalGrade = models.FloatField(null=True, blank=True)
    submit = models.BooleanField(default=False)
    submit_text = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'year', 'school_class', 'section', 'assignmentID')


class Exam(models.Model):
    year = models.ForeignKey(StudyYear, on_delete=models.CASCADE)
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    examID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    teacher = models.ForeignKey(Employee, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    examGrade = models.FloatField(null=True, blank=True)
    finalGrade = models.FloatField(null=True, blank=True)
    insertingTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('year', 'school_class', 'section', 'student', 'examID')


class Attendance(models.Model):
    year = models.ForeignKey(StudyYear, on_delete=models.CASCADE)
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.CharField(max_length=255)
    excuse = models.CharField(max_length=255)
    notes = models.TextField()
    insertedUserID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    insertingTime = models.DateTimeField()

    class Meta:
        unique_together = ('year', 'school_class', 'section', 'student', 'date')


class Lecture(models.Model):
    lectureID = models.AutoField(primary_key=True)
    classID = models.ForeignKey(Class, on_delete=models.CASCADE)
    sectionID = models.ForeignKey(Section, on_delete=models.CASCADE)
    subjectID = models.ForeignKey(Subject, on_delete=models.CASCADE)
    yearID = models.ForeignKey(StudyYear, on_delete=models.CASCADE)
    teacherID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    startTime = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='start_time')
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    endTime = models.ForeignKey(Time, on_delete=models.CASCADE)
    roomNumber = models.CharField(max_length=255)
