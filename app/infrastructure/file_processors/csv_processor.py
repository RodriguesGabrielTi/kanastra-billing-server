from typing import IO, List, Dict, Type
import pandas as pd
from io import TextIOWrapper


class CsvProcessor:
    def process(self, file: IO[bytes], columns_map: Dict[str, str], dtype: Dict[str, Type[any]]) -> List[Dict]:
        """Reads a CSV file and returns a list of dictionaries."""
        file_stream = TextIOWrapper(file, encoding="utf-8")
        df = pd.read_csv(
            file_stream,
            dtype=dtype,
        )
        return df.rename(columns=columns_map).to_dict(orient="records")
