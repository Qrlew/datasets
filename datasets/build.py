from sqlalchemy import create_engine, text, MetaData, Table, Column
from sqlalchemy import Integer, String
from sqlalchemy.schema import CreateTable
from datasets.sources.financial.financial import Financial
from datasets.sources.loader import Loader
from datasets.databases.postgresql import PostgreSQL
from datasets.databases.mariadb import MariaDB

database = PostgreSQL()
# loader = Loader(database)
# loader.load(Financial())

# database.set_schema('financial')
# database.dump('/tmp/financial.sql')

print(database.declaration())