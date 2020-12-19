import random
from time import sleep
from executor.celeryd import app as celery

@celery.task(bind=True)
def task1(self, *args, **kwargs):
    print("Running task one returns 1")
    return 1

@celery.task(bind=True)
def task2(self, *args, **kwargs):
    print("Running task two returns 1.2")
    return 1.2

@celery.task(bind=True)
def task3(self, *args, **kwargs):
    print("Running task 3 returns 1.3")
    return 1.3

@celery.task(bind=True)
def runner(self, id):
    sleep_time = random.randrange(20,100)
    print(f"Running task {id}, task_id {self.request.id} sleeping for {sleep_time} seconds")
    sleep(sleep_time)
    return sleep_time

