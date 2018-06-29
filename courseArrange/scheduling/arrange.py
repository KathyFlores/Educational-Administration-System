from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from basicInfo.models import time, teacher,  course, room, teach, takeup
import random
import datetime
import logging

def calc_course_time(credit):
	#return int(credit // 2 + 1)
	ret = int(2 * credit)
	ret = min(ret,6)
	ret = max(ret,2)
	return ret

def meet_require(CourseType,RoomType):
	for t in CourseType:
		if (not (t in RoomType)):
			return False
	return True

def between(i,start,end):
	st = [0,
		 datetime.time(8,0,0),
		 datetime.time(8,50,0),
		 datetime.time(9,50,0),
		 datetime.time(10,40,0),
		 datetime.time(11,30,0),
		 datetime.time(13,15,0),
		 datetime.time(14,5,0),
		 datetime.time(14,55,0),
		 datetime.time(15,55,0),
		 datetime.time(16,45,0),
		 datetime.time(18,30,0),
		 datetime.time(19,20,0),
		 datetime.time(20,10,0)]
	return (st[i] >= start and st[i] < end)

#period:{1:[1,2,3],2:[4,5]}
def get_period(time_id):
	for t in time_list:
		if (t.time_id == time_id):			
			day = t.day
			while (day > 7):
				day = day - 7
			start = t.start
			end = t.end
			for i in range(1,14):
				if between(i,start,end):
					return [day,i]
	return [0,0]


def construct_single_arrange(course_id,teacher_id,room_id,period):
	return {
		'course_id': course_id,
		'teacher_id': teacher_id,
		'room_id': room_id,
		'period': period
	}

def rev_dict(lst):
	rev = {}
	for i in range(len(lst)):
		rev[lst[i]] = i
	return rev

def RET(lst):
	ret = []
	for t in lst:
		ret.append(t)
	return JsonResponse(ret, safe = False)

def time_cmp(t1,t2):
	if (t1.day == t2.day):
		return t1.start < t2.start
	return (t1.day < t2.day)

@csrf_exempt
def api_arrange(request):
	if request.method != 'GET':
		return HttpResponseNotFound()
	global time_list,teacher_list,course_list,room_list,teach_list
	global teacher_dict,course_dict,room_dict

	tmp_time_list = time.objects.all()
	time_list = []
	for t in tmp_time_list:
		if (t.day > 0 and t.day <= 7):
			time_list.append(t)
	for i in range(0,len(time_list)):
		for j in range(i+1,len(time_list)):
			if (time_cmp(time_list[j],time_list[i])):
				(time_list[i],time_list[j]) = (time_list[j],time_list[i])
	starttime = [[],[],[],[]]
	for i in range(0,len(time_list)):
		t = time_list[i]
		if (t.start.hour == 8 and t.start.minute == 0):
			starttime[2].append(i)
		if (t.start.hour == 9 and t.start.minute == 50):
			starttime[2].append(i)
			starttime[3].append(i)
		if (t.start.hour == 13 and t.start.minute == 15):
			starttime[3].append(i)
		if (t.start.hour == 14 and t.start.minute == 5):
			starttime[2].append(i)
		if (t.start.hour == 15 and t.start.minute == 55):
			starttime[2].append(i)
		if (t.start.hour == 18 and t.start.minute == 30):
			starttime[2].append(i)
			starttime[3].append(i)
	random.shuffle(starttime[2])
	random.shuffle(starttime[3])
	time_arrange = [[],[2],[2],[3],[2,2],[2,3],[3,3]]
	
	teacher_list = teacher.objects.all()
	course_list = course.objects.all()
	room_list = room.objects.all()
	teach_list = teach.objects.all()
	course_dict = {}
	room_dict = {}
	
	#for t in freetime_list:
	#	res.append(t.teacher_id.account_id)
	#	res = str(type(t.teacher_id_id))
	#return JsonResponse(res, safe = False)
	for t in course_list:
		course_dict[t.course_id] = t
	for t in room_list:
		room_dict[t.room_id] = t
		print(t.room_id)

	arrange_all = []
	room_time = set()
	teacher_time = set()
	#random.shuffle(teach_list)
	for t in teach_list:
		teacher_id = t.teacher_id_id
		course_id = t.course_id_id
		course_time = int(course_dict[course_id].hour)
		#course_time = calc_course_time(course_dict[course_id].credit)
		candidate_room_time = set()
		candidate_teacher_time = set()
		arrange_this_teach = []
		course_type = course_dict[course_id].type
		teach_ok = True
		for period_length in time_arrange[course_time]:
			find_period = False
			for r in room_list:
				room_id = r.room_id
				room_type = room_dict[room_id].type
				if (not meet_require(course_type,room_type)):
					continue
				arrange = {
					'teach_id':t.teach_id,
					'course_id':course_id,
					'teacher_id':teacher_id,
					'room_id':room_id,
					'time_ids':[]
				}
				period = {}
				for i in range(1,8):
					period[i] = []
				
				for st in starttime[period_length]:
					period_ok = True
					for i in range(0,period_length):
						time_id = time_list[st + i].time_id
						if (((room_id,time_id) in room_time) or ((teacher_id,time_id) in teacher_time) or ((teacher_id,time_id) in candidate_teacher_time)):
							period_ok = False
							break
					if (not period_ok):
						continue
					find_period = True
					for i in range(0,period_length):
						time_id = time_list[st + i].time_id
						candidate_room_time.add((room_id,time_id))
						candidate_teacher_time.add((teacher_id,time_id))
						[day,classnum] = get_period(time_id)
						period[day].append(classnum)
						arrange['time_ids'].append(time_id)
					break
				if (not find_period):
					continue
				arrange['period'] = period
				arrange_this_teach.append(arrange)
				break
			if (not find_period):
				teach_ok = False
				break
		if  (not teach_ok):
			continue
		for arrange in arrange_this_teach:
			arrange_all.append(arrange)
		for (room_id,time_id) in candidate_room_time:
			room_time.add((room_id,time_id))
		for (teacher_id,time_id) in candidate_teacher_time:
			teacher_time.add((teacher_id,time_id))
	
	takeup.objects.all().delete()
	for arrange in arrange_all:
		for time_id in arrange['time_ids']:
			ins_time_id = time.objects.get(time_id = time_id)
			ins_teach_id = teach.objects.get(teach_id = arrange['teach_id'])
			ins_room_id = room.objects.get(room_id = arrange['room_id'])
			ins_teacher_id = teacher.objects.get(teacher_id = arrange['teacher_id'])
			take_up_ins = takeup(teach_id = ins_teach_id,time_id = ins_time_id,room_id = ins_room_id,teacher_id = ins_teacher_id)
			take_up_ins.save()
	return JsonResponse(arrange_all, safe = False)


'''
res = [{
        'course_id': r.course_id.course_id,
        'teacher_id': r.teacher_id.teacher_id,
        'room_id': r.room_id.room_id,
        'time_id': r.time_id.time_id
    } for r in takeup_filter]

    return JsonResponse(res, safe=False)

'''
