from django.db import models

CHOICE = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D')
)


class Teacher(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=20)
    class_id = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    chapter = models.CharField(max_length=10)

    def __str__(self):
        return self.chapter


class KnowledgePoint(models.Model):
    knowledge_point = models.CharField(max_length=10)

    def __str__(self):
        return self.knowledge_point


class ChoiceQuestion(models.Model):
    content = models.TextField()

    choice_a = models.TextField()
    choice_b = models.TextField()
    choice_c = models.TextField()
    choice_d = models.TextField()

    solution = models.CharField(max_length=1, choices=CHOICE)

    score = models.PositiveSmallIntegerField(default=1)

    creator = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)

    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, blank=True, null=True)
    knowledge_point = models.ForeignKey(KnowledgePoint, on_delete=models.SET_NULL, blank=True, null=True)

    add_time = models.DateTimeField('time added')
    latest_modify_time = models.DateTimeField('time latest modified')

    def __str__(self):
        return self.content


class TrueOrFalseQuestion(models.Model):
    content = models.TextField()

    solution = models.BooleanField()

    score = models.PositiveSmallIntegerField(default=1)

    creator = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)

    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, blank=True, null=True)
    knowledge_point = models.ForeignKey(KnowledgePoint, on_delete=models.SET_NULL, blank=True, null=True)

    add_time = models.DateTimeField('time added')
    latest_modify_time = models.DateTimeField('time latest modified')

    def __str__(self):
        return self.content


class Test(models.Model):
    name = models.CharField(max_length=50)

    choice_questions = models.ManyToManyField(ChoiceQuestion, null=True, blank=True)
    true_or_false_questions = models.ManyToManyField(TrueOrFalseQuestion, null=True, blank=True)

    creator = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)

    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)

    attend_students = models.ManyToManyField(Student, null=True, blank=True)

    start_time = models.DateTimeField('date starts')
    end_time = models.DateTimeField('date ends')

    def __str__(self):
        return self.name


class ChoiceQuestionAnswerRecord(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
    answer = models.CharField(max_length=1, choices=CHOICE, blank=True, null=True, default=None)
    answer_time = models.DateTimeField('time answered', blank=True, null=True, default=None)


class TrueOrFalseQuestionAnswerRecord(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(TrueOrFalseQuestion, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
    answer = models.NullBooleanField(default=None, blank=True, null=True)
    answer_time = models.DateTimeField('time answered', default=None)
