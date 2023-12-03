import os.path
import importlib.resources as pkg_resources
from qrlew_datasets.files import SQL, CSV

def test_files():
    for sql_source in ['extract', 'financial', 'hepatitis', 'imdb', 'retail']:
        print(SQL(sql_source))
    
    for csv_source in ['heart_data']:
        print(CSV(csv_source))