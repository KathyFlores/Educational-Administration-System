from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from basicInfo.models import room


def api_room_get(request):
    room_id = request.GET.get('room_id')
    if room_id is None:
        room_id = 0
    else:
        try:
            room_id = int(room_id)
        except ValueError:
            return HttpResponseBadRequest()

    count = request.GET.get('count')
    if count is None:
        count = 0xffff
    else:
        try:
            count = int(count)
        except ValueError:
            return HttpResponseBadRequest()
    room_filter = room.objects.order_by('room_id').filter(room_id__gte=room_id)[:count]
    res = [{
        'room_id': r.room_id,
        'capacity': r.capacity,
        'location': r.location,
        'type': r.type
    } for r in room_filter]
    return JsonResponse(res, safe=False)


@csrf_exempt
def api_room_get_pagecount(request):
    if request.method != 'GET':
        return HttpResponseNotFound()
    room_id = request.GET.get('room_id')
    if room_id is None:
        room_id = 0
    else:
        try:
            room_id = int(room_id)
        except ValueError:
            return HttpResponseBadRequest()

    count = request.GET.get('count')
    if count is None:
        count = 0xffff
    else:
        try:
            count = int(count)
        except ValueError:
            return HttpResponseBadRequest()
    room_filter = room.objects.filter(room_id__gte=room_id)[:count]
    res = [{
        'room_id': r.room_id,
        'capacity': r.capacity,
        'location': r.location,
        'type': r.type
    } for r in room_filter]
    pagecount = (len(res) + 19) // 20
    return JsonResponse({'success': True, 'pagecount':pagecount})


def api_room_post(request):
    room_id = request.POST.get('room_id')
    capacity = request.POST.get('capacity')
    location = request.POST.get('location')
    room_type = request.POST.get('type')
    if room_id is None:
        room_all = room.objects.all()
        max_room_id = 0
        for r in room_all:
            max_room_id = max(max_room_id, r.room_id)
        room_id = max_room_id + 1
    if capacity is None:
        return JsonResponse({'success': False, 'reason': '`capacity` is required'})
    if location is None:
        return JsonResponse({'success': False, 'reason': '`location` is required'})
    if room_type is None:
        return JsonResponse({'success': False, 'reason': '`type` is required'})

    try:
        room_id = int(room_id)
    except ValueError:
        return JsonResponse({'success': False, 'reason': '`room_id` is not an integer'})
    try:
        capacity = int(capacity)
    except ValueError:
        return JsonResponse({'success': False, 'reason': '`capacity` is not an integer'})

    room_filter = room.objects.filter(room_id=room_id)
    if len(room_filter) == 0:
        room.objects.create(
            room_id=room_id,
            capacity=capacity,
            location=location,
            type=room_type
        )
        return JsonResponse({'success': True, 'reason': 'OK room created'})
    else:
        room_filter[0].capacity = capacity
        room_filter[0].location = location
        room_filter[0].type = room_type
        room_filter[0].save()
        return JsonResponse({'success': True, 'reason': 'OK room modified'})


@csrf_exempt
def api_room_delete(request):
    if request.method != 'POST':
        return HttpResponseNotFound()
    room_ids = eval(request.POST.get('room_id'))
    for i in range(len(room_ids)):
        try:
            room_ids[i] = int(room_ids[i])
        except ValueError:
            return JsonResponse({'success': False, 'reason': 'One of the `room_id` is not an integer'})

    room_filter = room.objects.filter(room_id__in=room_ids)
    delete_cnt = len(room_filter)
    room_filter.delete()
    return JsonResponse({'success': True, 'reason': 'OK %d room(s) deleted' % delete_cnt})


@csrf_exempt
def api_room(request):
    if request.method == 'GET':
        return api_room_get(request)
    elif request.method == 'POST':
        return api_room_post(request)
    else:
        return HttpResponseNotFound()
