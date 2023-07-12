from typing import Optional
from time import sleep
import subprocess
from sqlalchemy import create_engine, Engine, MetaData, text
from datasets.database import MutableDatabase

NAME: str = "qrlew-mariadb"
PORT: int = 3306
USER: str = "qrlew"
PASSWORD: str = "qrlew-mariadb"

class MariaDB(MutableDatabase):
    def __init__(self, name=NAME, user=USER, password=PASSWORD, port=PORT) -> None:
        self.name = name
        self.user = user
        self.password = password
        self.port = port

    def try_get_existing(self) -> Optional[Engine]:
        """Try to connect to postgresql"""
        try:
            engine = create_engine(f'mysql+pymysql://{self.user}:{self.password}@localhost:{self.port}')
            # Try to connect
            with engine.connect() as conn:
                for table in conn.tables():
                    print(table)
            return engine
        except:
            return None

    def try_get_container(self) -> Optional[Engine]:
        """Try to start or run a postgresql container"""
        # Try to start an existing container
        if subprocess.run(['docker', 'start', self.name]).returncode != 0:
            # Run a new container
            subprocess.run([
                'docker',
                'run',
                '-v', '/tmp:/tmp',
                '--name', self.name,
                '--detach', '--rm',
                '--env', f'MARIADB_USER={self.user}',
                '--env', f'MARIADB_PASSWORD={self.password}',
                '--env', f'MARIADB_ROOT_PASSWORD={self.password}',
                '--port', f'{self.port}:3306',
                'mariadb:latest'])
        attempt = 0
        while subprocess.run(['docker', 'exec', self.name, 'pg_isready']).returncode != 0 and attempt<10:
            print("Waiting postgresql to be ready...")
            sleep(1)
            attempt += 1
        return self.try_get_existing()

    # Implements engine
    def engine(self) -> Engine:
        """Create a postgresql engine"""
        engine = self.try_get_existing()
        if engine is None:
            engine = self.try_get_container()
        assert(engine is not None)
        return engine
    
    # Dump psql files
    def dump(self, path: str) -> None:
        """Dump psql"""
        subprocess.run(['docker', 'exec', self.name, 'pg_dump',
                        '-h', 'localhost',
                        '-U', self.user,
                        '-Fp',
                        '-n', 'financial',
                        '-f', path])
