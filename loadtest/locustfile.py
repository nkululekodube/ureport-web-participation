from locust import HttpLocust, TaskSet

def index(l):
    l.client.get("/")

def register(l):
    l.client.get("/register")

class UserBehavior(TaskSet):
    tasks = {index: 2, register: 1}

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
