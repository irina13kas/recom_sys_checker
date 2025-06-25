import random
from logic.task_types import collaborative, content_based #, hybrid
from logic.test_data import movie_ratings_examples, games_collaborative_examples

def generate_task():
    task_type = random.choice(["collaborative"]) #, "content_based","hybrid"])
    if task_type=="collaborative":
        return collaborative.generate_task()
    elif task_type=="content_based":
        return content_based.generate()
    #else:
        #return hybrid.generate()

def get_test_data(dataset_name: str):
    if dataset_name == "movie_ratings":
        return movie_ratings_examples
    elif dataset_name == "games_collaborative":
        return games_collaborative_examples
    
