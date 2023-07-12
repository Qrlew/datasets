from typing import Optional
from time import sleep
import subprocess
from sqlalchemy import create_engine as create_sqlalchemy_engine, Engine, MetaData, text

NAME: str = "qrlew-datasets"
PORT: int = 5432
USER: str = "postgres"
PASSWORD: str = "qrlew-datasets"

def try_get_existing(user=USER, password=PASSWORD, port=PORT) -> Optional[Engine]:
    """Try to connect to postgresql"""
    try:
        return create_sqlalchemy_engine(f'postgresql+psycopg://{user}:{password}@localhost:{port}')
    except:
        return None

def try_get_container(name=NAME, user=USER, password=PASSWORD, port=PORT) -> Optional[Engine]:
    """Try to start or run a postgresql container"""
    # Try to start an existing container
    if subprocess.run(['docker', 'start', name]).returncode != 0:
        # Run a new container
        subprocess.run([
             'docker',
             'run',
             '--name', name,
             '-d', '--rm',
             '-e', f'POSTGRES_PASSWORD={PASSWORD}',
             '-p', f'{port}:5432',
             'postgres'])
    attempt = 0
    while subprocess.run(['docker', 'exec', name, 'pg_isready']).returncode != 0 and attempt<10:
        print("Waiting postgresql to be ready...")
        sleep(1)
        attempt += 1
    return try_get_existing(user, password, port)

def create_engine(name=NAME, user=USER, password=PASSWORD, port=PORT) -> Engine:
    engine = try_get_existing(user, password, port)
    if engine is None:
        engine = try_get_container(name, user, password, port)
    # assert(engine is not None)
    return engine
