import re
import io
import sqlite3
import pandas as pd
from pathlib import Path

CSV_PATH = Path('db/upcPrice.txt')
DB_PATH = Path('db/upcPrice.db')
TABLE_NAME = 'upc'
COLUMNS = ['upc', 'format', 'desc', 'prix']
DTYPES = {'upc': 'str', 'format': 'str', 'desc': 'str', 'prix': 'float'}


class UPCDatabase:
    """
    Class to handle the UPC database.
    """
    def __init__(self, db_path: Path=DB_PATH, csv_path: Path=CSV_PATH, table_name: str=TABLE_NAME, normalize: bool=False):
        self.db_path = db_path
        self.csv_path = csv_path
        self.table_name = table_name
        self.con = None

        if not self.db_path.exists() or normalize:
            self.normalize()
        
        self.con = self.open()
        self.cur = self.con.cursor()
    
    def __del__(self):
        self.close()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self) -> sqlite3.Connection:
        """
        Opens the UPC database.
        """
        if self.con is None:
            self.con = sqlite3.connect(str(self.db_path))
            self.con.row_factory = sqlite3.Row
        return self.con
    
    def close(self):
        """
        Closes the UPC database.
        """
        self.cur.close()
        self.con.close()

    def get_upc_info(self, upc: str) -> sqlite3.Row:
        """
        Get info about UPC from the database.
        """
        self.cur.execute(f"SELECT * FROM {self.table_name} WHERE upc='{upc}';")
        res = self.cur.fetchone()
        return res
    
    def normalize(self):
        """
        Normalizes the UPC database.
        """
        out = io.StringIO()
        pattern = re.compile(r'[\b\r]')
        with open(self.csv_path, 'r', encoding='cp850', newline='\n') as db_in:
            for line in db_in:
                out.write(re.sub(pattern, '', line))
        
        out.seek(0)
        df = pd.read_csv(out, sep=',', names=COLUMNS, dtype=DTYPES, engine="python", on_bad_lines=bad_line_handler)
        df.desc = df.desc.str.strip()
        df.to_sql('upc', self.open(), index=False, if_exists='replace')
        out.close()


def bad_line_handler(line: list[str]) -> list[str] | None:
    """
    Handles a bad line in the UPC database.
    The usual format is "upc, format, desc, unused, ..., unused, prix".
    """
    return line[:3] + [line[-1]]


if __name__=='__main__':
    db = UPCDatabase()
    print(dict(db.get_upc_info("0715067020402")))