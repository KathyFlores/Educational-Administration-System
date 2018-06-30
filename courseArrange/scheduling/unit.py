import requests
import unittest


class TestCourse(unittest.TestCase):
    def testPost(self):
        api = 'http://127.0.0.1:8000/course_arrange/api/scheduling/course/'
        response = requests.post(url=api,
                      data={'teacher_id': "000123", 'course_id': "00010001", 'time_id': "[3, 4, 5]", 'room_id': "1", 'duplicate': 2})
        print(response.text)