import random
from logic.task_types import collaborative, content_based #, hybrid

def generate_task():
    task_type = random.choice(["collaborative"]) #, "content_based","hybrid"])
    if task_type=="collaborative":
        return collaborative.generate()
    elif task_type=="content_based":
        return content_based.generate()
    #else:
        #return hybrid.generate()
    
