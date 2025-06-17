"""
data_ingestion.py
-----------------
Скачивает датасет «Bank Marketing» (UCI #222) через ucimlrepo,
преобразует его в два справочника ― «Клиенты» и «Счета» ―
и сохраняет их в формате .pkl в каталоге work/data/.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from ucimlrepo import fetch_ucirepo  # pip install ucimlrepo

from library.common_funcs import save_df
from scripts.data_maps import JOB_INCOME_MAP, CITY_LIST, F_NAMES, L_NAMES

# --------------------------------------------------------------------------- #
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

UCI_DATASET_ID = 222          # Bank Marketing
SEED = 42                     # чтобы всё было воспроизводимо
# --------------------------------------------------------------------------- #


def load_dataset() -> pd.DataFrame:
    """Получает полный DataFrame из репозитория UCI."""
    ds = fetch_ucirepo(id=UCI_DATASET_ID)  # объект с features/targets/metadata
    return pd.concat([ds.data.features, ds.data.targets], axis=1)


# ---------- Преобразование в справочник «Клиенты» -------------------------- #
def make_clients(df_src: pd.DataFrame) -> pd.DataFrame:
    n = len(df_src)
    rng = np.random.default_rng(SEED)

    clients = pd.DataFrame({
        "client_id": np.arange(1, n + 1, dtype=int),
        "last_name": rng.choice(L_NAMES, size=n),
        "first_name": rng.choice(F_NAMES, size=n),
        "age": df_src["age"],
        "gender": rng.choice(["М", "Ж"], size=n),
        "city": rng.choice(
            CITY_LIST, size=n,
            p=[0.35, 0.25, 0.15, 0.15, 0.10]
        ),
        "income": df_src["job"].map(JOB_INCOME_MAP).astype(float),
        "reg_date": (
            pd.to_datetime("2018-01-01")
            + pd.to_timedelta(rng.integers(0, 365 * 3, size=n), unit="D")
        ),
    })
    return clients


# ---------- Преобразование в справочник «Счета» ---------------------------- #
def make_accounts(df_src: pd.DataFrame) -> pd.DataFrame:
    n = len(df_src)
    rng = np.random.default_rng(SEED + 1)

    accounts = pd.DataFrame({
        "account_id": np.arange(1, n + 1, dtype=int),
        "client_id": np.arange(1, n + 1, dtype=int),   # один счёт = один клиент
        "account_type": np.where(df_src["loan"] == "yes", "Кредитный", "Дебетовый"),
        "balance": df_src["balance"].astype(float).round(2),
        "currency": "EUR",
        "open_date": (
            pd.to_datetime("2018-01-01")
            + pd.to_timedelta(rng.integers(0, 365 * 3, size=n), unit="D")
        ),
    })
    return accounts


# ---------- Точка входа ----------------------------------------------------- #
def main() -> None:
    print("↓  Fetching Bank Marketing (UCI #222) …")
    raw = load_dataset()
    print(f"   {len(raw):,} rows loaded.")

    clients_df = make_clients(raw)
    accounts_df = make_accounts(raw)

    save_df(clients_df, DATA_DIR / "clients.pkl")
    save_df(accounts_df, DATA_DIR / "accounts.pkl")
    print("✔  Saved clients.pkl and accounts.pkl in work/data")


if __name__ == "__main__":
    main()
