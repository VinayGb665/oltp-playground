import os
from .celery_mode import CeleryMode
from .thread_mode import ThreadMode

class FactoryExecutor():
    def pick_executor(self, mode="celery"):
        if mode=="celery":
            return CeleryMode()
        elif mode == "local":
            return ThreadMode()
        else:
            print("Invalid executor mode")
    
def get_executor():
    mode = os.environ.get('executor', 'celery')
    return FactoryExecutor().pick_executor(mode=mode)
