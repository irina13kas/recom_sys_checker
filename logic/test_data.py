import pandas as pd
import numpy as np
from typing import List, Dict

class TestDataGenerator:
    @staticmethod
    def generate_user_based_cases() -> List[Dict]:
        """Генерация 5 тестовых случаев для User-Based CF"""
        return [
            # Случай 1: Базовый пример
            {
                "data": pd.DataFrame({
                    "user_id": [1, 1, 2, 2, 3, 3, 4, 4],
                    "movie_id": [101, 102, 101, 103, 102, 103, 101, 104],
                    "rating": [5, 3, 4, 2, 1, 5, 4, 3]
                }),
                "target": {"user_id": 1, "movie_id": 103, "k": 2},
                "description": "User-Based: Базовый пример (ожидается высокая схожесть пользователей 1 и 2)"
            },
            
            # Случай 2: Холодный старт
            {
                "data": pd.DataFrame({
                    "user_id": [1, 1, 2, 2, 3, 3],
                    "movie_id": [101, 102, 101, 103, 102, 103],
                    "rating": [4, 2, 5, 1, 3, 5]
                }),
                "target": {"user_id": 4, "movie_id": 101, "k": 2},  # Новый пользователь
                "description": "User-Based: Холодный старт (новый пользователь)"
            },
            
            # Случай 3: Явные предпочтения
            {
                "data": pd.DataFrame({
                    "user_id": [1,1,1,2,2,2,3,3,3],
                    "movie_id": [101,102,103,101,102,103,101,102,103],
                    "rating": [5,5,5,3,3,3,1,1,1]  # Четкие группы пользователей
                }),
                "target": {"user_id": 1, "movie_id": 104, "k": 2},
                "description": "User-Based: Явные группы пользователей"
            },
            
            # Случай 4: Разреженные данные
            {
                "data": pd.DataFrame({
                    "user_id": [1,2,3,4,5,6,7,8],
                    "movie_id": [101,101,101,101,102,102,102,102],
                    "rating": [5,4,3,2,1,2,3,4]  # Мало пересечений
                }),
                "target": {"user_id": 1, "movie_id": 102, "k": 3},
                "description": "User-Based: Разреженные данные"
            },
            
            # Случай 5: Противоположные вкусы
            {
                "data": pd.DataFrame({
                    "user_id": [1,1,2,2,3,3],
                    "movie_id": [101,102,101,102,101,102],
                    "rating": [5,1,5,1,1,5]  # Противоположные оценки
                }),
                "target": {"user_id": 1, "movie_id": 103, "k": 1},
                "description": "User-Based: Противоположные вкусы пользователей"
            }
        ]

    @staticmethod
    def generate_item_based_cases() -> List[Dict]:
        """Генерация 5 тестовых случаев для Item-Based CF"""
        return [
            # Случай 1: Базовый пример
            {
                "data": pd.DataFrame({
                    "user_id": [1,1,2,2,3,3],
                    "movie_id": [101,102,101,103,102,103],
                    "rating": [4,2,5,1,3,5]
                }),
                "target": {"user_id": 3, "movie_id": 101, "k": 2},
                "description": "Item-Based: Базовый пример"
            },
            
            # Случай 2: Новый предмет
            {
                "data": pd.DataFrame({
                    "user_id": [1,1,2,2,3,3,4,4],
                    "movie_id": [101,102,101,103,102,103,101,104],
                    "rating": [5,3,4,2,1,5,4,3]
                }),
                "target": {"user_id": 1, "movie_id": 105, "k": 3},  # Новый предмет
                "description": "Item-Based: Холодный старт (новый предмет)"
            },
            
            # Случай 3: Популярные предметы
            {
                "data": pd.DataFrame({
                    "user_id": [1,1,2,2,3,3,4,4,5,5],
                    "movie_id": [101,102,101,102,101,102,101,102,101,103],
                    "rating": [4,5,4,5,4,5,4,5,4,2]  # 102 - популярный
                }),
                "target": {"user_id": 5, "movie_id": 102, "k": 1},
                "description": "Item-Based: Популярные предметы"
            },
            
            # Случай 4: Нишевые предметы
            {
                "data": pd.DataFrame({
                    "user_id": [1,1,2,2,3,3,4,5],
                    "movie_id": [101,102,101,103,102,103,104,104],
                    "rating": [4,2,5,1,3,5,5,5]  # 104 - нишевый
                }),
                "target": {"user_id": 1, "movie_id": 104, "k": 2},
                "description": "Item-Based: Нишевые предметы"
            },
            
            # Случай 5: Противоположные предметы
            {
                "data": pd.DataFrame({
                    "user_id": [1,1,2,2,3,3],
                    "movie_id": [101,102,101,102,101,102],
                    "rating": [5,1,5,1,1,5]  # 101 и 102 противоположны
                }),
                "target": {"user_id": 3, "movie_id": 102, "k": 1},
                "description": "Item-Based: Противоположные предметы"
            }
        ]

    @staticmethod
    def get_all_cases() -> Dict[str, List[Dict]]:
        return {
            "user_based": TestDataGenerator.generate_user_based_cases(),
            "item_based": TestDataGenerator.generate_item_based_cases()
        }







# import pandas as pd

# movie_ratings_examples = [
#     {
#         "data": pd.DataFrame({
#             "user_id": [1,1,2,2,3,3,4,4,5,5],
#             "movie_id": [101,102,101,103,102,103,101,104,105,103],
#             "rating": [5,3,4,2,1,5,4,3,2,4]
#         }),
#         "target": {"user_id": 1, "movie_id": 103, "k": 3},
#         "description": "Базовый пример с 5 пользователями"
#     },
#     {
#         "data": pd.DataFrame({
#             "user_id": [1,1,2,2,3,3,4,5],
#             "movie_id": [101,102,101,103,102,103,101,102],
#             "rating": [4,2,5,1,3,5,4,3]
#         }),
#         "target": {"user_id": 3, "movie_id": 101, "k": 2},
#         "description": "Пример с пропущенными значениями"
#     },
#     {
#         "data": pd.DataFrame({
#             "user_id": [1,2,3,4,5,6,7,8,9,10],
#             "movie_id": [101,101,101,101,101,102,102,102,102,102],
#             "rating": [5,4,3,2,1,1,2,3,4,5]
#         }),
#         "target": {"user_id": 1, "movie_id": 102, "k": 5},
#         "description": "Поляризованные оценки (явные фавориты)"
#     },
#     {
#         "data": pd.DataFrame({
#             "user_id": [1,1,1,2,2,2,3,3,3],
#             "movie_id": [101,102,103,101,102,103,101,102,103],
#             "rating": [3,3,3,4,4,4,5,5,5]
#         }),
#         "target": {"user_id": 1, "movie_id": 104, "k": 2},
#         "description": "Новый товар (cold start problem)"
#     },
#     {
#         "data": pd.DataFrame({
#             "user_id": [1,1,2,2,3,3,4,4,5,5,6,6],
#             "movie_id": [101,102,101,103,102,103,101,104,105,103,101,106],
#             "rating": [5,1,5,1,5,1,5,1,5,1,5,1]
#         }),
#         "target": {"user_id": 3, "movie_id": 101, "k": 4},
#         "description": "Явное разделение на две группы пользователей"
#     }
# ]

# games_collaborative_examples = [
#     {
#         "data": pd.DataFrame({
#             "user_id": [1,1,2,2,3,3,4,4],
#             "game": ["Witcher3","Cyberpunk","Witcher3","Skyrim","Cyberpunk","Skyrim","Witcher3","GTA5"],
#             "hours": [50,20,30,60,10,40,45,35]
#         }),
#         "target": {"user_id": 1, "game": "Skyrim", "k": 2},
#         "description": "Базовый пример с играми"
#     },
#     {
#         "data": pd.DataFrame({
#             "user_id": [1,2,3,4,5,6],
#             "game": ["Witcher3","Witcher3","Witcher3","Witcher3","Witcher3","Witcher3"],
#             "hours": [100,5,80,20,60,30]
#         }),
#         "target": {"user_id": 1, "game": "Cyberpunk", "k": 3},
#         "description": "Все пользователи играли в одну игру"
#     },
#     {
#         "data": pd.DataFrame({
#             "user_id": [1,1,2,2,3,3,4,4,5,5],
#             "game": ["Witcher3","Cyberpunk","Witcher3","Skyrim","Cyberpunk","Skyrim","Witcher3","GTA5","Skyrim","FIFA"],
#             "hours": [120,10,90,60,5,30,80,50,40,20]
#         }),
#         "target": {"user_id": 3, "game": "Witcher3", "k": 2},
#         "description": "Разные категории игр"
#     },
#     {
#         "data": pd.DataFrame({
#             "user_id": [1,2,3,4,5],
#             "game": ["Witcher3","Cyberpunk","Skyrim","GTA5","FIFA"],
#             "hours": [100,50,80,60,30]
#         }),
#         "target": {"user_id": 1, "game": "FIFA", "k": 1},
#         "description": "Каждый пользователь играл только в одну игру"
#     },
#     {
#         "data": pd.DataFrame({
#             "user_id": [1,1,1,2,2,2,3,3,3],
#             "game": ["Witcher3","Cyberpunk","Skyrim","Witcher3","Cyberpunk","Skyrim","Witcher3","Cyberpunk","Skyrim"],
#             "hours": [50,20,10,60,30,5,70,40,15]
#         }),
#         "target": {"user_id": 2, "game": "GTA5", "k": 3},
#         "description": "Новая игра (cold start)"
#     }
# ]