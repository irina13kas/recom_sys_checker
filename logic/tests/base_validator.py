from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any
from pathlib import Path
import importlib.util
import numpy as np

class BaseValidator(ABC):
    def __init__(self):
        self.required_functions = []
        self.test_cases = []

    @abstractmethod
    def validate_functionality(self, module, test_case: Dict) -> Dict:
        pass

    def check_structure(self, module) -> Dict:
        missing = [f for f in self.required_functions if not hasattr(module, f)]
        return {
            'passed': not missing,
            'missing_functions': missing
        }

    def load_solution(self, file_path: Path):
        spec = importlib.util.spec_from_file_location("user_solution", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run_tests(self, solution_path: Path) -> Dict:
        try:
            module = self.load_solution(solution_path)
            structure_check = self.check_structure(module)
            
            if not structure_check['passed']:
                return {
                    'structure': structure_check,
                    'functionality': [],
                    'passed': False
                }

            results = []
            for test_case in self.test_cases:
                results.append(self.validate_functionality(module, test_case))

            return {
                'structure': structure_check,
                'functionality': results,
                'passed': all(r['passed'] for r in results)
            }
        except Exception as e:
            return {
                'error': str(e),
                'passed': False
            }