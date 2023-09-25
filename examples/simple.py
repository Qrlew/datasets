
import subprocess
import logging
from datasets.databases import PostgreSQL

logging.basicConfig(level=logging.DEBUG)

name = 'pyqrlew-db'
# subprocess.run([
#     'docker',
#     'run',
#     '--hostname', name,
#     '--volume', '/tmp:/tmp',
#     '--name', name,
#     '--detach', '--rm',
#     '--env', f'POSTGRES_PASSWORD={name}',
#     '--publish', '5432:5432',
#     'postgres'])

db = PostgreSQL(name=name, user='postgres', password=name, port=5433)
db.load('datasets/sources/extract/extract.sql')
db.set_schema('extract')
db.dump('/tmp/test.dump')