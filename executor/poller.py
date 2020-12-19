from executor.task_manager import TaskManager
import polling2, time

def task_poller_validator(response):
    if response:
        print("All dependent tasks have been executed, spawning next layer")
        return True
    return False

def task_poller(tasks, tm: TaskManager):        
    polling2.poll(
        lambda: tm.check_status(tasks)!=False,
        step=1,
        poll_forever=True
    )