import json
import os
from typing import Any

import pandas as pd
from pandas import DataFrame


def load_config() -> dict:
    with open("src/config.json", 'r', encoding='utf-8') as file:
        return json.load(file)


def load_cookie_lexicon() -> dict:
    config = load_config()

    with open(config['paths']['utilities']['cookie_lexicon'], 'r', encoding='utf-8') as file:
        return json.load(file)


def load(path: str) -> Any:
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_cookie_db_local() -> pd.DataFrame:
    config = load_config()
    file_path = config['paths']['utilities']['cookie_db_local']

    if os.path.exists(file_path):
        return pd.read_csv(file_path)

    columns = ["ID", "Platform", "Category", "Cookie name", "Is Wildcard", "Wildcard Name", "Timestamp"]
    df = pd.DataFrame(columns=columns)

    df.to_csv(file_path, index=False)

    return df

def save_cookie_db_local(df: pd.DataFrame):
    config = load_config()
    file_path = config['paths']['utilities']['cookie_db_local']
    df.to_csv(file_path, index=False)


def load_cookie_db_open() -> DataFrame:
    config = load_config()

    return pd.read_csv(config['paths']['utilities']['cookie_db_open'])
