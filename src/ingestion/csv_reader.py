from pathlib import Path

import pandas as pd


def read_csv(file_path: Path) -> str:
    df = pd.read_csv(file_path)
    return df.to_string(index = False)