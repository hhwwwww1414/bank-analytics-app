"""
data_management.py
------------------
CRUD-функции для справочников «Клиенты» и «Счета».

Источник данных выбирается динамически через scripts.app_state.mode
и переключается на лету без перезапуска GUI.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

from library.common_funcs import load_df, save_df, read_config
import scripts.app_state as app_state          # ← импортируем модуль, не переменную!

CONFIG = read_config()
DATA_DIR = Path(__file__).parent.parent / CONFIG["PATHS"]["data_dir"]


# -------------------------------------------------------------------------
def _primary_file(base: str) -> Path:
    """clients_real.pkl / clients_synth.pkl в зависимости от текущего режима."""
    suffix = "real" if app_state.mode is app_state.DataMode.REAL else "synth"
    return DATA_DIR / f"{base}_{suffix}.pkl"


def _actual_file(base: str) -> Path:
    """Если «нового» файла ещё нет, используем старое имя без суффикса."""
    new_path = _primary_file(base)
    old_path = DATA_DIR / f"{base}.pkl"
    return new_path if new_path.exists() else old_path


# -------------------------------------------------------------------------#
#                       CRUD :  К Л И Е Н Т Ы                               #
# -------------------------------------------------------------------------#
def load_clients() -> pd.DataFrame:
    return load_df(_actual_file("clients"))


def save_clients(df: pd.DataFrame) -> None:
    save_df(df, _primary_file("clients"))


def add_client(df: pd.DataFrame, client_row: dict) -> pd.DataFrame:
    return pd.concat([df, pd.DataFrame([client_row])], ignore_index=True)


def delete_client(df: pd.DataFrame, client_id: int) -> pd.DataFrame:
    return df[df["client_id"] != client_id].reset_index(drop=True)


# -------------------------------------------------------------------------#
#                       CRUD :  С Ч Е Т А                                   #
# -------------------------------------------------------------------------#
def load_accounts() -> pd.DataFrame:
    return load_df(_actual_file("accounts"))


def save_accounts(df: pd.DataFrame) -> None:
    save_df(df, _primary_file("accounts"))


def add_account(df: pd.DataFrame, account_row: dict) -> pd.DataFrame:
    return pd.concat([df, pd.DataFrame([account_row])], ignore_index=True)


def delete_account(df: pd.DataFrame, account_id: int) -> pd.DataFrame:
    return df[df["account_id"] != account_id].reset_index(drop=True)
