import pandas as pd

def parse_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_string(index=False)
