from sqlalchemy import create_engine, text, MetaData, Table, Column
from sqlalchemy import Integer, String
from sqlalchemy.schema import CreateTable
from datasets.sources.financial import Financial
from datasets.databases.postgresql import PostgreSQL

# Get a source db
input = Financial()

print(input)

# Copy to Postgresql
output = PostgreSQL(port=5432)
output.add(input)

