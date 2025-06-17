"""common_funcs.py

Универсальные функции загрузки и сохранения данных, а также утилиты
для конфигурации. Реализованы в функциональном стиле без классов.
"""

import pickle
from pathlib import Path
from configparser import ConfigParser


def save_df(df, file_path: str | Path) -> None:
    """Сохраняет pandas.DataFrame в бинарный файл .pkl"""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open('wb') as f:
        pickle.dump(df, f)


def load_df(file_path: str | Path):
    """Загружает pandas.DataFrame из бинарного файла .pkl"""
    file_path = Path(file_path)
    with file_path.open('rb') as f:
        return pickle.load(f)


def read_config(config_path: str | Path = Path(__file__).parent.parent / 'scripts' / 'app_config.ini') -> ConfigParser:
    """Считывает конфигурационный файл INI"""
    cfg = ConfigParser()
    cfg.read(config_path, encoding='utf-8')
    return cfg
