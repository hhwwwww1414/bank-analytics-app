# tests/conftest.py

import sys
from pathlib import Path

# Вставляем в начало sys.path путь на уровень выше — туда, где лежит папка scripts/
root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(root))
