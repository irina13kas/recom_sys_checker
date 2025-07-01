import random
from logic.task_types.collaborative import CollaborativeTaskGenerator
from logic.task_types.content_based import ContentBasedTaskGenerator
# from hybrid import HybridTaskGenerator               # на будущее

class TaskFactory:
    GENERATORS = {
        #"collaborative": CollaborativeTaskGenerator,
        "content_based": ContentBasedTaskGenerator,
        # "hybrid": HybridTaskGenerator
    }

    @staticmethod
    def generate_description():
        task_type = random.choice(list(TaskFactory.GENERATORS.keys()))
        generator_class = TaskFactory.GENERATORS[task_type]
        generator = generator_class()
        task_text, task_info = generator.generate_task()
        task_info["type"] = task_type
        return task_text, task_info
