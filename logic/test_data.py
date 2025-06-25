import pandas as pd

movie_ratings_examples = [
    {
        "data": pd.DataFrame({
            "user_id": [1,1,2,2,3,3,4,4,5,5],
            "movie_id": [101,102,101,103,102,103,101,104,105,103],
            "rating": [5,3,4,2,1,5,4,3,2,4]
        }),
        "target": {"user_id": 1, "movie_id": 103, "k": 3},
        "description": "Базовый пример с 5 пользователями"
    },
    {
        "data": pd.DataFrame({
            "user_id": [1,1,2,2,3,3,4,5],
            "movie_id": [101,102,101,103,102,103,101,102],
            "rating": [4,2,5,1,3,5,4,3]
        }),
        "target": {"user_id": 3, "movie_id": 101, "k": 2},
        "description": "Пример с пропущенными значениями"
    },
    {
        "data": pd.DataFrame({
            "user_id": [1,2,3,4,5,6,7,8,9,10],
            "movie_id": [101,101,101,101,101,102,102,102,102,102],
            "rating": [5,4,3,2,1,1,2,3,4,5]
        }),
        "target": {"user_id": 1, "movie_id": 102, "k": 5},
        "description": "Поляризованные оценки (явные фавориты)"
    },
    {
        "data": pd.DataFrame({
            "user_id": [1,1,1,2,2,2,3,3,3],
            "movie_id": [101,102,103,101,102,103,101,102,103],
            "rating": [3,3,3,4,4,4,5,5,5]
        }),
        "target": {"user_id": 1, "movie_id": 104, "k": 2},
        "description": "Новый товар (cold start problem)"
    },
    {
        "data": pd.DataFrame({
            "user_id": [1,1,2,2,3,3,4,4,5,5,6,6],
            "movie_id": [101,102,101,103,102,103,101,104,105,103,101,106],
            "rating": [5,1,5,1,5,1,5,1,5,1,5,1]
        }),
        "target": {"user_id": 3, "movie_id": 101, "k": 4},
        "description": "Явное разделение на две группы пользователей"
    }
]

games_collaborative_examples = [
    {
        "data": pd.DataFrame({
            "user_id": [1,1,2,2,3,3,4,4],
            "game": ["Witcher3","Cyberpunk","Witcher3","Skyrim","Cyberpunk","Skyrim","Witcher3","GTA5"],
            "hours": [50,20,30,60,10,40,45,35]
        }),
        "target": {"user_id": 1, "game": "Skyrim", "k": 2},
        "description": "Базовый пример с играми"
    },
    {
        "data": pd.DataFrame({
            "user_id": [1,2,3,4,5,6],
            "game": ["Witcher3","Witcher3","Witcher3","Witcher3","Witcher3","Witcher3"],
            "hours": [100,5,80,20,60,30]
        }),
        "target": {"user_id": 1, "game": "Cyberpunk", "k": 3},
        "description": "Все пользователи играли в одну игру"
    },
    {
        "data": pd.DataFrame({
            "user_id": [1,1,2,2,3,3,4,4,5,5],
            "game": ["Witcher3","Cyberpunk","Witcher3","Skyrim","Cyberpunk","Skyrim","Witcher3","GTA5","Skyrim","FIFA"],
            "hours": [120,10,90,60,5,30,80,50,40,20]
        }),
        "target": {"user_id": 3, "game": "Witcher3", "k": 2},
        "description": "Разные категории игр"
    },
    {
        "data": pd.DataFrame({
            "user_id": [1,2,3,4,5],
            "game": ["Witcher3","Cyberpunk","Skyrim","GTA5","FIFA"],
            "hours": [100,50,80,60,30]
        }),
        "target": {"user_id": 1, "game": "FIFA", "k": 1},
        "description": "Каждый пользователь играл только в одну игру"
    },
    {
        "data": pd.DataFrame({
            "user_id": [1,1,1,2,2,2,3,3,3],
            "game": ["Witcher3","Cyberpunk","Skyrim","Witcher3","Cyberpunk","Skyrim","Witcher3","Cyberpunk","Skyrim"],
            "hours": [50,20,10,60,30,5,70,40,15]
        }),
        "target": {"user_id": 2, "game": "GTA5", "k": 3},
        "description": "Новая игра (cold start)"
    }
]