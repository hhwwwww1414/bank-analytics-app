"""
generator_synth.py – создаёт clients_synth.pkl / accounts_synth.pkl
по заданным параметрам.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from library.common_funcs import save_df

DATA_DIR = Path(__file__).parent.parent / "data"

@dataclass
class SynthParams:
    n_clients: int = 1000
    seed: int = 42
    income_mu: float = 10.5      # для lognormal
    income_sigma: float = 0.4

def generate(params: SynthParams) -> None:
    rng = np.random.default_rng(params.seed)
    cities  = ["Москва", "СПб", "Новосиб", "Екб", "Казань"]
    genders = rng.choice(["М", "Ж"], params.n_clients)

    clients = pd.DataFrame({
        "client_id": np.arange(1, params.n_clients + 1),
        "last_name": rng.choice(["Иванов", "Петров", "Сидоров", "Кузнецов"], params.n_clients),
        "first_name": rng.choice(["Иван", "Мария", "Сергей", "Ольга"], params.n_clients),
        "age": rng.integers(18, 70, params.n_clients),
        "gender": genders,
        "city": rng.choice(cities, params.n_clients),
        "income": np.round(rng.lognormal(params.income_mu, params.income_sigma, params.n_clients), 2),
        "reg_date": pd.to_datetime("2018-01-01") + pd.to_timedelta(rng.integers(0, 365 * 3, params.n_clients), unit="D"),
    })

    n_acc = int(params.n_clients * 1.2)
    accounts = pd.DataFrame({
        "account_id": np.arange(1, n_acc + 1),
        "client_id": rng.choice(clients["client_id"], n_acc),
        "account_type": rng.choice(["Дебетовый", "Кредитный", "Сберегательный"], n_acc),
        "balance": rng.uniform(1000, 1_000_000, n_acc).round(2),
        "currency": "EUR",
        "open_date": pd.to_datetime("2018-01-01") + pd.to_timedelta(rng.integers(0, 365 * 3, n_acc), unit="D"),
    })

    DATA_DIR.mkdir(exist_ok=True, parents=True)
    save_df(clients, DATA_DIR / "clients_synth.pkl")
    save_df(accounts, DATA_DIR / "accounts_synth.pkl")
