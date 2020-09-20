import requests
import json
from datetime import datetime

class Course:
    def __init__(self, id, name):
        self.id = id
        self.name = name

CANVAS_TOKEN = "1770~KBb4GdfNpBhVafrsMBlCVnTAfBZQGx4iCZ0QFqv28GPiPnzcFgMW66v8vrLy9rYY"
USER_ID = "501847"

url = f'https://umich.instructure.com/api/v1/courses/'
payload = {'per_page':100}
header = {'Authorization': f'Bearer {CANVAS_TOKEN}'}

r = requests.get(url, headers=header, params=payload)

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
                courses.append(Course(i['id'], i['name']))
                print(i['name'])
        except KeyError:
            pass

for i in courses:
    print(i.__dict__)
