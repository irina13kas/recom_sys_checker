from abc import ABC, abstractmethod
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds
from typing import Dict, Any

class BaseValidator(ABC):
    """Абстрактный базовый класс для валидаторов"""
    @abstractmethod
    def validate(self, task_params: Dict, user_function: callable, test_data: Dict) -> Dict:
        pass

    @staticmethod
    def create_report(passed: bool, expected: Any, actual:Any, test_case: str, error: str = None) -> Dict:
        return {
            "passed": passed,
            "expected": expected,
            "actual": actual,
            "test_case": test_case,
            "error": error
        }
    
class CollaborativeValidator(BaseValidator):
    """Валидатор для коллаборативной фильтрации"""

    def validate(self, task_params: Dict, user_function: callable, test_data: Dict) -> Dict:
        data = test_data["data"]
        target = test_data["target"]

        try:
            if task_params["algorithm"] == "k-NN":
                excepted = self._knn_predict(data, target, task_params)
            elif task_params["algorithm"] == "SVD":
                excepted = self._svd_predict(data, target, task_params)
            elif task_params["algorithm"] == "ALS":
                excepted = self._als_predict(data, target, task_params)
            else:
                raise ValueError(f"Unknown algorithm: {task_params['algorithm']}")
                
            user_result = user_function(data, **target)

            return self.create_report(
                passed = np.isclose(excepted, user_result, atol=0.1),
                excepted = round(float(excepted), 2),
                actual = round(float(user_result), 2),
                test_case = test_data["description"]
            )
        except Exception as e:
            return self.create_report(
                passed=False,
                expected=None,
                actual=None,
                test_case=test_data["description"],
                error=str(e)
            )
            
    def _knn_predict(self, df, target, params):
        if params["filter_type"] == "user_based":
            return self._user_based_knn(df, target)
        return self._item_based_knn(df, target)
            
    def _user_based_knn(self, df, target):
        value_col = "rating" if "rating" in df.columns else "hours"
        item_col = "movie_id" if "movie_id" in df.colums else "game"

        pivot = df.pivot_table(
            index = "user_id",
            columns = item_col,
            values = value_col,
            fill_value = 0
        )

        sim = cosine_similarity(pivot)
        target_idx = pivot.index.get_loc(target["user_id"])
        nearest = np.argsort(sim[target_idx])[-target["k"]-1:-1]
        return pivot.iloc[nearest][target.get("movie_id") or target["game"]].mean()
            
    def _item_based_knn(self, df, target):
        """Универсальная реализация Item-Based k-NN"""
        value_col = self._get_value_column(df)
        item_col = self._get_item_column(df)
        user_id = target["user_id"]
        item = target.get("movie_id") or target["game"]
        k = target["k"]

        pivot = self._create_pivot(df, index="user_id", columns=item_col, values=value_col)
        sim = cosine_similarity(pivot.T)
        item_idx = pivot.columns.get_loc(item)
        nearest = np.argsort(sim[item_idx])[-k-1:-1]
        return pivot.iloc[pivot.index.get_loc(user_id), nearest].mean()

    def _svd_predict(self, df, target):
        """Универсальная реализация SVD предсказания"""
        value_col = self._get_value_column(df)
        item_col = self._get_item_column(df)
        user_id = target["user_id"]
        item = target.get("movie_id") or target["game"]

        pivot = self._create_pivot(df, index="user_id", columns=item_col, values=value_col)
        k_factors = min(2, pivot.shape[0]-1, pivot.shape[1]-1)  # Защита от малых матриц
        U, sigma, Vt = svds(pivot.values, k=k_factors)
        sigma = np.diag(sigma)
        pred = np.dot(np.dot(U, sigma), Vt)
        return pred[pivot.index.get_loc(user_id), pivot.columns.get_loc(item)]

    def _als_predict(self, df, target):
        """Упрощенная реализация ALS (заглушка)"""
        value_col = self._get_value_column(df)
        item_col = self._get_item_column(df)
                
        pivot = self._create_pivot(df, index="user_id", columns=item_col, values=value_col)
        return pivot.mean().mean()  # В реальной реализации использовать implicit.ALS

    @staticmethod
    def _get_value_column(df) -> str:
        """Определяет столбец со значениями (rating/hours)"""
        return "rating" if "rating" in df.columns else "hours"

    @staticmethod
    def _get_item_column(df) -> str:
        """Определяет столбец с предметами (movie_id/game)"""
        return "movie_id" if "movie_id" in df.columns else "game"

    @staticmethod
    def _create_pivot(df, index: str, columns: str, values: str):
        """Создает pivot-таблицу с обработкой отсутствующих значений"""
        return df.pivot_table(
            index=index,
            columns=columns,
            values=values,
            fill_value=0,
            aggfunc='mean'  # На случай дубликатов
            )

class ContentBasedValidator(BaseValidator):
    """Валидатор для контентной фильтрации (заготовка)"""
    
    def validate(self, task_params: Dict, user_function: callable, test_data: Dict) -> Dict:
        # Реализация для контентной фильтрации
        pass

class HybridValidator(BaseValidator):
    """Валидатор для гибридных систем (заготовка)"""
    
    def validate(self, task_params: Dict, user_function: callable, test_data: Dict) -> Dict:
        # Реализация для гибридных систем
        pass

class ValidatorFactory:
    """Фабрика валидаторов"""

    @staticmethod
    def get_validator(task_type: str) -> BaseValidator:
        validators = {
            "collaborative": CollaborativeValidator(),
            "content_based": ContentBasedValidator(),
            "hybrid": HybridValidator()
        }
        return validators.get(task_type, CollaborativeValidator())