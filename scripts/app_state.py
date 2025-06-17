"""
app_state.py – хранит текущий режим данных в рамках сессии GUI.
"""
from enum import Enum, auto

class DataMode(Enum):
    REAL = auto()
    SYNTH = auto()

mode: DataMode = DataMode.REAL          # значение по умолчанию
