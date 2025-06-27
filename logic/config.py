from pathlib import Path

# Конфигурация проекта
class Config:
    TEST_CASES_DIR = Path("test_cases")
    REPORTS_DIR = Path("reports")
    STYLE_CONFIG = {
        'flake8': {
            'command': 'flake8 --max-line-length=120 --ignore=E203,W503,E501',
            'timeout': 30
        },
        'black': {
            'command': 'black --check --diff --quiet',
            'timeout': 45
        }
    }
    DATASETS = {
        'collaborative': ['movie_ratings.csv', 'games_collaborative.csv'],
        'content': ['movie_content.csv', 'game_descriptions.csv'],
        'hybrid': ['hybrid_movies.csv', 'hybrid_games.csv']
    }