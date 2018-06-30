from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import datetime

from basicInfo.models import course, room, takeup, time, teach, teacher


def api_course_post(request):
    course_id = request.POST.get('course_id')
    teacher_id = request.POST.get('teacher_id')
    room_id = request.POST.get('room_id')
    time_id = eval(request.POST.get('time_id'))
    duplicate = request.POST.get('duplicate')

    if course_id is None:
        return JsonResponse({'success': False, 'reason': '`course_id` is required'})
    elif teacher_id is None:
        return JsonResponse({'success': False, 'reason': '`teacher_id` is required'})
    elif room_id is None:
        return JsonResponse({'success': False, 'reason': '`room_id` is required'})
    elif time_id is None:
        return JsonResponse({'success': False, 'reason': '`time_id` is required'})
    elif duplicate is None:
        return JsonResponse({'success': False, 'reason': '`duplicate` is required'})

    try:
        room_id = int(room_id)
    except ValueError:
        return JsonResponse({'success': False, 'reason': '`room_id` is not an integer'})
    try:
        for i in range(len(time_id)):
            time_id[i] = int(time_id[i])
    except ValueError:
        return JsonResponse({'success': False, 'reason': '`time_id[index]` is not an integer'})
    try:
        duplicate = int(duplicate)
    except ValueError:
        return JsonResponse({'success': False, 'reason': '`duplicate` is not an integer'})

    teach_filter = teach.objects.filter(teacher_id=teacher_id, course_id=course_id, duplicate=duplicate)
    reStr = ''
    try:
        if len(teach_filter) == 0:
            teach_filter = teach.objects.all()
            max_teach_id = 0
            for i in teach_filter:
                max_teach_id = max(max_teach_id, i.teach_id)
            max_teach_id += 1
            teach.objects.create(
                teach_id=max_teach_id,
                duplicate=duplicate,
                teacher_id=teacher.objects.get(teacher_id=teacher_id),
                course_id=course.objects.get(course_id=course_id),
                capacity=0
            )
            reStr += 'OK teach created '
        else:
            reStr += 'OK teach already exist '
        teach_filter = teach.objects.filter(teacher_id=teacher_id, course_id=course_id, duplicate=duplicate)
        teach_id = 0
        for i in teach_filter:
            teach_id = i.teach_id
        for i in range(len(time_id)):
            takeup_filter = takeup.objects.filter(teach_id=teach_id, teacher_id=teacher_id, room_id=room_id,
                                                  time_id=time_id[i])
            if len(takeup_filter) == 0:
                takeup.objects.create(
                    teach_id=teach.objects.get(teach_id=teach_id),
                    teacher_id=teacher.objects.get(teacher_id=teacher_id),
                    room_id=room.objects.get(room_id=room_id),
                    time_id=time.objects.get(time_id=time_id[i])
                )
                reStr += 'OK takeup created'
            else:
                reStr += 'OK takeup already exist'
        return JsonResponse({'success': True, 'reason': reStr})
    except ValueError:
        return JsonResponse({'success': False, 'reason': 'ValueError'})


def get_period(time_id):
    if (time_id < 1 or time_id > 91):
        return [0,0]
    return [(time_id-1)//13+1,(time_id-1)%13+1]


def api_course_get(request):
    course_id = request.GET.get('course_id')
    teacher_id = request.GET.get('teacher_id')
    room_id = request.GET.get('room_id')
    time_id = request.GET.get('time_id')
    count = request.GET.get('count')
    takeup_filter = takeup.objects.all()
    if course_id is not None:
        try:
            teach_filter = teach.objects.filter(course_id=course_id)
            find_course = [i.teach_id for i in teach_filter]
            takeup_filter = takeup_filter.filter(teach_id__in=find_course)
        except ValueError:
            return HttpResponseBadRequest()
    if teacher_id is not None:
        try:
            takeup_filter = takeup_filter.filter(teacher_id=teacher_id)
        except ValueError:
            return HttpResponseBadRequest()
    elif room_id is not None:
        try:
            room_id = int(room_id)
            takeup_filter = takeup_filter.filter(room_id=room_id)
        except ValueError:
            return HttpResponseBadRequest()
    elif time_id is not None:
        try:
            time_id = int(time_id)
            takeup_filter = takeup_filter.filter(time_id=time_id)
        except ValueError:
            return HttpResponseBadRequest()
    if count is None:
        count = 0xffff
    else:
        try:
            count = int(count)
            takeup_filter = takeup_filter[:count]
        except ValueError:
            return JsonResponse({'success': False, 'reason': '`count` is not an integer'})

    #take_up_ins = takeup(teach_id = ins_teach_id,time_id = ins_time_id,room_id = ins_room_id,teacher_id = ins_teacher_id)
    takeup_filter = takeup_filter.order_by('teach_id','room_id','time_id')
    res = []
    takeup_len = len(takeup_filter)
    i = 0
    while(i < takeup_len):
        r = takeup_filter[i]
        ret_dict = {
            'course_id': teach.objects.get(teach_id=r.teach_id.teach_id).course_id.course_id,
            'course_name': teach.objects.get(teach_id=r.teach_id.teach_id).course_id.name,
            'teacher_id': r.teacher_id.teacher_id_id,
            'teacher_name': teacher.objects.get(teacher_id=r.teacher_id.teacher_id_id).name,
            'room_id': r.room_id.room_id,
            'room_name': room.objects.get(room_id=r.room_id.room_id).location,
            'duplicate': teach.objects.get(teach_id=r.teach_id.teach_id).duplicate,
            'capacity': teach.objects.get(teach_id=r.teach_id.teach_id).capacity,
        }
        period = {}
        for day in range(1,8):
            period[day] = []
        j = i
        while(j < takeup_len and takeup_filter[i].teach_id == takeup_filter[j].teach_id and takeup_filter[i].room_id == takeup_filter[j].room_id):
            if takeup_filter[j].time_id.day == 0:
                continue
            [day,classnum] = get_period(takeup_filter[j].time_id.time_id)
            period[day].append(classnum)
            j += 1

        i = j
        
        ret_dict['period'] = period
        res.append(ret_dict)
    '''
    res = [{
        'course_id': teach.objects.get(teach_id=r.teach_id.teach_id).course_id.course_id,
        'course_name': teach.objects.get(teach_id=r.teach_id.teach_id).course_id.name,
        'teacher_id': r.teacher_id.teacher_id_id,
        'teacher_name': teacher.objects.get(teacher_id=r.teacher_id.teacher_id_id).name,
        'room_id': r.room_id.room_id,
        'room_name': room.objects.get(room_id=r.room_id.room_id).location,
        'time_id': r.time_id.time_id,
        'time_start': time.objects.get(time_id=r.time_id.time_id).start,
        'time_end': time.objects.get(time_id=r.time_id.time_id).end,
        'time_day': time.objects.get(time_id=r.time_id.time_id).day,
        'duplicate': teach.objects.get(teach_id=r.teach_id.teach_id).duplicate,
        'capacity': teach.objects.get(teach_id=r.teach_id.teach_id).capacity,
        #'exam_date': teach.objects.get(teach_id=r.teach_id.teach_id).exam_date
    } for r in takeup_filter]
    '''
    return JsonResponse(res, safe=False)


@csrf_exempt
def api_course_get_pagecount(request):
    if request.method != 'GET':
        return HttpResponseNotFound()
    course_id = request.GET.get('course_id')
    teacher_id = request.GET.get('teacher_id')
    room_id = request.GET.get('room_id')
    time_id = request.GET.get('time_id')
    count = request.GET.get('count')
    takeup_filter = takeup.objects.all()
    if course_id is not None:
        try:
            teach_filter = teach.objects.filter(course_id=course_id)
            find_course = [i.teach_id for i in teach_filter]
            takeup_filter = takeup_filter.filter(teach_id__in=find_course)
        except ValueError:
            return HttpResponseBadRequest()
    if teacher_id is not None:
        try:
            takeup_filter = takeup_filter.filter(teacher_id=teacher_id)
        except ValueError:
            return HttpResponseBadRequest()
    elif room_id is not None:
        try:
            room_id = int(room_id)
            takeup_filter = takeup_filter.filter(room_id=room_id)
        except ValueError:
            return HttpResponseBadRequest()
    elif time_id is not None:
        try:
            time_id = int(time_id)
            takeup_filter = takeup_filter.filter(time_id=time_id)
        except ValueError:
            return HttpResponseBadRequest()
    if count is None:
        count = 0xffff
    else:
        try:
            count = int(count)
            takeup_filter = takeup_filter[:count]
        except ValueError:
            return JsonResponse({'success': False, 'reason': '`count` is not an integer'})

    takeup_filter = takeup_filter.order_by('teacher_id')
    res = [{
        'course_name': teach.objects.get(teach_id=r.teach_id.teach_id).course_id.name,
        'teacher_name': teacher.objects.get(teacher_id=r.teacher_id.teacher_id_id).name,
        'room_name': room.objects.get(room_id=r.room_id.room_id).location,
        'time_id': r.time_id.time_id,
        'time_start': time.objects.get(time_id=r.time_id.time_id).start,
        'time_end': time.objects.get(time_id=r.time_id.time_id).end,
        'time_day': time.objects.get(time_id=r.time_id.time_id).day,
        'duplicate': teach.objects.get(teach_id=r.teach_id.teach_id).duplicate,
        'capacity': teach.objects.get(teach_id=r.teach_id.teach_id).capacity,
        #'exam_date': teach.objects.get(teach_id=r.teach_id.teach_id).exam_date
    } for r in takeup_filter]

    return JsonResponse({'success': True, 'pagecount': (len(res) + 19) // 20}, safe=False)


@csrf_exempt
def api_course_update(request):
    if request.method != 'POST':
        return HttpResponseNotFound()
    course_id = request.POST.get('course_id')
    teacher_id = request.POST.get('teacher_id')
    duplicate = request.POST.get('duplicate')
    capacity = request.POST.get('capacity')
    exam_date_year = request.POST.get('exam_date_year')
    exam_date_month = request.POST.get('exam_date_month')
    exam_date_day = request.POST.get('exam_date_day')
    if course_id is None or teacher_id is None or duplicate is None:
        return HttpResponseBadRequest()
    try:
        duplicate = int(duplicate)
    except ValueError:
        return HttpResponseBadRequest()
    teach_filter = teach.objects.filter(course_id=course_id, teacher_id=teacher_id, duplicate=duplicate)
    if len(teach_filter) == 0:
        return HttpResponseBadRequest()
    if capacity is not None:
        try:
            teach_filter[0].capacity = int(capacity)
        except ValueError:
            return HttpResponseBadRequest()
    if exam_date_year is not None and exam_date_month is not None and exam_date_day is not None:
        try:
            teach_filter[0].exam_date = datetime.date(int(exam_date_year), int(exam_date_month), int(exam_date_day))
            teach_filter[0].save()
        except ValueError:
            return HttpResponseBadRequest()

    return JsonResponse({'success': True}, safe=False)


@csrf_exempt
def api_course_delete(request):
    if request.method != 'POST':
        return HttpResponseNotFound()
    re_delete_cnt = 0
    delete = eval(request.POST.get('delete'))
    for i in delete:
        course_id = i.get('course_id')
        teacher_id = i.get('teacher_id')
        room_id = i.get('room_id')
        duplicate = i.get('duplicate')
        print(course_id, teacher_id, room_id, duplicate)
        takeup_filter = takeup.objects.all()
        if course_id is not None:
            try:
                teach_filter = teach.objects.filter(course_id=course_id)
                find_course = [i.teach_id for i in teach_filter]
                takeup_filter = takeup_filter.filter(teach_id__in=find_course)
            except ValueError:
                return JsonResponse({'success': False, 'reason': '`course_id` is not an integer'})
        if teacher_id is not None:
            try:
                takeup_filter = takeup_filter.filter(teacher_id=teacher_id)
            except ValueError:
                return JsonResponse({'success': False, 'reason': '`teacher_id` is not an integer'})
        if room_id is not None:
            try:
                room_id = int(room_id)
                takeup_filter = takeup_filter.filter(room_id=room_id)
            except ValueError:
                return JsonResponse({'success': False, 'reason': '`room_id` is not an integer'})
        if duplicate is not None:
            try:
                duplicate = int(duplicate)
                teach_filter = teach.objects.filter(duplicate=duplicate)
                find_duplicate = [i.teach_id for i in teach_filter]
                takeup_filter = takeup_filter.filter(teach_id__in=find_duplicate)
            except ValueError:
                return JsonResponse({'success': False, 'reason': '`duplicate` is not an integer'})
        delete_cnt = len(takeup_filter)
        re_delete_cnt += delete_cnt
        takeup_filter.delete()

    return JsonResponse({'success': True, 'reason': 'OK %d course(s) deleted' % re_delete_cnt})


@csrf_exempt
def api_course(request):
    if request.method == 'GET':
        return api_course_get(request)
    elif request.method == 'POST':
        return api_course_post(request)
    else:
        return HttpResponseNotFound()



