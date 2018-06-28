import requests

def testCourseGET():
    api="http://127.0.0.1:8000/api/admin/course"
    response=requests.get(url=api)
    print(response.text)

def testCoursePOST():
    api="http://127.0.0.1:8000/api/admin/course"
    postdata={
        "courseid":"00010002",
        "examdate":"2018-1-1T11:11",
        "capacity":"100",
        "permit":0
    }
    response=requests.post(url=api,data=postdata)
    print(response.text)


def testTeachGET():
    api = "http://127.0.0.1:8000/api/admin/teach"
    response = requests.get(url=api)
    print(response.text)

def testTeachPOST():
    api = "http://127.0.0.1:8000/api/admin/teach"
    postdata={
        "course":"00010000",
        "tid":"000123",
        "capacity":"110",
        "permit":1
    }
    response = requests.post(url=api, data=postdata)
    print(response.text)


def testStudentInfoUpdate():
    api="http://127.0.0.1:8000/api/admin/student/info"
    postdata={
        "account_id":"3150105000",
        "name":"胖次",
        "dorm":"启真湖底111"
    }
    response=requests.post(url=api,data=postdata)
    print(response.text)

def testTeacherInfoUpdate():
    api = "http://127.0.0.1:8000/api/admin/teacher/info"
    postdata = {
        "account_id": "000123",
        "name": "胖次1",
        "title": "教授",
        "office":"410",
        "management":"软件工程"
    }
    response = requests.post(url=api, data=postdata)
    print(response.text)

def testUpdateCourse():
    api="http://127.0.0.1:8000/api/admin/modifycourse"
    postdata={
        "id":"00010000",
        "name":"程序sheji",
        "hour":2.5,
        "credit":3,
        "intro":"a course very head",
        "type":"0",
        "exam_date":"2018-10-25T14:30",

    }
    response=requests.post(url=api,data=postdata)
    print(response.text)


def testCourseAcceptIDList():
    api="http://127.0.0.1:8000/api/admin/listCourseAcceptedId"
    response=requests.get(url=api)
    print(response.text)

def testCourseAcceptGet():
    api="http://127.0.0.1:8000/api/admin/acceptedCourse"
    postdata={
        "course_id":"00010000"
    }
    response=requests.get(url=api,params=postdata)
    print(response.text)

def testCourseAcceptPost():
    api="http://127.0.0.1:8000/api/admin/acceptedCourse"
    postdata = {
        "id": "00010000",
        "name": "程序sheji",
        "hour": 2.5,
        "credit": 3,
        "intro": "a course very head",
        "type": "0",
        "exam_date": "2018-10-25T14:30",

    }
    response = requests.post(url=api, data=postdata)
    print(response.text)
def testTeachAcceptGet():
    api="http://127.0.0.1:8000/api/admin/acceptedTeach"
    postdata={
        "teach_id":"1"
    }
    response=requests.get(url=api,params=postdata)
    print(response.text)

def testTeachAcceptPost():
    api = "http://127.0.0.1:8000/api/admin/acceptedTeach"
    postdata = {
        "teach_id": "1",
        "tid":"000123",
        "capacity":"30"
    }
    response = requests.post(url=api, data=postdata)
    print(response.text)

if __name__=="__main__":
    testTeachPOST()