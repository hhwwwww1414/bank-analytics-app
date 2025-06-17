"""generate_initial_data.py

Скрипт для генерации тестовых данных «Клиенты» и «Счета» и сохранения
их в каталоге work/data в формате .pkl.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from library.common_funcs import save_df

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)


def generate_clients(n_clients: int = 200, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    cities = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань']
    first_names = ['Иван', 'Мария', 'Сергей', 'Ольга', 'Алексей']
    last_names = ['Иванов', 'Петрова', 'Сидоров', 'Смирнова', 'Кузнецов']

    data = {
        'client_id': np.arange(1, n_clients + 1),
        'last_name': np.random.choice(last_names, n_clients),
        'first_name': np.random.choice(first_names, n_clients),
        'age': np.random.randint(18, 70, n_clients),
        'gender': np.random.choice(['М', 'Ж'], n_clients),
        'city': np.random.choice(cities, n_clients, p=[0.3, 0.25, 0.15, 0.15, 0.15]),
        'income': np.round(np.random.lognormal(10, 0.4, n_clients), 2),
        'reg_date': pd.to_datetime('2018-01-01') + pd.to_timedelta(np.random.randint(0, 365 * 3, n_clients), unit='D')
    }
    return pd.DataFrame(data)


def generate_accounts(clients_df: pd.DataFrame, n_accounts: int | None = None, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed + 1)
    if n_accounts is None:
        n_accounts = len(clients_df) + 100  # чуть больше, чем количество клиентов
    account_types = ['Дебетовый', 'Кредитный', 'Сберегательный']
    currencies = ['RUB', 'USD', 'EUR']

    data = {
        'account_id': np.arange(1, n_accounts + 1),
        'client_id': np.random.choice(clients_df['client_id'], n_accounts),
        'account_type': np.random.choice(account_types, n_accounts),
        'balance': np.round(np.random.uniform(1000, 1_000_000, n_accounts), 2),
        'currency': np.random.choice(currencies, n_accounts),
        'open_date': pd.to_datetime('2018-01-01') + pd.to_timedelta(np.random.randint(0, 365 * 3, n_accounts), unit='D')
    }
    return pd.DataFrame(data)


def main() -> None:
    clients_df = generate_clients()
    accounts_df = generate_accounts(clients_df)

    save_df(clients_df, DATA_DIR / 'clients.pkl')
    save_df(accounts_df, DATA_DIR / 'accounts.pkl')
    print('Generated and saved clients.pkl and accounts.pkl')


if __name__ == '__main__':
    main()
