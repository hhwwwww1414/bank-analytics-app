import pandas as pd
import tempfile
from pathlib import Path

import pytest

from scripts import data_management as dm

@pytest.fixture
def tmp_clients_file(tmp_path):
    # Создаём пустой файл-источник
    p = tmp_path / "clients.pkl"
    # Создаём DataFrame с двумя записями и сохраняем туда
    df = pd.DataFrame([
        {'client_id': 1, 'first_name': 'Иван', 'age': 30},
        {'client_id': 2, 'first_name': 'Ольга', 'age': 25},
    ])
    dm.save_df(df, p)  # сохраняем через common_funcs.save_df
    return df, p

def test_load_clients(tmp_clients_file, monkeypatch):
    df_orig, pkl = tmp_clients_file
    # Подменяем путь в модуле data_management
    monkeypatch.setattr(dm, "CLIENTS_FILE", pkl)
    df_loaded = dm.load_clients()
    pd.testing.assert_frame_equal(df_loaded, df_orig)

def test_add_and_delete_client(monkeypatch):
    # Создадим DataFrame «на лету»
    df = pd.DataFrame([{'client_id': 1, 'first_name': 'A'}])
    # Проверяем add_client
    df2 = dm.add_client(df, {'client_id': 2, 'first_name': 'B'})
    assert len(df2) == 2
    assert set(df2['client_id']) == {1, 2}

    # Проверяем delete_client
    df3 = dm.delete_client(df2, client_id=1)
    assert len(df3) == 1
    assert df3.iloc[0]['client_id'] == 2

@pytest.fixture
def tmp_accounts_file(tmp_path):
    p = tmp_path / "accounts.pkl"
    df = pd.DataFrame([
        {'account_id': 101, 'client_id': 1, 'balance': 1000.0},
        {'account_id': 102, 'client_id': 2, 'balance': 2000.0},
    ])
    dm.save_df(df, p)
    return df, p

def test_load_accounts(tmp_accounts_file, monkeypatch):
    df_orig, pkl = tmp_accounts_file
    monkeypatch.setattr(dm, "ACCOUNTS_FILE", pkl)
    df_loaded = dm.load_accounts()
    pd.testing.assert_frame_equal(df_loaded, df_orig)

def test_add_and_delete_account():
    df = pd.DataFrame([{'account_id': 1, 'client_id': 1}])
    df2 = dm.add_account(df, {'account_id': 2, 'client_id': 1})
    assert len(df2) == 2
    assert set(df2['account_id']) == {1, 2}

    df3 = dm.delete_account(df2, account_id=1)
    assert len(df3) == 1
    assert df3.iloc[0]['account_id'] == 2
