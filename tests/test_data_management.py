import pandas as pd
import pytest
from pathlib import Path

import scripts.data_management as dm
from library.common_funcs import save_df

@pytest.fixture
def tmp_clients_file(tmp_path):
    # создаём DataFrame и сохраняем его как clients.pkl
    df = pd.DataFrame([
        {'client_id': 1, 'first_name': 'Иван', 'age': 30},
        {'client_id': 2, 'first_name': 'Ольга', 'age': 25},
    ])
    pkl = tmp_path / "clients.pkl"
    save_df(df, pkl)
    return df, pkl

def test_load_clients(tmp_clients_file, monkeypatch):
    df_orig, pkl = tmp_clients_file
    # подменяем внутреннюю функцию _actual_file, чтобы она вернула наш pkl
    monkeypatch.setattr(dm, "_actual_file", lambda base: pkl)
    df_loaded = dm.load_clients()
    pd.testing.assert_frame_equal(df_loaded, df_orig)

@pytest.fixture
def tmp_accounts_file(tmp_path):
    df = pd.DataFrame([
        {'account_id': 101, 'client_id': 1, 'balance': 1000.0},
        {'account_id': 102, 'client_id': 2, 'balance': 2000.0},
    ])
    pkl = tmp_path / "accounts.pkl"
    save_df(df, pkl)
    return df, pkl

def test_load_accounts(tmp_accounts_file, monkeypatch):
    df_orig, pkl = tmp_accounts_file
    monkeypatch.setattr(dm, "_actual_file", lambda base: pkl)
    df_loaded = dm.load_accounts()
    pd.testing.assert_frame_equal(df_loaded, df_orig)

def test_add_and_delete_client():
    df = pd.DataFrame([{'client_id': 1, 'first_name': 'A'}])
    df2 = dm.add_client(df, {'client_id': 2, 'first_name': 'B'})
    assert len(df2) == 2 and set(df2['client_id']) == {1, 2}

    df3 = dm.delete_client(df2, client_id=1)
    assert len(df3) == 1 and df3.iloc[0]['client_id'] == 2

def test_add_and_delete_account():
    df = pd.DataFrame([{'account_id': 1, 'client_id': 1}])
    df2 = dm.add_account(df, {'account_id': 2, 'client_id': 1})
    assert len(df2) == 2 and set(df2['account_id']) == {1, 2}

    df3 = dm.delete_account(df2, account_id=1)
    assert len(df3) == 1 and df3.iloc[0]['account_id'] == 2
