import pandas as pd
from pathlib import Path

def read_excel(file_path:Path) -> str:
    df = pd.read_excel(file_path)
    return df.to_string(index=False)
