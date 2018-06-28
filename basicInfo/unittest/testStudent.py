import requests

def testStudentInfo():
    api="http://127.0.0.1:8000/api/student/info"
    post={
        "account_id":"3150105000"
    }
    response=requests.get(url=api,params=post)
    print(response.text)

def testStudentExam():
    api = "http://127.0.0.1:8000/api/student/exam"
    post = {
        "account_id": "3150105000"
    }
    response = requests.get(url=api, params=post)
    print(response.text)

def testStudentGrade():
    api = "http://127.0.0.1:8000/api/student/grade"
    post = {
        "account_id": "3150105000"
    }
    response = requests.get(url=api, params=post)
    print(response.text)


if __name__=="__main__":
    testStudentExam()