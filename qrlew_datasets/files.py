from pathlib import Path
from urllib.request import urlretrieve

class File:
    def __init__(self, name: str) -> None:
        self.name = name
        self.remote_bucket = 'https://storage.googleapis.com/qrlew-datasets/'
        if not self.local().is_file():
            self.local().parent.mkdir(parents=True, exist_ok=True)
            urlretrieve(self.remote(), self.local().as_posix())

    def local(self) -> Path:
        raise NotImplementedError()

    def remote(self) -> str:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f'{self.name} <- {self.local()} <- {self.remote()}'

class SQL(File):
    def local(self) -> Path:
        return Path('/') / 'tmp' / 'qrlew-datasets' / f'{self.name}.sql'
    
    def remote(self) -> str:
        if self.name == 'hepatitis':
            return f'{self.remote_bucket}{self.name}/Hepatitis_std.sql'
        if self.name == 'imdb':
            return f'{self.remote_bucket}{self.name}/imdb_ijs.sql'
        # Default treatment
        return f'{self.remote_bucket}{self.name}/{self.name}.sql'

class CSV(File):
    def local(self) -> Path:
        return Path('/') / 'tmp' / 'qrlew-datasets' / f'{self.name}.csv'
    
    def remote(self) -> str:
        # Default treatment
        return f'{self.remote_bucket}{self.name}/{self.name}.csv'
