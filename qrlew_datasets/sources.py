import subprocess
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from qrlew_datasets.database import Database
from qrlew_datasets.network import Network

class RelationalDatasetRepository(Database):
    '''Sources from relational.fit.cvut.cz'''
    def __init__(self, name: str) -> None:
        super().__init__()
        self._schema = name

    def engine(self) -> Engine:
        return create_engine(f'mysql+pymysql://guest:relational@relational.fit.cvut.cz:3306/{self.schema()}')
    
    def url(self) -> str:
        return f'mysql://guest:relational@relational.fit.cvut.cz:3306/{self.schema()}'
    
    def schema(self) -> str:
        return self._schema

class Financial(RelationalDatasetRepository):
    def __init__(self) -> None:
        super().__init__('financial')

class Hepatitis(RelationalDatasetRepository):
    def __init__(self) -> None:
        super().__init__('Hepatitis_std')

class IMDB(RelationalDatasetRepository):
    def __init__(self) -> None:
        super().__init__('imdb_ijs')

NAME: str = "qrlew-pgloader"

class Loader:
    '''Load different sources to destination'''
    def __init__(self, destination: Database) -> None:
        self.destination = destination
        self.net = Network().name

    def load(self, source: Database) -> bool:
        """Try to run pgloader to load a DB into the target DB"""
        # Try to start an existing container
        subprocess.run([
                'docker',
                'run',
                '--rm',
                '-it',
                '--net', self.net,
                'dimitri/pgloader:latest',
                'pgloader',
                 source.url(),
                 self.destination.url()])
        return True