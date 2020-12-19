import redis
import json
from executor.celeryd import app 
from celery.result import AsyncResult
from executor.tasks import runner
class TaskManager():
    def __init__(self, *args, **kwargs):
        self.redis = redis.StrictRedis("localhost", db=1)

    def spawn_task(self, id):
        task_id = runner.delay(id)
        # print(f"Spawned task id is {task_id}")
        return task_id
    
    def get_results(self, task_id):
        key_prefix = "celery-task-meta-"
        res = self.redis.get(f"{key_prefix}{task_id}")
        # print(f"Key is {key_prefix}{task_id}")
        if res:
            res = json.loads(res)
            return res.get('result')
        return False
    
    def check_status(self, tasks):
        results = []
        for task_id in tasks:
            res = self.get_results(task_id)
            # print(res)
            if res:
                results.append(res)
            else:
                return False
            
        return results
                
if __name__ == "__main__":
    tm = TaskManager()
    # id = tm.spawn_task(10)
    print(f"Status is {tm.get_status('ac63f5d4-3d34-4d4d-acac-0c727bba0798')}")