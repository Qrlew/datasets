from sqlalchemy import create_engine, text, MetaData, Table, Column
from sqlalchemy import Integer, String
from sqlalchemy.schema import CreateTable
from datasets.sources.financial import Financial
from datasets.sources.loader import Loader
from datasets.databases.postgresql import PostgreSQL
from datasets.databases.mariadb import MariaDB

# Get a source db
input = Financial()

# Copy to Postgresql
# output = PostgreSQL()
# output.set_schema('financial')
# output.add(input)
# output.dump('/tmp/pg_financial')

# db = MariaDB()
# db._dump('relational.fit.cvut.cz', 'guest', 'relational', 'financial', '/tmp/financial.sql')

output = PostgreSQL()
# output.set_schema('financial')
# output.load('/tmp/financial.sql')

loader = Loader(output)
loader.load(input)