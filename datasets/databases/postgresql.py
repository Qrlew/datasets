from typing import Optional
from time import sleep
import subprocess
from sqlalchemy import create_engine, Engine, MetaData, text
from datasets.database import MutableDatabase

NAME: str = "qrlew-datasets"
PORT: int = 5432
USER: str = "postgres"
PASSWORD: str = "qrlew-datasets"

class PostgreSQL(MutableDatabase):
    def __init__(self, name=NAME, user=USER, password=PASSWORD, port=PORT) -> None:
        self.name = name
        self.user = user
        self.password = password
        self.port = port

    def try_get_existing(self) -> Optional[Engine]:
        """Try to connect to postgresql"""
        try:
            engine = create_engine(f'postgresql+psycopg://{self.user}:{self.password}@localhost:{self.port}')
            # Try to connect
            with engine.connect() as connection:
                tables = connection.execute(text('''SELECT * FROM pg_catalog.pg_tables WHERE schemaname='public' '''))
                for table in tables:
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
                '--name', self.name,
                '-d', '--rm',
                '-e', f'POSTGRES_PASSWORD={PASSWORD}',
                '-p', f'{self.port}:5432',
                'postgres'])
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
