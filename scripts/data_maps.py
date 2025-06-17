"""data_maps.py

Словари и вспомогательные списки для конвертации данных Bank Marketing (#222).
"""
import numpy as np

# Приближённые средние годовые доходы, EUR
JOB_INCOME_MAP: dict[str, float] = {
    'admin.': 45000,
    'blue-collar': 35000,
    'entrepreneur': 55000,
    'housemaid': 20000,
    'management': 60000,
    'retired': 25000,
    'self-employed': 50000,
    'services': 30000,
    'student': 12000,
    'technician': 40000,
    'unemployed': 15000,
    'unknown': np.nan,
}

CITY_LIST: list[str] = [
    'Москва', 'Санкт-Петербург', 'Новосибирск',
    'Екатеринбург', 'Казань'
]

F_NAMES: list[str] = ['Иван', 'Мария', 'Сергей', 'Ольга', 'Алексей']
L_NAMES: list[str] = ['Иванов', 'Петрова', 'Сидоров', 'Смирнова', 'Кузнецов']
