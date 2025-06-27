import random
from collaborative import CollaborativeTaskGenerator
from content_based import generate as generate_content_based
from hybrid import generate as generate_hybrid

class MainTaskGenerator:
    def __init__(self):
        self.collab_generator = CollaborativeTaskGenerator()
        self.task_types = {
            "collaborative": self.collab_generator.generate_task,
            "content_based": generate_content_based,
            "hybrid": generate_hybrid
        }
    
