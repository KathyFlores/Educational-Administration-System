from django.contrib import admin

from .models import *

admin.site.register(Teacher)
admin.site.register(Student)


class ChoiceQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Content', {'fields': ['content']}),
        ('Choices', {'fields': ['choice_a', 'choice_b', 'choice_c', 'choice_d']}),
        ('Solution', {'fields': ['solution']}),
        ('Score', {'fields': ['score']}),
        ('Creator', {'fields': ['creator']}),
        ('Chapter', {'fields': ['chapter']}),
        ('Knowledge Point', {'fields': ['knowledge_point']}),
        ('Time information', {'fields': ['add_time', 'latest_modify_time']})
    ]


admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)


class TrueOrFalseQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Content', {'fields': ['content']}),
        ('Solution', {'fields': ['solution']}),
        ('Score', {'fields': ['score']}),
        ('Creator', {'fields': ['creator']}),
        ('Chapter', {'fields': ['chapter']}),
        ('Knowledge Point', {'fields': ['knowledge_point']}),
        ('Time information', {'fields': ['add_time', 'latest_modify_time']})
    ]


admin.site.register(TrueOrFalseQuestion, TrueOrFalseQuestionAdmin)


class TestAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['name']}),
        ('Creator', {'fields': ['creator']}),
        ('Attend Students', {'fields': ['attend_students']}),
        ('Questions', {'fields': ['choice_questions', 'true_or_false_questions']}),
        ('Time information', {'fields': ['start_time', 'end_time']})
    ]
    filter_horizontal = ('attend_students', 'choice_questions', 'true_or_false_questions')


admin.site.register(Test, TestAdmin)

admin.site.register(ChoiceQuestionAnswerRecord)
admin.site.register(TrueOrFalseQuestionAnswerRecord)

admin.site.register(Chapter)
admin.site.register(KnowledgePoint)
