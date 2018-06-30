from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.views import generic
import json
import datetime
from .models import Test, ChoiceQuestionAnswerRecord, ChoiceQuestion, TrueOrFalseQuestionAnswerRecord, \
    TrueOrFalseQuestion, Chapter, KnowledgePoint

from basicInfo.models import course as Subject, teach as Teach, student as Student, teacher as Teacher, \
    account as Account
from courseSelect.models import Selection


# login_student = Student.objects.all()[0]
# login_student = None
# # login_teacher = Teacher.objects.all()[0]
# login_teacher = None


class SubjectsTeacherView(generic.ListView):
    model = Subject
    template_name = 'online_test/subjects_teacher.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # object_list = login_teacher.subjects.all()
        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account

        login_teacher = Teacher.objects.get(teacher_id=account_id)

        object_list = []
        for teach in Teach.objects.filter(teacher_id=login_teacher):
            object_list.append(teach.course_id)
        context['object_list'] = object_list

        return context


class SubjectsStudentView(generic.ListView):
    model = Subject
    template_name = 'online_test/subjects_student.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # object_list = login_student.subjects.all()
        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account
        login_student = Student.objects.get(student_id=account_id)

        object_list = []
        for teach in Selection.objects.filter(student=login_student, state=True):
            object_list.append(teach.teach.course_id)
        context['object_list'] = object_list
        return context


class TestsView(generic.ListView):
    model = Test
    template_name = 'online_test/tests.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        subject = Subject.objects.get(course_id=self.kwargs['subject'])

        context = super().get_context_data(**kwargs)

        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account
        login_student = Student.objects.get(student_id=account_id)

        object_list = Test.objects.filter(attend_students=login_student, subject=subject)
        context['object_list'] = object_list
        context['subject_id'] = subject.course_id
        return context


class TestDetail(generic.DetailView):
    model = Test
    template_name = 'online_test/test_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account
        login_student = Student.objects.get(student_id=account_id)

        context['choice_question_answer_record'] = {}
        for record in ChoiceQuestionAnswerRecord.objects.filter(test=self.object, student=login_student):
            context['choice_question_answer_record'][record.question.id] = record.answer
            print(record.answer, record.id, record.question)

        context['true_or_false_question_answer_record'] = {}
        for record in TrueOrFalseQuestionAnswerRecord.objects.filter(test=self.object, student=login_student):
            # context['true_or_false_question_answer_record'][record.id] = 'T' if record.answer else 'F'
            print(record.answer, record.id, record.question)

            if record.answer == True:
                context['true_or_false_question_answer_record'][record.question.id] = 'T'
            elif record.answer == False:
                context['true_or_false_question_answer_record'][record.question.id] = 'F'
            else:
                context['true_or_false_question_answer_record'][record.question.id] = 'None'

        return context


class TeacherStatisticsTests(generic.ListView):
    model = Test
    template_name = 'online_test/teacher_statistics_tests.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        subject = Subject.objects.get(course_id=self.kwargs['subject'])
        context = super().get_context_data(**kwargs)

        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account
        login_teacher = Teacher.objects.get(teacher_id=account_id)

        object_list = Test.objects.filter(creator=login_teacher, subject=subject)
        context['object_list'] = object_list
        context['subject_id'] = subject.course_id

        return context


class TeacherStatisticsChapters(generic.ListView):
    model = Chapter
    template_name = 'online_test/teacher_statistics_chapters.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account
        login_teacher = Teacher.objects.get(teacher_id=account_id)

        subject = Subject.objects.get(course_id=self.kwargs['subject'])

        object_list = {}
        for test in Test.objects.filter(creator=login_teacher, subject=subject):
            for record in ChoiceQuestionAnswerRecord.objects.filter(test=test):
                if record.question.chapter not in object_list.keys():
                    object_list[record.question.chapter] = {'correct_num': 0, 'total_num': 1}
                    if record.answer == record.question.solution:
                        object_list[record.question.chapter]['correct_num'] += 1
                else:
                    object_list[record.question.chapter]['total_num'] += 1
                    if record.answer == record.question.solution:
                        object_list[record.question.chapter]['correct_num'] += 1

            for record in TrueOrFalseQuestionAnswerRecord.objects.filter(test=test):
                if record.question.chapter not in object_list.keys():
                    object_list[record.question.chapter] = {'correct_num': 0, 'total_num': 1}
                    if record.answer == record.question.solution:
                        object_list[record.question.chapter]['correct_num'] += 1
                else:
                    object_list[record.question.chapter]['total_num'] += 1
                    if record.answer == record.question.solution:
                        object_list[record.question.chapter]['correct_num'] += 1
        context['object_list'] = object_list
        context['subject_id'] = subject.course_id

        return context


class TeacherStatisticsKnowledgePoints(generic.ListView):
    model = KnowledgePoint
    template_name = 'online_test/teacher_statistics_knowledge_points.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account
        login_teacher = Teacher.objects.get(teacher_id=account_id)

        subject = Subject.objects.get(course_id=self.kwargs['subject'])

        object_list = {}
        for test in Test.objects.filter(creator=login_teacher, subject=subject):
            print(test)
            for record in ChoiceQuestionAnswerRecord.objects.filter(test=test):
                if record.question.knowledge_point not in object_list.keys():
                    object_list[record.question.knowledge_point] = {'correct_num': 0, 'total_num': 1}
                    if record.answer == record.question.solution:
                        object_list[record.question.knowledge_point]['correct_num'] += 1
                else:
                    object_list[record.question.knowledge_point]['total_num'] += 1
                    if record.answer == record.question.solution:
                        object_list[record.question.knowledge_point]['correct_num'] += 1

            for record in TrueOrFalseQuestionAnswerRecord.objects.filter(test=test):
                if record.question.knowledge_point not in object_list.keys():
                    object_list[record.question.knowledge_point] = {'correct_num': 0, 'total_num': 1}
                    if record.answer == record.question.solution:
                        object_list[record.question.knowledge_point]['correct_num'] += 1
                else:
                    object_list[record.question.knowledge_point]['total_num'] += 1
                    if record.answer == record.question.solution:
                        object_list[record.question.knowledge_point]['correct_num'] += 1
        context['object_list'] = object_list
        context['subject_id'] = subject.course_id

        return context


class TestStatistics(generic.DetailView):
    model = Test
    template_name = 'online_test/test_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test_score = 0

        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account

        assert isinstance(self.object, Test)

        for question in self.object.choice_questions.all():
            test_score += question.score

        for question in self.object.true_or_false_questions.all():
            test_score += question.score

        avg_score = 0
        student_scores = []
        for student in self.object.attend_students.all():
            student_info = {'id': student.student_id, 'name': student.name, 'score': 0}
            for record in ChoiceQuestionAnswerRecord.objects.filter(test=self.object, student=student):
                if record.answer == record.question.solution:
                    avg_score += record.question.score
                    student_info['score'] = student_info['score'] + record.question.score
            for record in TrueOrFalseQuestionAnswerRecord.objects.filter(test=self.object, student=student):
                if record.answer == record.question.solution:
                    avg_score += record.question.score
                    student_info['score'] = student_info['score'] + record.question.score
            student_scores.append(student_info)

        avg_score /= len(self.object.attend_students.all())
        print(self.object.subject.course_id)

        context['avg'] = avg_score
        context['total'] = test_score
        context['subject_id'] = self.object.subject.course_id
        context['students'] = student_scores
        return context


class TestStatisticsStudentRecord(generic.DetailView):
    model = Test
    template_name = 'online_test/test_statistics_student_record.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account

        student = Student.objects.get(student_id=self.kwargs['student_pk'])

        T_score = 0
        T_total_score = 0
        C_score = 0
        C_total_score = 0
        choice_question_records = []
        for record in ChoiceQuestionAnswerRecord.objects.filter(test=self.object, student=student):
            choice_question_records.append(record)
            C_total_score += record.question.score
            if record.answer == record.question.solution:
                C_score += record.question.score

        true_or_false_question_records = []
        for record in TrueOrFalseQuestionAnswerRecord.objects.filter(test=self.object, student=student):
            true_or_false_question_records.append(record)
            T_total_score += record.question.score
            if record.answer == record.question.solution:
                T_score += record.question.score
        context['test'] = self.object
        context['choice_question_answer_record'] = choice_question_records
        context['true_or_false_question_answer_record'] = true_or_false_question_records
        context['T_score'] = T_score
        context['T_total_score'] = T_total_score
        context['C_score'] = C_score
        context['C_total_score'] = C_total_score
        return context


class TestStatisticsTeacherRecord(generic.DetailView):
    model = Test
    template_name = 'online_test/test_statistics_teacher_record.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account

        student = Student.objects.get(student_id=self.kwargs['student_pk'])

        T_score = 0
        T_total_score = 0
        C_score = 0
        C_total_score = 0
        choice_question_records = []
        for record in ChoiceQuestionAnswerRecord.objects.filter(test=self.object, student=student):
            choice_question_records.append(record)
            C_total_score += record.question.score
            if record.answer == record.question.solution:
                C_score += record.question.score

        true_or_false_question_records = []
        for record in TrueOrFalseQuestionAnswerRecord.objects.filter(test=self.object, student=student):
            true_or_false_question_records.append(record)
            T_total_score += record.question.score
            if record.answer == record.question.solution:
                T_score += record.question.score
        context['test'] = self.object
        context['choice_question_answer_record'] = choice_question_records
        context['true_or_false_question_answer_record'] = true_or_false_question_records
        context['T_score'] = T_score
        context['T_total_score'] = T_total_score
        context['C_score'] = C_score
        context['C_total_score'] = C_total_score
        return context


class StudentStatistics(generic.ListView):
    model = Test
    template_name = 'online_test/student_statistics.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = Subject.objects.get(course_id=self.kwargs['subject'])

        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account
        login_student = Student.objects.get(student_id=account_id)

        object_list = Test.objects.filter(attend_students=login_student, subject=subject,
                                          end_time__lte=datetime.datetime.now())
        context['object_list'] = object_list
        context['student_id'] = login_student.student_id
        context['subject_id'] = subject.course_id

        return context


def submit_answer(request: HttpRequest):
    account_id = request.session['account_id']
    login_student = Student.objects.get(student_id=account_id)

    if request.method == 'POST':
        test_id = int(request.POST['test_id'])
        question_type = request.POST['type']

        if question_type == 'choice':
            for key, value in request.POST.items():
                print(key, value)
                if key != 'test_id' and key != 'type':
                    try:
                        record = ChoiceQuestionAnswerRecord.objects.get(test=Test.objects.get(id=test_id),
                                                                        student=login_student,
                                                                        question=ChoiceQuestion.objects.get(id=key))
                        record.answer = value
                        record.answer_time = timezone.now()
                        record.save()
                    except ChoiceQuestionAnswerRecord.DoesNotExist:
                        record = ChoiceQuestionAnswerRecord(
                            test=Test.objects.get(id=test_id),
                            question=ChoiceQuestion.objects.get(id=key),
                            student=None,
                            answer=value,
                            answer_time=timezone.now()
                        )
                        record.save()

        elif question_type == 'true_or_false':
            for key, value in request.POST.items():
                if key != 'test_id' and key != 'type':
                    print(key, value)
                    try:
                        record = TrueOrFalseQuestionAnswerRecord.objects.get(test=Test.objects.get(id=test_id),
                                                                             student=login_student,
                                                                             question=TrueOrFalseQuestion.objects.get(
                                                                                 id=key))

                        record.answer = (value == 'T')
                        record.answer_time = timezone.now()
                        record.save()
                    except TrueOrFalseQuestionAnswerRecord.DoesNotExist:
                        record = TrueOrFalseQuestionAnswerRecord(
                            test=Test.objects.get(id=test_id),
                            question=TrueOrFalseQuestion.objects.get(id=key),
                            student=None,
                            answer=(value == 'T'),
                            answer_time=timezone.now()
                        )
                        record.save()

    return HttpResponse(json.dumps({'success': True, 'result': 'ok'}))


class ProblemBank(generic.ListView):
    model = Test
    template_name = 'online_test/problem_bank.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account
        return context


class SingleProblem(generic.ListView):
    model = Test
    template_name = 'online_test/problem_single.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account
        return context



class SingleChoice(generic.ListView):
    model = Test
    template_name = 'online_test/problem_single_choice.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account

        T_score = 0
        T_total_score = 0
        C_score = 0
        C_total_score = 0
        choice_question_records = []
        true_or_false_question_records = []
        pk = int(self.kwargs['pk'])
        select = ChoiceQuestion.objects.filter(pk=int(pk))[0]

        context['problem'] = select

        return context


class SingleStaticChoice(generic.ListView):
    model = Test
    template_name = 'online_test/problem_single_static_choice.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account

        T_score = 0
        T_total_score = 0
        C_score = 0
        C_total_score = 0
        choice_question_records = []
        true_or_false_question_records = []
        pk = int(self.kwargs['pk'])
        select = ChoiceQuestion.objects.filter(pk=int(pk))[0]
        context['problem'] = select

        return context


class SingleJudge(generic.ListView):
    model = Test
    template_name = 'online_test/problem_single_judge.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account

        T_score = 0
        T_total_score = 0
        C_score = 0
        C_total_score = 0
        choice_question_records = []
        true_or_false_question_records = []
        pk = int(self.kwargs['pk'])
        print(pk)
        judge = TrueOrFalseQuestion.objects.filter(pk=pk)[0]
        context['problem'] = judge

        return context


class SingleStaticJudge(generic.ListView):
    model = Test
    template_name = 'online_test/problem_single_static_judge.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account

        T_score = 0
        T_total_score = 0
        C_score = 0
        C_total_score = 0
        choice_question_records = []
        true_or_false_question_records = []
        pk = int(self.kwargs['pk'])
        print(pk)
        judge = TrueOrFalseQuestion.objects.filter(pk=pk)[0]
        context['problem'] = judge

        return context


# class SingleStaticChoice(generic.ListView):
#     model = Test
#     template_name = 'online_test/problem_single_static_choice.html'
#
#
# class SingleStaticJudge(generic.ListView):
#     model = Test
#     template_name = 'online_test/problem_single_static_judge.html'


class ManualTestGeneration(generic.ListView):
    model = Test
    template_name = 'online_test/manual_test_generation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account

        return context


class AutoTestGeneration(generic.ListView):
    model = Test
    template_name = 'online_test/auto_test_generation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account

        return context


def test_add(request: HttpRequest):
    account_id = request.session['account_id']
    login_teacher = Teacher.objects.get(teacher_id=account_id)

    if request.method == "POST":
        select = []
        judge = []
        subject = Subject.objects.filter(name=request.POST.get("subject"))[0]
        start = request.POST.get("start_time")
        end = request.POST.get("end_time")
        year = int(start[0:4])
        month = int(start[5:7])
        day = int(start[8:])
        start_date = datetime.datetime(
            year=year,
            month=month,
            day=day
        )
        year = int(end[0:4])
        month = int(end[5:7])
        day = int(end[8:])
        end_date = datetime.datetime(
            year=year,
            month=month,
            day=day
        )
        # 查出改科目对应的考试时间
        test = Test(
            name=request.POST.get("name"),
            subject=subject,
            creator=login_teacher,
            start_time=start_date,
            end_time=end_date
        )

        test.save()
        for every in Student.objects.all():
            test.attend_students.add(every)
            for key, value in request.POST.items():
                if "question" in key and "pk" in key:
                    index = key[8:12]
                    ty = "question" + index + "[type]"
                    id_pk = "question" + index + "[pk]"
                    if request.POST.get(ty) == '1':
                        # print(id_pk)
                        quec = ChoiceQuestion.objects.filter(id=int(request.POST.get(id_pk)))[0]
                        test.choice_questions.add(quec)
                        record = ChoiceQuestionAnswerRecord(
                            test=test,
                            student=every,
                            question=quec
                        )
                        record.save()
                    else:
                        print(int(request.POST.get(id_pk)))
                        quej = TrueOrFalseQuestion.objects.filter(id=int(request.POST.get(id_pk)))[0]
                        print(quej)
                        print("hello222")
                        test.true_or_false_questions.add(quej)
                        print(test)
                        print(every)
                        record2 = TrueOrFalseQuestionAnswerRecord(
                            test=test,
                            student=every,
                            question=quej
                        )
                        print("hello222")
                        record2.save()

                    print("hello333")
        print("hi44")
        for key, value in request.POST.items():
            if "question" in key and "pk" in key:
                index = key[8:12]
                ty = "question" + index + "[type]"
                id_pk = "question" + index + "[pk]"

                if request.POST.get(ty) == '1':
                    que = ChoiceQuestion.objects.filter(id=int(request.POST.get(id_pk)))[0]
                    test.choice_questions.add(que)
                else:
                    que = TrueOrFalseQuestion.objects.filter(id=int(request.POST.get(id_pk)))[0]
                    test.true_or_false_questions.add(que)
        test.save()
    return HttpResponse(json.dumps({'success': True, 'result': 'ok'}), content_type="application/json")


def test_mod(request: HttpRequest, pk):
    account_id = request.session['account_id']
    login_teacher = Teacher.objects.get(teacher_id=account_id)

    get = Test.objects.filter(id=pk)[0]
    if request.method == "POST":
        select = []
        judge = []
        subject = Subject.objects.filter(name=request.POST.get("subject"))[0]
        select = ChoiceQuestion.objects.filter(subject=subject)
        judge = TrueOrFalseQuestion.objects.filter(subject=subject)
        # 查出改科目对应的考试时间
        get.name = request.POST.get("name")
        get.subject = subject
        get.creator = login_teacher
        get.attend_students = []

        for every in select:
            get.choice_questions.add(every)
        for every in judge:
            get.true_or_false_questions.add(every)
        get.save()
    return HttpResponse(json.dumps({'success': True, 'result': 'ok'}), content_type="application/json")


def test_del(request: HttpRequest, pk):
    get = Test.objects.filter(id=pk)[0]
    get.delete()
    return HttpResponse(json.dumps({'success': True, 'result': 'ok'}), content_type="application/json")


def test_gerner(request: HttpRequest):
    account_id = request.session['account_id']
    login_teacher = Teacher.objects.get(teacher_id=account_id)

    if request.method == "POST":
        select = []
        judge = []
        subject = Subject.objects.filter(name=request.POST.get("subject"))[0]
        select = ChoiceQuestion.objects.filter(subject=subject)
        judge = TrueOrFalseQuestion.objects.filter(subject=subject)
        start = request.POST.get("start_time")
        end = request.POST.get("end_time")
        year = int(start[0:4])
        month = int(start[5:7])
        day = int(start[8:])
        start_date = datetime.datetime(
            year=year,
            month=month,
            day=day
        )
        year = int(end[0:4])
        month = int(end[5:7])
        day = int(end[8:])
        end_date = datetime.datetime(
            year=year,
            month=month,
            day=day
        )
        # start_d = datetime.datetime(
        #    datetime=start_date
        # )
        # end_d = datetime.datetime(
        #    datetime=end_date
        # )
        # 查出改科目对应的考试时间
        test = Test(
            name=request.POST.get("name"),
            subject=subject,
            creator=login_teacher,
            start_time=start_date,
            end_time=end_date
        )

        test.save()
        for every in Student.objects.all():
            test.attend_students.add(every)
            for quec in select:
                test.choice_questions.add(quec)
                record = ChoiceQuestionAnswerRecord(
                    test=test,
                    student=every,
                    question=quec
                )
                record.save()
            for quej in judge:
                test.true_or_false_questions.add(quej)
                record2 = TrueOrFalseQuestionAnswerRecord(
                    test=test,
                    student=every,
                    question=quej
                )
                record2.save()

            print("hello333")

        # info = request.POST.get("questions")
        # info_data = json.loads(info)
        # for key in info_data:
        #     if info_data[key]["type"] == 1:
        #         select += choice_re(info_data[key])
        #     else:
        #         judge += judge_re(info_data[key])

        for every in select:
            test.choice_questions.add(every)
        for every in judge:
            test.true_or_false_questions.add(every)

        test.save()

    return HttpResponse(json.dumps({'success': True, 'result': 'ok'}), content_type="application/json")


def test_json(test):
    infos_choice = []
    count = -1
    for reever in test:
        count = count + 1
        info = {"name": reever.name, "choice_questions": choice_json(reever.choice_questions),
                "true_or_false_questions": judge_json(reever.true_or_false_questions),
                "creator": reever.creator.name,
                "subject": reever.subject.name, "pk": reever.id}
        infos_choice.append({count: info})
    return infos_choice


def test_search(request: HttpRequest):
    if request.method == "POST":
        infos = {}
        test = Test.objects.all()  # filter(name=request.POST.get("name"),
        #      creator=request.POST.get("creator"), subject=request.POST.get("subject"))
        infos = test_json(test)
        return HttpResponse(json.dumps({'infos': infos}), content_type="application/json")


def subject(request: HttpRequest):
    account_id = request.session['account_id']
    login_teacher = Teacher.objects.get(teacher_id=account_id)

    teach_id = login_teacher.teacher_id.account_id
    course_id = Teach.objects.filter(teacher_id=teach_id)
    course = []
    count = -1
    for every in course_id:
        count += 1
        course.append({count: every.course_id.name})
    return HttpResponse(json.dumps({'subject': course}), content_type="application/json")


def chapter(request: HttpRequest):
    account_id = request.session['account_id']
    login_teacher = Teacher.objects.get(teacher_id=account_id)

    teach_id = login_teacher.teacher_id.account_id
    course_id = Teach.objects.filter(teacher_id=teach_id)
    total = []
    count = -1
    for every in course_id:
        count += 1
        print(every.course_id.name)

        chapter = Chapter.objects.filter(subject=every.course_id)
        print(100002)
        print(chapter)

        tem = []
        s = -1
        print(type(chapter))
        for e in chapter:
            print(100000)
            s += 1
            print(e)
            tem.append({s: e.chapter})
        print(2222)
        total.append({every.course_id.name: tem})
    print(3333)
    return HttpResponse(json.dumps({'chapter': total}), content_type="application/json")


def knowledge_point(request: HttpRequest):
    account_id = request.session['account_id']
    login_teacher = Teacher.objects.get(teacher_id=account_id)

    teach_id = login_teacher.teacher_id.account_id
    course_id = Teach.objects.filter(teacher_id=teach_id)
    total = []
    count = -1
    for every in course_id:
        count += 1
        knowledge_point = KnowledgePoint.objects.filter(subject=every.course_id)
        tem = []
        s = -1
        for e in knowledge_point:
            s += 1
            tem.append({s: e.knowledge_point})
        total.append({every.course_id.name: tem})
    return HttpResponse(json.dumps({'knowledge_point': total}), content_type="application/json")


class ProblemDetail(generic.DetailView):
    template_name = 'online_test/problem_single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.request.session['account_id']
        account = Account.objects.get(account_id=account_id)
        context['account'] = account

        T_score = 0
        T_total_score = 0
        C_score = 0
        C_total_score = 0
        choice_question_records = []
        true_or_false_question_records = []
        if self.kwargs['pk'] == "1":
            pk = ChoiceQuestion.objects.get(id=self.kwargs['pk'])
            select = ChoiceQuestion.objects.filter(pk=pk)[0]
            context['choice_question'] = select
        else:
            pk = TrueOrFalseQuestion.objects.get(id=self.kwargs['pk'])
            judge = TrueOrFalseQuestion.objects.filter(pk=pk)[0]
            context['true_or_false_question'] = judge

        return context


def problem_search(request: HttpRequest):
    account_id = request.session['account_id']
    login_teacher = Teacher.objects.get(teacher_id=account_id)

    if request.method == "POST":
        print('post')
        print(request.POST.get("type"))
        infos = {}
        subject = Subject.objects.filter(name=request.POST.get("subject"))[0]
        chapter = Chapter.objects.filter(chapter=request.POST.get("chapter"))[0]
        knowledge_point = KnowledgePoint.objects.filter(knowledge_point=request.POST.get("knowledge_point"))[0]
        if request.POST.get("type") == "1":
            result = ChoiceQuestion.objects.filter(creator=login_teacher, subject=subject,
                                                   chapter=chapter, knowledge_point=knowledge_point)
            print(result.all())
            infos = choice_json(result)
            # print('end: '+infos)
        elif request.POST.get("type") == "0":
            result = TrueOrFalseQuestion.objects.filter(creator=login_teacher, subject=subject,
                                                        chapter=chapter, knowledge_point=knowledge_point)
            infos = judge_json(result)
            print(result.count())
        else:

            result = ChoiceQuestion.objects.filter(creator=login_teacher, subject=subject,
                                                   chapter=chapter, knowledge_point=knowledge_point)
            choice_j = choice_json(result)

            result = TrueOrFalseQuestion.objects.filter(creator=login_teacher, subject=subject,
                                                        chapter=chapter, knowledge_point=knowledge_point)
            select_j = judge_json(result)
            infos = {'choice': choice_j, 'judge': select_j}
        return HttpResponse(json.dumps({'infos': infos}), content_type="application/json")


def problem_add(request: HttpRequest):
    account_id = request.session['account_id']
    login_teacher = Teacher.objects.get(teacher_id=account_id)

    if request.method == "POST":
        subject = Subject.objects.filter(name=request.POST.get("subject"))[0]
        chapter = Chapter.objects.filter(chapter=request.POST.get("chapter"))[0]
        knowledge_point = KnowledgePoint.objects.filter(knowledge_point=request.POST.get("knowledge_point"))[0]

        if request.POST.get("type") == "1":
            result = ChoiceQuestion(
                content=request.POST.get("content"),
                choice_a=request.POST.get("choice_a"),
                choice_b=request.POST.get("choice_b"),
                choice_c=request.POST.get("choice_c"),
                choice_d=request.POST.get("choice_d"),
                solution=request.POST.get("solution"),
                score=request.POST.get("score"),
                creator=login_teacher,
                subject=subject,
                chapter=chapter,
                knowledge_point=knowledge_point,
                add_time=timezone.now(),
                latest_modify_time=timezone.now()
            )
            # print(result)
            result.save()
        elif request.POST.get("type") == "0":
            if request.POST.get("solution") == 'true':
                solution = True
            else:
                solution = False
            result = TrueOrFalseQuestion(
                content=request.POST.get("content"),
                solution=solution,
                score=request.POST.get("score"),
                creator=login_teacher,
                subject=subject,
                chapter=chapter,
                knowledge_point=knowledge_point,
                add_time=timezone.now(),
                latest_modify_time=timezone.now()
            )
            # print(result)
            result.save()
        # choice = ChoiceQuestion.objects.filter(creator=login_teacher)
        # infos_choice = choice_json(choice)
        # judge = TrueOrFalseQuestion.objects.filter(creator=login_teacher)
        # infos_judge = judge_json(judge)
        return HttpResponse(json.dumps({'success': True, 'result': 'ok'}), content_type="application/json")
        # HttpResponse(json.dumps({'choice': infos_choice, 'judge': infos_judge}))
        # #render(request, 'online_test/problem_bank.html', {'choice': infos_choice, 'judge': infos_judge})


def choice_json(choice):
    infos_choice = []
    count = -1
    for reever in choice:
        print("1111")
        count = count + 1
        info = {"content": reever.content, "choice_a": reever.choice_a,
                "choice_b": reever.choice_b, "choice_c": reever.choice_c, "choice_d": reever.choice_d,
                "solution": reever.solution, "score": reever.score, "creator": reever.creator.name,
                "subject": reever.subject.name,
                "chapter": reever.chapter.chapter, "knowledge_point": reever.knowledge_point.knowledge_point,

                "pk": reever.id}
        infos_choice.append({count: info})
    return infos_choice


def judge_json(judge):
    infos_judge = []
    count = -1
    for reever in judge:
        count = count + 1
        info = {"content": reever.content,
                "solution": reever.solution, "score": reever.score, "creator": reever.creator.name,
                "subject": reever.subject.name,
                "chapter": reever.chapter.chapter, "knowledge_point": reever.knowledge_point.knowledge_point,
                "pk": reever.id}
        infos_judge.append({count: info})

    return infos_judge


def problem_mod(request: HttpRequest, pk):
    # try:
    if request.method == "POST":
        if request.POST.get("type") == "1":
            flag = 1
            get = ChoiceQuestion.objects.filter(id=pk)[0]
            get.content = request.POST.get("content")
            get.choice_a = request.POST.get("choice_a")
            get.choice_b = request.POST.get("choice_b")
            get.choice_c = request.POST.get("choice_c")
            get.choice_d = request.POST.get("choice_d")
            get.solution = request.POST.get("solution")
            subject = Subject.objects.filter(name=request.POST.get("subject"))[0]
            get.subject = subject
            chapter = Chapter.objects.filter(chapter=request.POST.get("chapter"))[0]
            get.chapter = chapter
            get.score = request.POST.get("score")
            knowledge_point = KnowledgePoint.objects.filter(knowledge_point=request.POST.get("knowledge_point"))[0]
            get.knowledge_point = knowledge_point
            get.save()
        # except BaseException:
        elif request.POST.get("type") == "0":
            flag = 0
            get = TrueOrFalseQuestion.objects.filter(id=pk)[0]
            get.content = request.POST.get("content")
            get.solution = request.POST.get("solution")
            print(request.POST.get("subject"))
            subject = Subject.objects.filter(name=request.POST.get("subject"))[0]
            get.subject = subject
            print("111")
            chapter = Chapter.objects.filter(chapter=request.POST.get("chapter"))[0]
            get.chapter = chapter
            print("222")
            get.score = request.POST.get("score")
            knowledge_point = KnowledgePoint.objects.filter(knowledge_point=request.POST.get("knowledge_point"))[0]
            get.knowledge_point = knowledge_point
            print("333")
            get.save()
        # choice = ChoiceQuestion.objects.filter(creator=login_teacher)
        # infos_choice = choice_json(choice)
        # judge = TrueOrFalseQuestion.objects.filter(creator=login_teacher)
        # infos_judge = judge_json(judge)
        return HttpResponse(json.dumps({'success': True, 'result': 'ok'}), content_type="application/json")
        # HttpResponse(json.dumps({'choice': infos_choice, 'judge': infos_judge}))
        # #render(request, 'online_test/problem_bank.html', {'choice': infos_choice, 'judge':)


def problem_del(request: HttpRequest, pk):
    type = request.POST.get("type")
    print(type)
    if type == "1":
        get = ChoiceQuestion.objects.filter(id=pk)[0]
    else:
        get = TrueOrFalseQuestion.objects.filter(id=pk)[0]

    get.delete()
    # try:
    #     flag = "1"
    #     get = get_object_or_404(ChoiceQuestion, pk=pk)
    # except BaseException:
    #     flag = "0"
    #     get = get_object_or_404(TrueOrFalseQuestion, pk=pk)
    # get.delete()
    # choice = ChoiceQuestion.objects.filter(creator=login_teacher)
    # infos_choice = choice_json(choice)
    # judge = TrueOrFalseQuestion.objects.filter(creator=login_teacher)
    # infos_judge = judge_json(judge)
    return HttpResponse(json.dumps({'success': True, 'result': 'ok'}), content_type="application/json")
    # HttpResponse(json.dumps({'choice': infos_choice, 'judge': infos_judge}))
    # #render(request, 'online_test/problem_bank.html', {'choice': infos_choice, 'judge': infos_judge})
