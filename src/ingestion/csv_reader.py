import pandas as pd
from pathlib import Path

def read_csv(file_path: Path) -> str:
    df = pd.read_csv(file_path)
    return df.to_string(index = False)