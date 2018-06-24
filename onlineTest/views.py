from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.views import generic
import json
from .models import Test, ChoiceQuestionAnswerRecord, ChoiceQuestion, TrueOrFalseQuestionAnswerRecord, \
    TrueOrFalseQuestion, Student, Teacher, Chapter, KnowledgePoint

login_student = Student.objects.all()[0]
login_teacher = Teacher.objects.all()[0]


class IndexView(generic.ListView):
    model = Test
    template_name = 'online_test/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = Test.objects.filter(attend_students=login_student)
        context['object_list'] = object_list
        return context


class TestDetail(generic.DetailView):
    model = Test
    template_name = 'online_test/test_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['choice_question_answer_record'] = {}
        for record in ChoiceQuestionAnswerRecord.objects.filter(test=self.object):
            context['choice_question_answer_record'][record.id] = record.answer

        context['true_or_false_question_answer_record'] = {}
        for record in TrueOrFalseQuestionAnswerRecord.objects.filter(test=self.object):
            context['true_or_false_question_answer_record'][record.id] = 'T' if record.answer else 'F'

        return context

class ProblemBank(generic.ListView):
    model = Test
    template_name = 'online_test/problem_bank.html'


class SingleProblem(generic.ListView):
    model = Test
    template_name = 'online_test/problem_single.html'

class ManualTestGeneration(generic.ListView):
    model = Test
    template_name = 'online_test/manual_test_generation.html'

class AutoTestGeneration(generic.ListView):
    model = Test
    template_name = 'online_test/auto_test_generation.html'

class TeacherStatisticsTests(generic.ListView):
    model = Test
    template_name = 'online_test/teacher_statistics_tests.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = Test.objects.filter(creator=login_teacher)
        context['object_list'] = object_list
        return context


class TeacherStatisticsChapters(generic.ListView):
    model = Chapter
    template_name = 'online_test/teacher_statistics_chapters.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = {}
        for test in Test.objects.filter(creator=login_teacher):
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
        return context


class TeacherStatisticsKnowledgePoints(generic.ListView):
    model = KnowledgePoint
    template_name = 'online_test/teacher_statistics_knowledge_points.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = {}
        for test in Test.objects.filter(creator=login_teacher):
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
        return context


class TestStatistics(generic.DetailView):
    model = Test
    template_name = 'online_test/test_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test_score = 0

        assert isinstance(self.object, Test)

        for question in self.object.choice_questions.all():
            test_score += question.score

        for question in self.object.true_or_false_questions.all():
            test_score += question.score

        avg_score = 0
        student_scores = []
        for student in self.object.attend_students.all():
            student_info = {'id': student.id, 'name': student.name, 'score': 0}
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

        context['avg'] = avg_score
        context['total'] = test_score

        context['students'] = student_scores
        return context


class TestStatisticsStudentRecord(generic.DetailView):
    model = Test
    template_name = 'online_test/test_statistics_student_record.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student = Student.objects.get(id=self.kwargs['student_pk'])

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

        student = Student.objects.get(id=self.kwargs['student_pk'])

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
        object_list = Test.objects.filter(attend_students=login_student)
        context['object_list'] = object_list
        context['student_id'] = login_student.id

        return context


def submit_answer(request: HttpRequest):
    if request.method == 'POST':
        test_id = int(request.POST['test_id'])
        question_type = request.POST['type']

        if question_type == 'choice':
            for key, value in request.POST.items():
                print(key, value)
                if key != 'test_id' and key != 'type':
                    try:
                        record = ChoiceQuestionAnswerRecord.objects.get(test=test_id)
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
                        record = TrueOrFalseQuestionAnswerRecord.objects.get(test=test_id)
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

def choice_re(data):
    choice = ChoiceQuestion(
        content=data["content"],
        choice_a=data["choice_a"],
        choice_b=data["choice_b"],
        choice_c=data["choice_c"],
        choice_d=data["choice_d"],
        solution=data["solution"],
        score=data["score"],
        creator=login_teacher,
        subject=data["subject"],
        chapter=data["chapter"],
        knowledge_point=data["knowledge_point"],
        add_time=timezone.now(),
        latest_modify_time=timezone.now()
    )
    return choice

def judge_re(data):
    judge = TrueOrFalseQuestion(
        content=data["content"],
        solution=data["solution"],
        score=data["score"],
        creator=login_teacher,
        subject=data["subject"],
        chapter=data["chapter"],
        knowledge_point=data["knowledge_point"],
        add_time=timezone.now(),
        latest_modify_time=timezone.now()
    )
    return judge

def  test_add(request: HttpRequest):
    if request.method == "POST":
        select = []
        judge = []
        #����Ŀ�Ŀ��Ӧ�Ŀ���ʱ��
        test = Test(
            name=request.POST.get("name"),
            subject=request.POST.get("subject"),
            creator=login_teacher,
            attend_students=[]
        )
        info = request.POST.get("questions")
        info_data = json.loads(info)
        for key in info_data:
            if info_data[key]["type"] == 1:
                select += choice_re(info_data[key])
            else:
                judge += judge_re(info_data[key])
        test.choice_questions = select
        test.true_or_false_questions = judge
        test.save()
    return HttpResponse(json.dumps({'success': True, 'result': 'ok'}), content_type="application/json")

def  test_mod(request: HttpRequest, pk):
    get = get_object_or_404(Test, pk=pk)
    if request.method == "POST":
        select = []
        judge = []
        #����Ŀ�Ŀ��Ӧ�Ŀ���ʱ��
        get.name=request.POST.get("name")
        get.subject=request.POST.get("subject")
        get.creator=login_teacher
        get.attend_students=[]
        info = request.POST.get("questions")
        info_data = json.loads(info)
        for key in info_data:
            if info_data[key]["type"] == 1:
                select += choice_re(info_data[key])
            else:
                judge += judge_re(info_data[key])
        get.choice_questions = select
        get.true_or_false_questions = judge
        get.save()
    return HttpResponse(json.dumps({'success': True, 'result': 'ok'}), content_type="application/json")

def test_del(request: HttpRequest, pk):
    get = get_object_or_404(Test, pk=pk)
    get.delete()
    return HttpResponse(json.dumps({'success': True, 'result': 'ok'}), content_type="application/json")

def test_json(test):
    infos_choice = {}
    count = -1
    for reever in test:
        count = count + 1
        info = {"name": reever.name, "choice_questions": choice_json(reever.choice_questions),
                "true_or_false_questions": judge_json(reever.true_or_false_questions),
                "creator": reever.creator,
                "subject": reever.subject, "start_time": reever.start_time,
                "end_time": reever.end_time, "pk": reever.pk}
        infos_choice[count + ""] = info
    return infos_choice

def test_search(request: HttpRequest):
    if request.method == "POST":
        infos = {}
        test = Test.objects.filter(name=request.POST.get("name"),
                                   creator=request.POST.get("creator"), subject=request.POST.get("subject"))
        infos = test_json(test)
        return HttpResponse(json.dumps({'infos': infos}), content_type="application/json")

def problem_detail(request: HttpRequest):
    if request.method == "POST":
        infos = {}
        if request.POST.get("type") == 1:
            result = ChoiceQuestion.objects.filter(creator=request.POST.get("creator"), subject=request.POST.get("subject"),
                                                   chapter=request.POST.get("chapter"), knowledge_point=request.POST.get("knowledge_point"))
            infos = choice_json(result)
        elif request.POST.get("type") == 0:
            result = TrueOrFalseQuestion.objects.filter(creator=request.POST.get("creator"), subject=request.POST.get("subject"),
                                                   chapter=request.POST.get("chapter"), knowledge_point=request.POST.get("knowledge_point"))
            infos = judge_json(result)
        return render(request, 'online_test/problem_single.html', {'infos': infos})

def problem_search(request: HttpRequest):
    print('get')
    if request.method == "POST":
        print('post')
        infos = {}
        if request.POST.get("type") == 1:
            result = ChoiceQuestion.objects.filter(creator=request.POST.get("creator"), subject=request.POST.get("subject"),
                                                   chapter=request.POST.get("chapter"), knowledge_point=request.POST.get("knowledge_point"))
            infos = choice_json(result)
        elif request.POST.get("type") == 0:
            result = TrueOrFalseQuestion.objects.filter(creator=request.POST.get("creator"), subject=request.POST.get("subject"),
                                                   chapter=request.POST.get("chapter"), knowledge_point=request.POST.get("knowledge_point"))
            infos = judge_json(result)
        return HttpResponse(json.dumps({'infos': infos}), content_type="application/json")

def problem_add(request: HttpRequest):
    if request.method == "POST":
        if request.POST.get("type") == 1:
            result = ChoiceQuestion(
                content = request.POST.get("content"),
                choice_a = request.POST.get("choice_a"),
                choice_b=request.POST.get("choice_b"),
                choice_c=request.POST.get("choice_c"),
                choice_d=request.POST.get("choice_d"),
                solution=request.POST.get("solution"),
                score = request.POST.get("score"),
                creator=login_teacher,
                subject=request.POST.get("subject"),
                chapter=request.POST.get("chapter"),
                knowledge_point=request.POST.get("knowledge_point"),
                add_time=timezone.now(),
                latest_modify_time=timezone.now()
            )
            result.save()
        elif request.POST.get("type") == 0:
            result = TrueOrFalseQuestion(
                content=request.POST.get("content"),
                solution=request.POST.get("solution"),
                score=request.POST.get("score"),
                creator=login_teacher,
                subject=request.POST.get("subject"),
                chapter=request.POST.get("chapter"),
                knowledge_point=request.POST.get("knowledge_point"),
                add_time=timezone.now(),
                latest_modify_time=timezone.now()
            )
            result.save()
        #choice = ChoiceQuestion.objects.filter(creator=login_teacher)
        #infos_choice = choice_json(choice)
        #judge = TrueOrFalseQuestion.objects.filter(creator=login_teacher)
        #infos_judge = judge_json(judge)
        return HttpResponse(json.dumps({'success': True, 'result': 'ok'}), content_type="application/json")
        #HttpResponse(json.dumps({'choice': infos_choice, 'judge': infos_judge}))
        # #render(request, 'online_test/problem_bank.html', {'choice': infos_choice, 'judge': infos_judge})
    return render(request, 'online_test/problem_single.html')

def choice_json(choice):
    infos_choice = {}
    count = -1
    for reever in choice:
        count = count + 1
        info = {"content": reever.content, "choice_a": reever.choice_a,
                "choice_b": reever.choice_b, "choice_c": reever.choice_c, "choice_d": reever.choice_d,
                "solution": reever.solution, "score": reever.score, "creator": reever.creator,
                "subject": reever.subject, "chapter": reever.chapter, "knowledge_point": reever.knowledge_point,
                "add_time": reever.add_time, "last_modify_time": reever.latest_modify_time, "pk": reever.pk}
        infos_choice[count + ""] = info
    return infos_choice

def judge_json(judge):
    infos_judge = {}
    count = -1
    for reever in judge:
        count = count + 1
        info = {"content": reever.content,
                "solution": reever.solution, "score": reever.score, "creator": reever.creator,
                "subject": reever.subject, "chapter": reever.chapter, "knowledge_point": reever.knowledge_point,
                "add_time": reever.add_time, "last_modify_time": reever.latest_modify_time, "pk": reever.pk}
        infos_judge[count + ""] = info
    return infos_judge

def problem_mod(request: HttpRequest, pk):
    # try:
    if request.POST.get("type") == 1:
        flag = 1
        get = get_object_or_404(ChoiceQuestion, pk=pk)
    # except BaseException:
    elif request.POST.get("type") == 0:
        flag = 0
        get = get_object_or_404(TrueOrFalseQuestion, pk=pk)
    if request.method == "POST":
        if flag == 1:
            result = ChoiceQuestion(
                content=get.content,
                choice_a=get.choice_a,
                choice_b=get.choice_b,
                choice_c=get.choice_c,
                choice_d=get.choice_d,
                solution=get.solution,
                score=get.score,
                creator=login_teacher,
                subject=get.subject,
                chapter=get.chapter,
                knowledge_point=get.knowledge_point,
                add_time=timezone.now(),
                latest_modify_time=timezone.now()
            )
            result.save()
        elif flag == 0:
            result = TrueOrFalseQuestion(
                content=get.content,
                solution=get.solution,
                score=get.score,
                creator=login_teacher,
                subject=get.subject,
                chapter=get.chapter,
                knowledge_point=get.knowledge_point,
                add_time=timezone.now(),
                latest_modify_time=timezone.now()
            )
            result.save()
        #choice = ChoiceQuestion.objects.filter(creator=login_teacher)
        #infos_choice = choice_json(choice)
        #judge = TrueOrFalseQuestion.objects.filter(creator=login_teacher)
        #infos_judge = judge_json(judge)
        return HttpResponse(json.dumps({'success': True, 'result': 'ok'}), content_type="application/json")
        #HttpResponse(json.dumps({'choice': infos_choice, 'judge': infos_judge}))
        # #render(request, 'online_test/problem_bank.html', {'choice': infos_choice, 'judge':)
    return render(request, 'online_test/problem_single.html', {"content": get, "type": flag})

def problem_del(request: HttpRequest, pk):
    try:
        flag = 1
        get = get_object_or_404(ChoiceQuestion, pk=pk)
    except BaseException:
        flag = 0
        get = get_object_or_404(TrueOrFalseQuestion, pk=pk)
    get.delete()
    #choice = ChoiceQuestion.objects.filter(creator=login_teacher)
    #infos_choice = choice_json(choice)
    #judge = TrueOrFalseQuestion.objects.filter(creator=login_teacher)
    #infos_judge = judge_json(judge)
    return HttpResponse(json.dumps({'success': True, 'result': 'ok'}), content_type="application/json")
    #HttpResponse(json.dumps({'choice': infos_choice, 'judge': infos_judge}))
    # #render(request, 'online_test/problem_bank.html', {'choice': infos_choice, 'judge': infos_judge})
