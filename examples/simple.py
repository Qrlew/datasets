
import subprocess
import logging
from datasets.databases import PostgreSQL

logging.basicConfig(level=logging.DEBUG)

name = 'example-db'
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

db = PostgreSQL(name=name, user='postgres', password=name, port=5432)
db.load('/tmp/extract.sql')
db.set_schema('extract')
db.dump('test.dump')