from pathlib import Path

import pandas as pd


def read_excel(file_path:Path) -> str:
    df = pd.read_excel(file_path)
    return df.to_string(index=False)
