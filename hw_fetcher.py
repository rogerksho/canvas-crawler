import requests
import json
from datetime import datetime

class Course:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Task:
    def __init__(self, id, course_id, name, due_date, others_submitted, submitted):
        self.id = id
        self.course_id = course_id
        self.name = name
        self.due_date = due_date
        self.others_submitted = others_submitted
        self.submitted = submitted

CANVAS_TOKEN = "1770~KBb4GdfNpBhVafrsMBlCVnTAfBZQGx4iCZ0QFqv28GPiPnzcFgMW66v8vrLy9rYY"
USER_ID = "501847"

courses_url = f'https://umich.instructure.com/api/v1/courses/'
payload = {'per_page':100}
header = {'Authorization': f'Bearer {CANVAS_TOKEN}'}

r = requests.get(courses_url, headers=header, params=payload)

parsed = json.loads(r.text)

with open('data.json', 'w') as outfile:
    json.dump(parsed, outfile, indent=4)

data = r.json()

courses = list()

for i in data:
    if type(i) == dict:
        try:
            start_date = i['start_at']
            date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
            if date > datetime(2020, 5, 1, 0, 0, 0):
                if i['id'] != 429142:
                    courses.append(Course(i['id'], i['name']))
        except KeyError:
            pass

todo = list()

for i in courses:
    ass_url = f"https://umich.instructure.com/api/v1/courses/{i.id}/assignments"
    ass_payload = {'per_page':100, 'include':['submission']}
    ass_r = requests.get(ass_url, headers=header, params=ass_payload)
    ass_parsed = json.loads(ass_r.text)

    for j in ass_r.json():
        due_date = datetime.strptime(j['due_at'], "%Y-%m-%dT%H:%M:%SZ")
        if due_date > datetime.now():
            todo.append(Task(j['id'], j['course_id'], j['name'], j['due_at'], j['has_submitted_submissions'], 'submitted_at' in j))

for u in todo:
    print(u.__dict__)
