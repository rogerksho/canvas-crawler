import requests
import json
from datetime import datetime

# course class
class Course:
    def __init__(self, id, name):
        self.id = id
        self.name = name

# assignment/task class
class Task:
    def __init__(self, id, course_id, name, due_date, others_submitted, submitted):
        self.id = id
        self.course_id = course_id
        self.name = name
        self.due_date = due_date
        self.others_submitted = others_submitted
        self.submitted = submitted
        self.time_left = due_date - datetime.now()

# crucial variables for api access
CANVAS_TOKEN = "1770~KBb4GdfNpBhVafrsMBlCVnTAfBZQGx4iCZ0QFqv28GPiPnzcFgMW66v8vrLy9rYY"
USER_ID = "501847"

# url and params (and headers) for fetching courses
courses_url = f'https://umich.instructure.com/api/v1/courses/'
payload = {'per_page':100}
header = {'Authorization': f'Bearer {CANVAS_TOKEN}'}

# http GET
r = requests.get(courses_url, headers=header, params=payload)

# initialise list of courses
courses = list()

# filter out all old courses
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

# initialise list of assignments
todo = list()

# for each course, fetch assignments
for i in courses:
    ass_url = f"https://umich.instructure.com/api/v1/courses/{i.id}/assignments"
    ass_payload = {'per_page':100, 'include':['submission']}
    ass_r = requests.get(ass_url, headers=header, params=ass_payload)
    ass_parsed = json.loads(ass_r.text)

    for j in ass_r.json():
        due_date = datetime.strptime(j['due_at'], "%Y-%m-%dT%H:%M:%SZ")

        # add to assignment list only if it is due in the future
        if due_date > datetime.now():
            todo.append(Task(j['id'], j['course_id'], j['name'], due_date, j['has_submitted_submissions'], j['submission']['submitted_at'] is not None))

# sorts assignments by due date
todo_sorted = (sorted(todo, key=lambda Task: Task.due_date))

# for sorted todo list, format data and prettyprint (but not actually that pretty xd)
for u in todo_sorted:
    print("==============================")
    print(f"TASK {i}")
    if u.submitted:
        print("## SUBMITTED ALREADY ##")
    print("name: ", u.name)
    if u.time_left.days > 0:
        s = u.time_left.seconds
        h, s = divmod(s, 3600)
        print("time left: ",u.time_left.days , " days and ", h, " hours")
    else:
        s = u.time_left.seconds
        h, s = divmod(s, 3600)
        m, s = divmod(s, 60)
        print("time left: ", h, " hours and ", m, " minutes")
    print('course: ', u.course_id)
    i += 1
